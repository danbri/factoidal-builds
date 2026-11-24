// Native presentation of a Lean storage scene. Keep the released draw/readback
// plan intact; the host presents the native drawable after its readback checks.
//
// One session lives as long as the window. A frame costs one uniform write, one
// tile write and one command submission. The shader module and pipeline are
// built again only when Lean's WGSL text or its pipeline description changes;
// buffers are made again only when they must grow; the surface is configured
// again only when the frame size changes. (Issue 1268.)
import {requestRenderPlan,textureUsage,bufferUsage,commandInterpreter,type RenderPlan} from "./render_plan.ts";
import {SurfaceLifecycle} from "./surface_lifecycle.ts";
import {unpad,checkPixels} from "./gpu_transport.ts";
import type {HTMLArtifact,HTMLLayers} from "./native_html_engine.ts";
import {createLayerRenderer,readbackStep,READBACK_COMMANDS} from "./layer_compositor.ts";
import {createGpuGate,sceneCost,type PipeEvent} from "./gpu_pacing.ts";
// The gate's first guess of GPU ms per sceneCost unit, before any frame has measured one on
// this machine: 0.8, a little under the 0.99 measured on Spinal Tap on an Apple M1 (2026-11-15),
// so a faster GPU waits at most a little for the first heavy frame and the M1 blocks little.
// Read without failing where the host has no env permission (tests run without --allow-env).
const GPU_MS_PER_UNIT=(()=>{try{const v=Number(Deno.env.get("FOAFNAUT_GPU_MS_PER_UNIT")??"0.8");return Number.isFinite(v)&&v>=0?v:0.8;}catch{return 0.8;}})();

// The plan commands that read the frame back to the CPU (layer_compositor.ts). The host
// leaves them out for a frame that is not checked, and runs them in full under
// --check-engine, in every sweep and on an idle check.
export {READBACK_COMMANDS};

export type SessionStats={pipelineBuilds:number;planRequests:number;configures:number;uniformBuffers:number;tileBuffers:number;bindGroups:number};
export type DrawResult={presented:boolean;checked:boolean;pixelHash:string;steps:Record<string,number>;
  prepareMs:number;drawMs:number;presentedAt:number};

type Native={prepareSurface():void;surfaceState():unknown;canPresent():boolean};
type Growing={buffer:GPUBuffer;capacity:number};

/** Where frames go: the window's surface, or (--offscreen, issue 1268) a GPU texture of the
 * window size. Off screen, a frame is "presented" when it is drawn and its commands are
 * submitted to that texture; the pixel checks read the same texture. */
export type PresentTarget=Deno.UnsafeWindowSurface|{offscreen:true};

/** framesInFlight: GPU submissions of this session that may be in flight at once (gpu_pacing.ts);
 * 0 is no bound, for measurement. onGpuDone gets the GPU time of each piece of GPU work. */
export type SessionOptions={framesInFlight?:number;onGpuDone?:(gpuMs:number)=>void;
  /** The readbacks a replay of page `p`'s GPU commands made (page-gpu.mjs), for Lean's `gpuRead`. */
  onGpuReads?:(p:number,results:unknown[])=>void;
  /** Each submission and each blocking GPU wait, for the pipeline trace (HostPipeline.Model). */
  onPipe?:(event:PipeEvent)=>void;gateDebug?:(record:Record<string,unknown>)=>void};

export async function createHTMLWindowSession(device:GPUDevice,target:PresentTarget,native:Native,options:SessionOptions={}) {
  // The Lean svg-offscreen plan always answers rgba8unorm, which a macOS window
  // surface does not support; the surface and pipeline use its preferred format.
  // Off screen the texture has the same format, so every draw is the same.
  const format=navigator.gpu.getPreferredCanvasFormat();
  const surface="offscreen" in target?undefined:target;
  const context=surface?.getContext("webgpu") as GPUCanvasContext|undefined;
  let offscreenTexture:GPUTexture|undefined;
  const stats:SessionStats={pipelineBuilds:0,planRequests:0,configures:0,uniformBuffers:0,tileBuffers:0,bindGroups:0};
  // The plan is a pure function of these inputs on one device (render_plan.ts).
  const plans=new Map<string,RenderPlan>();
  let pipelineKey="",pipeline:GPURenderPipeline|undefined,uniform:Growing|undefined,tiles:Growing|undefined;
  let bindKey="",bindGroup:GPUBindGroup|undefined;
  let readback:Growing|undefined,configured="",lifecycle:SurfaceLifecycle<GPUTexture>|undefined;
  let disposed=false,lastSteps:Record<string,number>={},lastHash="",last:HTMLArtifact|undefined,lastChecked=false;
  const configure=(plan:RenderPlan,width:number,height:number)=>{
    const key=`${width}x${height}`;
    if(lifecycle&&configured===key)return;
    configured=key;stats.configures++;
    const driver=surface&&context?{
      configure(w:number,h:number){
        surface.width=w;surface.height=h;
        context.configure({device,format,alphaMode:"opaque",usage:textureUsage(plan.texture!.usage)});
      },
      prepare:()=>native.prepareSurface(),acquire:()=>context.getCurrentTexture(),
      present:()=>surface.present(),state:()=>native.surfaceState(),ready:()=>native.canPresent(),
    }:{
      configure(w:number,h:number){
        offscreenTexture?.destroy();
        offscreenTexture=device.createTexture({size:[w,h],format,usage:textureUsage(plan.texture!.usage)|GPUTextureUsage.RENDER_ATTACHMENT|GPUTextureUsage.COPY_SRC});
      },
      // The draw has already submitted its commands to the texture: nothing more to hand over.
      prepare:()=>{},acquire:()=>offscreenTexture!,present:()=>{},
      state:()=>({offscreen:true,format,width:offscreenTexture?.width??0,height:offscreenTexture?.height??0}),ready:()=>true,
    };
    if(!lifecycle){lifecycle=new SurfaceLifecycle<GPUTexture>(driver,format);}
    else lifecycle.setDriver(driver);
    lifecycle.configure(width,height);
  };
  const grow=(slot:Growing|undefined,bytes:number,usage:number,count:()=>void):Growing=>{
    if(slot&&slot.capacity>=bytes)return slot;
    slot?.buffer.destroy();count();
    return {buffer:device.createBuffer({size:bytes,usage}),capacity:bytes};
  };
  async function buildPipeline(plan:RenderPlan,code:string) {
    // Everything that shapes the pipeline, and nothing that is only a size.
    const key=JSON.stringify([code,plan.pipeline,plan.bindGroup,plan.format,plan.uniform.bindingType,plan.uniform.usage]);
    if(key===pipelineKey&&pipeline)return;
    const shader=device.createShaderModule({code});
    const diagnostics=await shader.getCompilationInfo();
    for(const m of diagnostics.messages)console.log(`${m.type} ${m.lineNum}:${m.linePos}: ${m.message}`);
    if(diagnostics.messages.some(m=>m.type==="error"))throw new Error("WGSL compilation failed: "+diagnostics.messages.filter(m=>m.type==="error").map(m=>`${m.lineNum}:${m.linePos} ${m.message}`).join("; "));
    pipeline=await device.createRenderPipelineAsync({layout:plan.pipeline.layout,
      vertex:{module:shader,entryPoint:plan.pipeline.vertexEntry},
      fragment:{module:shader,entryPoint:plan.pipeline.fragmentEntry,targets:[{format:plan.format}]},
      primitive:{topology:plan.pipeline.topology}});
    pipelineKey=key;bindKey="";stats.pipelineBuilds++;
  }
  // Two layers (issue 1268): each Lean render is drawn into two textures, and every
  // present is Lean's composite of them at an offset. A scroll in the band presents again.
  // A checked frame's readback is a blocking GPU wait too: in the pipeline trace it is the
  // frame's submit and a wait (the gate counts the frame as answered: settled).
  const onReadback=options.onPipe?(phase:"begin"|"end")=>{if(phase==="begin"){options.onPipe!("submit");options.onPipe!("ask");}else options.onPipe!("answer");}:undefined;
  const layered=createLayerRenderer(device,format,device.limits,onReadback);
  let lastLayers:{layers:HTMLLayers;width:number;height:number;offset:number}|undefined;
  // GPU work of this session runs one call at a time, in the order asked. Each call first
  // waits until the GPU has finished the work of the call before (the gate), so a page whose
  // frames cost the GPU more than the host's turn can not queue frames on the GPU. After a
  // halt (quit, window close) a call asks the GPU for nothing and presents nothing.
  const gate=createGpuGate(device.queue,options.framesInFlight??1,options.onGpuDone,GPU_MS_PER_UNIT,options.onPipe,{answersAtReturn:true,debug:options.gateDebug});
  let halted=false;
  const notPresented=():DrawResult=>({presented:false,checked:false,pixelHash:lastHash,steps:lastSteps,prepareMs:0,drawMs:0,presentedAt:0});
  let queue:Promise<unknown>=Promise.resolve();
  // `cost`: the GPU work of the call's last submission (sceneCost of what it drew; a function
  // when the call itself finds out: a partial or banded draw), so the gate can sleep through it
  // instead of blocking the thread in Deno's wait. A composite alone counts its pixels.
  // A checked draw reads the frame back, which blocks until the GPU is done: it first waits
  // until nothing is in flight and for the loop's next turn, so the block is its own frame's
  // work alone, right after input was taken.
  const inOrder=<T>(work:()=>Promise<T>,cost:number|(()=>number)=0,check=false):Promise<T|DrawResult>=>{
    const run=async()=>{
      if(check){await gate.quiet();await gate.nextTurn();}else await gate.before();
      if(halted)return notPresented();
      try{return await work();}finally{gate.after(typeof cost==="function"?cost():cost,check);}
    };
    const next=queue.then(run,run);queue=next.catch(()=>{});return next;
  };
  async function present(width:number,height:number,offset:number,check:boolean,start:number,drawn:Record<string,number>):Promise<DrawResult> {
    const setup=performance.now();
    const plan=await layered.plan(width,height,[0,0,0,0]);
    const planned=performance.now();
    configure(plan,width,height);
    const prepared=performance.now();
    if(prepared-setup>10)console.log(JSON.stringify({type:"native-html-cold-surface",
      width,height,planMs:planned-setup,configureMs:prepared-planned,totalMs:prepared-setup}));
    const texture=lifecycle!.acquire();
    if(!texture)return {presented:false,checked:false,pixelHash:lastHash,steps:lastSteps,prepareMs:prepared-start,drawMs:0,presentedAt:0};
    // A press darkening is not Lean's frame: its present is not checked against Lean's probes.
    const checking=check&&!layered.pressed;
    const result=await layered.composite(texture,width,height,offset,checking);
    lifecycle!.present();
    const presentedAt=performance.now();
    const steps={...drawn,...Object.fromEntries(Object.entries(result.steps).map(([k,v])=>["composite."+k,v]))};
    if(checking)lastHash=result.hash;
    lastSteps=steps;lastChecked=checking;last=undefined;
    return {presented:true,checked:checking,pixelHash:result.hash,steps,prepareMs:prepared-start,drawMs:presentedAt-prepared,presentedAt};
  }
  /** Page GPU commands of a turn (L4Factoidal.PageGpu): replay them; with page canvases on
   * screen, blit them into the page layer and present the composite again (no Lean call). */
  function pageGpu(p:number,commands:unknown[]):Promise<DrawResult|undefined> {
    return inOrder<DrawResult|undefined>(async()=>{
      if(disposed)return undefined;
      const reads=await layered.replayGpu(p,commands);
      if(reads?.length)options.onGpuReads?.(p,reads);
      if(!lastLayers||!layered.refreshCanvases())return undefined;
      return present(lastLayers.width,lastLayers.height,lastLayers.offset,false,performance.now(),{});
    });
  }
  // The GPU work of the last submission of the frame being drawn (the layer renderer says what
  // it drew: damage rectangles, the last band, a whole scene), plus the composite's pixels.
  let frameUnits:number|undefined;
  async function renderLayers(layers:HTMLLayers,width:number,height:number,offset:number,check:boolean):Promise<DrawResult> {
    if(disposed)throw new Error("Native HTML session already disposed");
    const start=performance.now();
    // A page whose last frames cost the GPU more than a frame is drawn in bands of about 16 ms
    // each (issue 450): Deno's onSubmittedWorkDone blocks this thread until the GPU is done, so
    // one large submission held input for seconds. Between bands the gate answers for the band
    // before and the loop takes input. A light page draws in one pass, as before.
    // The estimate of the whole page scene: its cost at the gate's measured rate (0 before any
    // measurement: one pass). Each band is a submission with its own cost, so the gate sleeps
    // through a band's GPU time, not through the whole frame's, before it asks.
    const wholeMs=gate.msFor(sceneCost(layers.page as never));
    const count=wholeMs>24?Math.min(16,Math.ceil(wholeMs/16)):1;
    options.gateDebug?.({ev:"frame",t:start,bands:count,wholeMs});
    const bands=count>1?{count,between:async(units:number)=>{gate.after(units);await new Promise(resolve=>setTimeout(resolve,0));await gate.before();}}:undefined;
    const drawn=await layered.drawLayers(layers,check,bands);
    frameUnits=drawn.units+width*height/1e6;
    const steps=Object.fromEntries([...Object.entries(drawn.chrome.steps).map(([k,v])=>["chrome."+k,v]),...Object.entries(drawn.page.steps).map(([k,v])=>["page."+k,v])]);
    lastLayers={layers,width,height,offset};
    return present(width,height,offset,check,start,steps);
  }
  async function render(frame:HTMLArtifact,check:boolean):Promise<DrawResult> {
    if(disposed)throw new Error("Native HTML session already disposed");
    const start=performance.now();
    const planKey=`${frame.width}x${frame.height}x${frame.data.length}`;
    let plan=plans.get(planKey);
    if(!plan){stats.planRequests++;plan={...await requestRenderPlan("svg-offscreen",format,frame as unknown as {width:number;height:number;data:number[]},device.limits),format};plans.set(planKey,plan);if(plans.size>32)plans.delete(plans.keys().next().value!);}
    await buildPipeline(plan,frame.wgsl);
    configure(plan,frame.width,frame.height);
    const tileWords=frame.tiles;
    // The shader reads arrayLength of both storage arrays, so the bound size is
    // the exact size even when the buffer behind it is larger.
    const uniformBytes=plan.uniform.bytes,tileBytes=tileWords?Math.max(16,tileWords.length*4):0;
    const uniformBefore=uniform?.buffer,tilesBefore=tiles?.buffer;
    uniform=grow(uniform,uniformBytes,bufferUsage(plan.uniform.usage),()=>{stats.uniformBuffers++;});
    if(tileWords)tiles=grow(tiles,tileBytes,GPUBufferUsage.STORAGE|GPUBufferUsage.COPY_DST,()=>{stats.tileBuffers++;});
    const wantBind=`${uniformBytes}|${tileBytes}`;
    if(!bindGroup||bindKey!==wantBind||uniform.buffer!==uniformBefore||tiles?.buffer!==tilesBefore){
      const entries:GPUBindGroupEntry[]=[{binding:plan.bindGroup.binding,resource:{buffer:uniform.buffer,offset:0,size:uniformBytes}}];
      if(tileWords)entries.push({binding:plan.bindGroup.binding+1,resource:{buffer:tiles!.buffer,offset:0,size:tileBytes}});
      bindGroup=device.createBindGroup({layout:pipeline!.getBindGroupLayout(plan.bindGroup.layoutIndex),entries});
      bindKey=wantBind;stats.bindGroups++;
    }
    if(check){
      readback=grow(readback,plan.readback!.bytes,bufferUsage(plan.readback!.usage),()=>{});
    }
    const prepared=performance.now();
    const texture=lifecycle!.acquire();
    if(!texture)return {presented:false,checked:false,pixelHash:lastHash,steps:lastSteps,prepareMs:prepared-start,drawMs:0,presentedAt:0};
    device.pushErrorScope("validation");let scoped=true;
    let steps:Record<string,number>={},hash="";
    try {
      device.queue.writeBuffer(uniform.buffer,plan.uniform.offset,new Float32Array(frame.data));
      if(tileWords)device.queue.writeBuffer(tiles!.buffer,0,new Uint32Array(tileWords));
      const interpreter=commandInterpreter(device,plan,{pipeline:pipeline!,bindGroup:bindGroup!},texture.createView(),{texture,readback:readback?.buffer});
      // Time each Lean plan command: mapRead waits for the GPU to finish the frame.
      for(const command of plan.commands){
        if(!check&&READBACK_COMMANDS.has(command))continue;
        const s=performance.now();await readbackStep(interpreter,command,onReadback);steps[command]=Math.round((performance.now()-s)*10)/10;
      }
      if(check){
        const bytes=interpreter.mapped();if(!bytes)throw new Error("Lean plan produced no native HTML readback");
        const pixels=unpad(bytes,plan.width,plan.height,plan.readback!.bytesPerRow);
        if(plan.format==="bgra8unorm")for(let i=0;i<pixels.length;i+=4){const b=pixels[i];pixels[i]=pixels[i+2];pixels[i+2]=b;}
        checkPixels(frame as unknown as Parameters<typeof checkPixels>[0],pixels);
        // FNV-1a over the frame: two renderers agree only if every byte agrees.
        let h=0x811c9dc5;const words=new Uint32Array(pixels.buffer,pixels.byteOffset,pixels.byteLength>>>2);
        for(let i=0;i<words.length;i++){h=Math.imul(h^words[i],0x01000193);}
        hash=(h>>>0).toString(16).padStart(8,"0");
        lastHash=hash;
      }
      const error=await device.popErrorScope();scoped=false;if(error)throw new Error(error.message);
    } catch(error) {
      // popErrorScope itself can fail after a device loss; preserve the cause.
      if(scoped)try{await device.popErrorScope();}catch{/* original failure */}
      throw error;
    }
    lifecycle!.present();
    const presentedAt=performance.now();
    lastSteps=steps;last=frame;lastChecked=check;
    return {presented:true,checked:check,pixelHash:hash,steps,prepareMs:prepared-start,drawMs:presentedAt-prepared,presentedAt};
  }
  return {
    /** Draw one Lean scene. check=true also reads the window back, checks Lean's probe pixels and hashes. */
    draw:(frame:HTMLArtifact,check:boolean):Promise<DrawResult>=>inOrder(()=>{lastLayers=undefined;return render(frame,check);},sceneCost(frame as never),check),
    /** Draw the two layers of one Lean render and present their composite at `offset`. */
    drawLayers:(layers:HTMLLayers,width:number,height:number,offset:number,check:boolean):Promise<DrawResult>=>inOrder(()=>{frameUnits=undefined;return renderLayers(layers,width,height,offset,check);},
      ()=>frameUnits??sceneCost(layers.page as never)+sceneCost(layers.chrome as never)+width*height/1e6,check),
    /** Present the layers already drawn at another offset: no Lean call and no scene draw. */
    shift:(offset:number,check:boolean):Promise<DrawResult>=>inOrder(async()=>{
      if(disposed)throw new Error("Native HTML session already disposed");
      if(!lastLayers)throw new Error("shift before any layers were drawn");
      lastLayers.offset=offset;
      return present(lastLayers.width,lastLayers.height,offset,check,performance.now(),{});
    },lastLayers?lastLayers.width*lastLayers.height/1e6:0,check),
    /** Replay a turn's page GPU commands and present the page canvases (no Lean call). */
    pageGpu,
    /** The press rectangles of the next presents (Lean's `press` answer); undefined clears them. */
    setPress:(rects:number[][]|undefined)=>layered.setPress(rects),
    get pressed(){return layered.pressed;},
    /** Draw the last presented scene again with the readback checks. Used after input has been idle. */
    checkLast():Promise<DrawResult|undefined> {
      return inOrder<DrawResult|undefined>(()=>lastLayers?renderLayers(lastLayers.layers,lastLayers.width,lastLayers.height,lastLayers.offset,true)
        :last?render(last,true):Promise.resolve(undefined),0,true);
    },
    get lastChecked(){return lastChecked;},
    /** Off screen: the texture the last frame was presented to (it has COPY_SRC), for --shot. */
    get offscreenTexture(){return offscreenTexture;},
    get frames(){return lifecycle?.framesPresented??0;},
    get steps(){return lastSteps;},
    get pixelHash(){return lastHash;},
    get stats(){return {...stats,layers:{...layered.stats},gpu:gate.stats};},
    /** Submit to done of recent GPU work, ms (about the GPU time, with the gate on). */
    get gpuTimes(){return gate.recent;},
    /** The host loop's turn, right after it took input: GPU waits start only here from now on
     * (gpu_pacing.ts `turn`), so at most one blocking wait comes between two pumps. */
    gpuTurn(){gate.turn();},
    /** Ms until the gate's next ask is due (null: none planned): the loop turns by then. */
    gpuDueIn():number|null {return gate.dueIn();},
    /** GPU submissions not yet answered for (the gate is waiting to ask, or for an answer). */
    get gpuInFlight(){return gate.inFlight;},
    /** Quit or close: from now on no call asks the GPU for work. Resolves when the GPU has
     * finished what it was given (at most the frames in flight). */
    halt():Promise<unknown> {halted=true;return gate.idle();},
    dispose(){
      if(disposed)return;disposed=true;
      if(lifecycle)context?.unconfigure();
      offscreenTexture?.destroy();
      readback?.buffer.destroy();uniform?.buffer.destroy();tiles?.buffer.destroy();layered.dispose();
    },
  };
}
