// GPU side of the two-layer render (WebDocument.layersJSON, issue 1268). Lean gives
// the chrome layer, the page layer of a band, the scene WGSL, the composite WGSL and
// every plan command. The host keeps a texture for each layer and runs the plans; it
// decides no colour and no position: the composite offset is scroll-bandTop, kept in
// the band that Lean gives (keepFrom..keepTo; clampOffset below).
//
// A scroll inside the band only runs the composite plan again with a new offset.
import {requestRenderPlan,bufferUsage,commandInterpreter,type RenderPlan,type DeviceFacts} from "./render_plan.ts";
import {unpad,checkPixels} from "./gpu_transport.ts";
import {sceneCost,sceneCostIn} from "./gpu_pacing.ts";
import type {HTMLArtifact,HTMLLayers} from "./native_html_engine.ts";
// Page canvases drawn by page scripts: Lean-validated GPU commands (L4Factoidal.PageGpu,
// docs/designissues/2026-11-08-page-gpu.md), the same replay as the Hub's.
import {createPageGpu} from "../../../docs/web/hub/foafnaut/page-gpu.mjs";

/** The canvas rectangles of a layers answer (WebDocument.canvasRects) and Lean's blit WGSL. */
type CanvasPlace={canvases?:{node:number;rect:number[];clip:number[]}[];canvasBlit?:string};

// The plan commands that read the frame back to the CPU. Lean's plan always
// lists them. The host leaves them out for a frame that is not checked.
export const READBACK_COMMANDS:ReadonlySet<string>=new Set(["copyTextureToBuffer","mapRead","readMapped","unmap"]);
/** One plan command; `mapRead` is bracketed by `onReadback` (the blocking part is the call). */
export function readbackStep(interpreter:{step(command:string):unknown},command:string,onReadback?:(phase:"begin"|"end")=>void):unknown {
  if(command!=="mapRead"||!onReadback)return interpreter.step(command);
  onReadback("begin");
  try{return interpreter.step(command);}finally{onReadback("end");}
}

/** FNV-1a over the pixels: two renderers agree only if every byte agrees. */
export function pixelHash(pixels:Uint8Array):string {
  let h=0x811c9dc5;const words=new Uint32Array(pixels.buffer,pixels.byteOffset,pixels.byteLength>>>2);
  for(let i=0;i<words.length;i++){h=Math.imul(h^words[i],0x01000193);}
  return (h>>>0).toString(16).padStart(8,"0");
}

/** The composite offset for a scroll: the page row of the band shown at the top of the view,
 * kept inside the band. `exact` is false when the scroll is past the band and the view waits for a new one. */
export function clampOffset(place:HTMLLayers["layers"],scroll:number):{offset:number;exact:boolean} {
  const last=Math.max(0,place.bandHeight-place.view);
  const offset=Math.max(0,Math.min(last,scroll-place.bandTop));
  return {offset,exact:offset===scroll-place.bandTop};
}
/** True when Lean says this band shows the scroll with no new render. */
export function keeps(place:HTMLLayers["layers"],scroll:number):boolean {return scroll>=place.keepFrom&&scroll<=place.keepTo;}

type Growing={buffer:GPUBuffer;capacity:number};
/** What Lean says changed since the answer `base` (`WebPaint.retainedAnswer`): `rects` in the
 * scene's pixels. A host whose texture holds answer `base` can draw those pixels alone. */
type Damage={id:number;base:number|null;rects:number[][]|null};
/** The same scene words: width, height, shader text, storage data and tile words, each word
compared exactly (a float by its bits). */
type Words=ArrayLike<number>;
function sameWords(a:Words|undefined,b:Words|undefined):boolean {
  if(!a||!b||a.length!==b.length)return a===b;
  if(a instanceof Float32Array&&b instanceof Float32Array){
    const x=new Uint32Array(a.buffer,a.byteOffset,a.length),y=new Uint32Array(b.buffer,b.byteOffset,b.length);
    for(let i=0;i<x.length;i++)if(x[i]!==y[i])return false;
    return true;
  }
  for(let i=0;i<a.length;i++)if(!Object.is(a[i],b[i]))return false;
  return true;
}
export function sameScene(a:HTMLArtifact,b:HTMLArtifact):boolean {
  return a.width===b.width&&a.height===b.height&&a.wgsl===b.wgsl&&sameWords(a.data as Words,b.data as Words)&&
    sameWords((a as unknown as {tiles?:Words}).tiles,(b as unknown as {tiles?:Words}).tiles);
}
type Slot={uniform?:Growing;tiles?:Growing;bind?:GPUBindGroup;bindKey:string;texture?:GPUTexture;size:string;
  /** The Lean answer `damage.id` drawn in `texture`. */
  drawn?:number;
  /** The answer with no damage (the chrome layer) the texture was drawn from. */
  drawnFrame?:HTMLArtifact};
export type PassResult={steps:Record<string,number>;pixels?:Uint8Array;hash:string;units?:number};

// The composite uniform: one word-of-four for the place and the rectangle count, then the
// rectangles (WebDocument.compositeShader: array<vec4u,maxPressRects+2>).
export const MAX_PRESS_RECTS=8;
const PLACE_WORDS=4*(MAX_PRESS_RECTS+2);
const LAYER_USAGE=()=>GPUTextureUsage.RENDER_ATTACHMENT|GPUTextureUsage.TEXTURE_BINDING|GPUTextureUsage.COPY_SRC;

/** `onReadback`: called just before and just after the call that maps the readback (Deno's
 * mapAsync blocks inside the call until the GPU is done), for the pipeline trace. */
export function createLayerRenderer(device:GPUDevice,format:GPUTextureFormat,limits:DeviceFacts=device.limits,onReadback?:(phase:"begin"|"end")=>void) {
  const plans=new Map<string,RenderPlan>();
  const pipelines=new Map<string,GPURenderPipeline>();
  const stats={planRequests:0,pipelineBuilds:0,layerTextures:0,bindGroups:0,scenesFull:0,scenesPartial:0,scenesKept:0,scenesSame:0,bandedScenes:0};
  const grow=(slot:Growing|undefined,bytes:number,usage:number):Growing=>{
    if(slot&&slot.capacity>=bytes)return slot;
    slot?.buffer.destroy();
    return {buffer:device.createBuffer({size:bytes,usage}),capacity:bytes};
  };
  async function plan(width:number,height:number,data:ArrayLike<number>):Promise<RenderPlan> {
    const key=`${width}x${height}x${data.length}`;
    let p=plans.get(key);
    if(!p){
      stats.planRequests++;
      p={...await requestRenderPlan("svg-offscreen",format,{width,height,data:data as number[]},limits),format};
      plans.set(key,p);if(plans.size>32)plans.delete(plans.keys().next().value!);
    }
    return p;
  }
  async function pipelineFor(p:RenderPlan,code:string):Promise<GPURenderPipeline> {
    const key=JSON.stringify([code,p.pipeline,p.format]);
    const kept=pipelines.get(key);if(kept)return kept;
    const started=performance.now();
    const shader=device.createShaderModule({code});
    const moduleReady=performance.now();
    const infoPending=shader.getCompilationInfo();
    const infoReturned=performance.now();
    const info=await infoPending;
    const infoReady=performance.now();
    if(info.messages.some(m=>m.type==="error"))throw new Error("WGSL compilation failed: "+info.messages.filter(m=>m.type==="error").map(m=>`${m.lineNum}:${m.linePos} ${m.message}`).join("; "));
    const pipelinePending=device.createRenderPipelineAsync({layout:p.pipeline.layout,
      vertex:{module:shader,entryPoint:p.pipeline.vertexEntry},
      fragment:{module:shader,entryPoint:p.pipeline.fragmentEntry,targets:[{format:p.format}]},
      primitive:{topology:p.pipeline.topology}});
    const pipelineReturned=performance.now();
    const pipeline=await pipelinePending;
    const ready=performance.now();
    console.log(JSON.stringify({type:"native-html-cold-pipeline",wgslLength:code.length,format:p.format,
      moduleMs:moduleReady-started,infoCallMs:infoReturned-moduleReady,infoWaitMs:infoReady-infoReturned,
      createCallMs:pipelineReturned-infoReady,createWaitMs:ready-pipelineReturned,totalMs:ready-started}));
    stats.pipelineBuilds++;pipelines.set(key,pipeline);if(pipelines.size>8)pipelines.delete(pipelines.keys().next().value!);
    return pipeline;
  }
  let readback:Growing|undefined;
  // Run a Lean plan on one target texture; with check, read it back and hash it.
  async function run(p:RenderPlan,resources:{pipeline:GPURenderPipeline;bindGroup:GPUBindGroup},target:GPUTexture,check:boolean,
    write:()=>void):Promise<PassResult> {
    const started=performance.now();
    if(check)readback=grow(readback,p.readback!.bytes,bufferUsage(p.readback!.usage));
    device.pushErrorScope("validation");let scoped=true;
    try{
      write();
      const written=performance.now();
      const interpreter=commandInterpreter(device,p,resources,target.createView(),{texture:target,readback:readback?.buffer});
      const steps:Record<string,number>={};
      for(const command of p.commands){
        if(!check&&READBACK_COMMANDS.has(command))continue;
        const s=performance.now();await readbackStep(interpreter,command,onReadback);steps[command]=Math.round((performance.now()-s)*10)/10;
      }
      let pixels:Uint8Array|undefined,hash="";
      if(check){
        const bytes=interpreter.mapped();if(!bytes)throw new Error("Lean plan produced no readback");
        pixels=unpad(bytes,p.width,p.height,p.readback!.bytesPerRow);
        if(p.format==="bgra8unorm")for(let i=0;i<pixels.length;i+=4){const b=pixels[i];pixels[i]=pixels[i+2];pixels[i+2]=b;}
        hash=pixelHash(pixels);
      }
      const scopeStart=performance.now();
      const validation=device.popErrorScope();
      const scopeReturned=performance.now();
      const error=await validation;
      const scopeDone=performance.now();
      scoped=false;if(error)throw new Error(error.message);
      if(scopeDone-started>10)console.log(JSON.stringify({type:"native-html-cold-render-commands",
        width:p.width,height:p.height,writeMs:written-started,commandsMs:scopeStart-written,
        scopeCallMs:scopeReturned-scopeStart,scopeAwaitMs:scopeDone-scopeReturned,totalMs:scopeDone-started}));
      return {steps,pixels,hash};
    }catch(error){
      if(scoped)try{await device.popErrorScope();}catch{/* original failure */}
      throw error;
    }
  }
  // Lean's rectangles only, over the pixels already in the texture (the scene shader's pixel
  // does not read what is there). No readback: an interactive frame.
  async function drawDamage(p:RenderPlan,resources:{pipeline:GPURenderPipeline;bindGroup:GPUBindGroup},target:GPUTexture,rects:number[][],write:()=>void):Promise<PassResult> {
    device.pushErrorScope("validation");let scoped=true;
    try{
      write();
      const encoder=device.createCommandEncoder();
      const pass=encoder.beginRenderPass({colorAttachments:[{view:target.createView(),loadOp:"load",storeOp:"store"}]});
      pass.setPipeline(resources.pipeline);pass.setBindGroup(p.bindGroup.index,resources.bindGroup);
      for(const [x,y,w,h] of rects){pass.setScissorRect(x,y,w,h);pass.draw(p.draw.vertexCount,p.draw.instanceCount,p.draw.firstVertex,p.draw.firstInstance);}
      pass.end();
      device.queue.submit([encoder.finish()]);
      const error=await device.popErrorScope();scoped=false;if(error)throw new Error(error.message);
      return {steps:{},hash:""};
    }catch(error){
      if(scoped)try{await device.popErrorScope();}catch{/* original failure */}
      throw error;
    }
  }
  /** Draw one Lean scene into the slot's texture (made at the scene's size), or into `target`. */
  /** A heavy frame in bands (issue 450): `count` horizontal bands of the layer, each its own
   * submission, `between` awaited after each (the session lets the GPU gate answer and the
   * host's loop take input there). The scene shader's pixel does not read the target, so the
   * bands give the bytes of one draw. */
  type Bands={count:number;between:(units:number)=>Promise<void>};
  async function drawScene(slot:Slot,frame:HTMLArtifact,check:boolean,target?:GPUTexture,bands?:Bands):Promise<PassResult> {
    const started=performance.now();
    const p=await plan(frame.width,frame.height,frame.data);
    const planned=performance.now();
    const pipeline=await pipelineFor(p,frame.wgsl);
    const pipelined=performance.now();
    if(!target){
      const size=`${frame.width}x${frame.height}`;
      if(!slot.texture||slot.size!==size){
        slot.texture?.destroy();stats.layerTextures++;
        slot.texture=device.createTexture({size:[frame.width,frame.height],format:p.format,usage:LAYER_USAGE()});slot.size=size;slot.drawn=undefined;slot.drawnFrame=undefined;
      }
    }
    const textureReady=performance.now();
    const damage=(frame as unknown as {damage?:Damage}).damage;
    // The same answer already in the slot's texture: nothing to do.
    if(!target&&!check&&damage&&slot.drawn===damage.id){stats.scenesKept++;return {steps:{},hash:"",units:0};}
    // An answer with no damage (the chrome layer) whose words are those the texture was drawn
    // from: the scene shader's pixels are a function of those words. Exact comparison, no hash.
    if(!target&&!check&&!damage&&slot.drawnFrame&&sameScene(slot.drawnFrame,frame)){stats.scenesSame++;return {steps:{},hash:"",units:0};}
    const tileWords=frame.tiles;
    const uniformBytes=p.uniform.bytes,tileBytes=tileWords?Math.max(16,tileWords.length*4):0;
    const before=[slot.uniform?.buffer,slot.tiles?.buffer];
    slot.uniform=grow(slot.uniform,uniformBytes,bufferUsage(p.uniform.usage));
    if(tileWords)slot.tiles=grow(slot.tiles,tileBytes,GPUBufferUsage.STORAGE|GPUBufferUsage.COPY_DST);
    const buffersReady=performance.now();
    const want=`${uniformBytes}|${tileBytes}|${JSON.stringify(p.pipeline)}`;
    if(!slot.bind||slot.bindKey!==want||slot.uniform.buffer!==before[0]||slot.tiles?.buffer!==before[1]){
      const entries:GPUBindGroupEntry[]=[{binding:p.bindGroup.binding,resource:{buffer:slot.uniform.buffer,offset:0,size:uniformBytes}}];
      if(tileWords)entries.push({binding:p.bindGroup.binding+1,resource:{buffer:slot.tiles!.buffer,offset:0,size:tileBytes}});
      slot.bind=device.createBindGroup({layout:pipeline.getBindGroupLayout(p.bindGroup.layoutIndex),entries});slot.bindKey=want;stats.bindGroups++;
    }
    const bindReady=performance.now();
    const write=()=>{
      device.queue.writeBuffer(slot.uniform!.buffer,p.uniform.offset,(frame.data instanceof Float32Array?frame.data:new Float32Array(frame.data)) as Float32Array<ArrayBuffer>);
      if(tileWords)device.queue.writeBuffer(slot.tiles!.buffer,0,new Uint32Array(tileWords));
    };
    // The texture holds answer `damage.base` (scene shader pixels do not read the target): draw
    // only what changed. Off the frame path (`check`, or another target), the whole scene.
    const rects=!target&&!check&&damage?.rects&&damage.base!==null&&slot.drawn===damage.base&&slot.texture?damage.rects:undefined;
    // `units`: the GPU work of this call's last submission (gpu_pacing.ts sceneCost of what was
    // drawn: the rectangles, the last band, or the whole scene), for the session's GPU gate.
    let result:PassResult,units=0;
    const ready=performance.now();
    if(rects){
      stats.scenesPartial++;units=rects.length?sceneCostIn(frame as never,rects):0;
      result=rects.length?await drawDamage(p,{pipeline,bindGroup:slot.bind},slot.texture!,rects,write):(write(),{steps:{},hash:""});
    }else if(!target&&!check&&bands&&bands.count>1&&slot.texture){
      stats.scenesFull++;stats.bandedScenes=(stats.bandedScenes??0)+1;
      const rows=Math.ceil(frame.height/bands.count);
      result={steps:{},hash:""};
      for(let i=0;i*rows<frame.height;i++){
        const y=i*rows,h=Math.min(rows,frame.height-y);
        result=await drawDamage(p,{pipeline,bindGroup:slot.bind},slot.texture,[[0,y,frame.width,h]],i===0?write:()=>{});
        units=sceneCostIn(frame as never,[[0,y,frame.width,h]]);
        if(y+h<frame.height)await bands.between(units);
      }
    }else{stats.scenesFull++;units=sceneCost(frame as never);result=await run(p,{pipeline,bindGroup:slot.bind},target??slot.texture!,check,write);}
    if(!target){slot.drawn=damage?.id;slot.drawnFrame=damage?undefined:frame;}
    if(check&&result.pixels)checkPixels(frame as unknown as Parameters<typeof checkPixels>[0],result.pixels);
    const finished=performance.now();
    if(finished-started>10)console.log(JSON.stringify({type:"native-html-cold-layer",
      width:frame.width,height:frame.height,planMs:planned-started,pipelineMs:pipelined-planned,
      textureMs:textureReady-pipelined,buffersMs:buffersReady-textureReady,
      bindMs:bindReady-buffersReady,tailMs:ready-bindReady,resourcesMs:ready-pipelined,
      drawMs:finished-ready,totalMs:finished-started}));
    return {...result,units};
  }
  const chrome:Slot={bindKey:"",size:""},page:Slot={bindKey:"",size:""},single:Slot={bindKey:"",size:""};
  // deno-lint-ignore no-explicit-any
  let pageGpu:any;
  const blitCanvases=():boolean=>{
    const place=shown?.layers as CanvasPlace|undefined;
    return !!(place?.canvases&&page.texture&&pageGpu?.blit(page.texture,place.canvases,place.canvasBlit));
  };
  let shown:HTMLLayers|undefined,place:GPUBuffer|undefined,compositeBind:GPUBindGroup|undefined,compositeKey="";
  // Press rectangles from Lean's `press` answer, in source rows (WebDocument.compositePress).
  let pressRects:number[][]=[];
  let textureIds=new WeakMap<GPUTexture,number>(),nextId=0;
  const idOf=(t:GPUTexture)=>{let id=textureIds.get(t);if(id===undefined){id=++nextId;textureIds.set(t,id);}return id;};
  return {
    stats,
    plan,
    /** Draw both layers of one Lean render into their textures. */
    async drawLayers(layers:HTMLLayers,check:boolean,bands?:Bands):Promise<{chrome:PassResult;page:PassResult;units:number}> {
      const c=await drawScene(chrome,layers.chrome,check);
      const g=await drawScene(page,layers.page,check,undefined,bands);
      shown=layers;
      blitCanvases();
      return {chrome:c,page:g,units:(c.units??0)+(g.units??0)};
    },
    /** Replay page GPU commands (Lean's host commands of page session `p`), in order. */
    async replayGpu(p:number,commands:unknown[]):Promise<unknown[]>{return await (pageGpu??=createPageGpu(device)).replay(p,commands);},
    /** The page canvases again, into the page layer; true when one was drawn (then composite). */
    refreshCanvases:()=>blitCanvases(),
    /** Draw one single-frame Lean scene into `target`: the reference that the composite must equal. */
    drawSingle:(frame:HTMLArtifact,target:GPUTexture,check:boolean)=>drawScene(single,frame,check,target),
    get layers(){return shown;},
    /** Copy the layers into `target` (width x height): Lean's composite WGSL at this offset. */
    async composite(target:GPUTexture,width:number,height:number,offset:number,check:boolean):Promise<PassResult> {
      if(!shown)throw new Error("composite before any layers were drawn");
      const p=await plan(width,height,[0,0,0,0]);
      const pipeline=await pipelineFor(p,shown.layers.composite);
      place??=device.createBuffer({size:PLACE_WORDS*4,usage:GPUBufferUsage.UNIFORM|GPUBufferUsage.COPY_DST});
      const key=`${idOf(chrome.texture!)}|${idOf(page.texture!)}|${JSON.stringify(p.pipeline)}`;
      if(!compositeBind||compositeKey!==key){
        compositeBind=device.createBindGroup({layout:pipeline.getBindGroupLayout(p.bindGroup.layoutIndex),entries:[
          {binding:0,resource:chrome.texture!.createView()},{binding:1,resource:page.texture!.createView()},{binding:2,resource:{buffer:place}}]});
        compositeKey=key;stats.bindGroups++;
      }
      const words=new Uint32Array(PLACE_WORDS);
      words.set([shown.layers.top,offset,shown.layers.bandHeight,pressRects.length]);
      pressRects.forEach((rect,i)=>words.set(rect,4*(i+1)));
      return run(p,{pipeline,bindGroup:compositeBind},target,check,()=>device.queue.writeBuffer(place!,0,words));
    },
    /** The rectangles the next composites darken (Lean's `press` answer); none clears them. */
    setPress(rects:number[][]|undefined){
      pressRects=(rects??[]).slice(0,MAX_PRESS_RECTS).filter(r=>r.length===4&&r.every(n=>Number.isSafeInteger(n)&&n>=0&&n<2**31));
    },
    get pressed(){return pressRects.length>0;},
    dispose(){
      for(const slot of [chrome,page,single]){slot.texture?.destroy();slot.uniform?.buffer.destroy();slot.tiles?.buffer.destroy();}
      place?.destroy();readback?.buffer.destroy();textureIds=new WeakMap();pageGpu?.close();
    },
  };
}
export type LayerRenderer=ReturnType<typeof createLayerRenderer>;
