// The Lean HTML engine in a Deno Worker. Every engine call that can take more than
// about 2 ms runs here, one at a time, so the main thread keeps
// only the window, the event pump, input and the GPU (issue 1268). The engine is the
// Wasm module or, when a path is given, a native dylib; all Lean calls stay on this
// one thread. The worker holds no page state: each request carries its inputs, and
// the font is loaded once at start. No GPU or native window is used here.
//
// Input runs before ordinary work, in arrival order. All scriptSession turns use that
// lane too, so input cannot pass an earlier resize or timer turn of the same session.
// A request with `low` (a scroll prefetch) runs only when no other request waits, and a
// newer low request replaces a low one that has not started; the replaced one is answered
// `dropped`. `dropLow` drops the low request that has not started. A low request that has
// started runs to its end: a Lean call can not be stopped.
import {loadHTML,type HTMLArtifact,type HTMLEngine} from "./native_html_engine.ts";
import {loadFontFile} from "./native_html_document.ts";
import {fallbackFontHost,loadFallbackFonts} from "./native_html_fonts.ts";
import {htmlQueue} from "./native_html_queue.ts";
import {gateConsole} from "../../../docs/web/hub/foafnaut/log-gate.mjs";

import {REMOTE_CALLS,type RemoteCall} from "./native_html_calls.ts";
export {REMOTE_CALLS};
export type {RemoteCall};
export type WorkerRequest={id:number;op:"init";font?:{path:string;family:string};nativeEngine?:string;logAll?:boolean}
  |{id:number;op:"call";name:RemoteCall;args:unknown[];input?:boolean;low?:boolean}
  |{id:number;op:"dropLow"}
  // The fallback fonts a page needs (native_html_fonts.ts): chosen and read here, as bytes,
  // into this engine, before the calls sent after it.
  |{id:number;op:"pageFonts";source:string}
  // The serif face or the monospace face (serif_font.ts), into this engine, before the calls
  // sent after it.
  |{id:number;op:"serifFont"|"monoFont";path:string;family:string};
export type WorkerReply={id:number;ok:true;value?:unknown;ms:number}|{id:number;ok:false;error:string;dropped?:boolean};

let engine:Promise<HTMLEngine>|undefined;
// The worker's lines go through the log gate too (log-gate.mjs); --log-all comes with init.
const logGate=gateConsole(console,{name:"foafnaut worker"});
// Only an engine that answers its first font with `fonts` (the count held) adds a fallback
// font after it; an older one would take it as a replacement (issue 1274).
let fallbackFonts:ReturnType<typeof fallbackFontHost>|undefined;
const scope=globalThis as unknown as {onmessage:(event:MessageEvent<WorkerRequest>)=>void;postMessage(message:unknown,transfer?:Transferable[]):void};
type RenderCommand={op?:string;name?:string};
type RenderInputs={source:unknown;width:unknown;height:unknown;commands:string[];other:Record<string,string>};
let previousRender:RenderInputs|undefined;
const optionNames=["url","scripting","syntax","zoomUnit","textScalePercent","media","liberal",
  "visited","resourceFailures","animated","heldImages","partialNote"] as const;
function renderInputChanges(args:unknown[]){
  const [source,width,height,options]=args as [unknown,unknown,unknown,Record<string,unknown>|undefined];
  const commands=Array.isArray(options?.commands)?options.commands as RenderCommand[]:[];
  const encoded=commands.map(x=>JSON.stringify(x));
  const other:Record<string,string>={};
  for(const name of optionNames)other[name]=JSON.stringify(options?.[name])??"";
  const current={source,width,height,commands:encoded,other};
  const previous=previousRender;
  previousRender=current;
  let common=0;
  if(previous?.source===source){
    while(common<encoded.length&&encoded[common]===previous?.commands[common])common++;
  }
  const kinds:Record<string,number>=Object.create(null);
  for(const c of commands.slice(common)){
    const attr=c.op==="setAttribute"||c.op==="removeAttribute"||c.op==="setAttributeNS"||c.op==="removeAttributeNS";
    const key=attr?c.op+":"+c.name:c.op??"unknown";
    kinds[key]=(kinds[key]??0)+1;
  }
  return {
    sameSource:previous?.source===source,
    sameViewport:previous?.width===width&&previous?.height===height,
    changedOptions:optionNames.filter(name=>other[name]!==previous?.other[name]),
    commandCount:encoded.length,previousCount:previous?.commands.length??0,common,kinds,
  };
}

let captures = 0;
function recordGovHeader(request:WorkerRequest,value:unknown) {
  if (request.op !== "call" || request.name !== "compileLayers" || captures >= 12) return;
  const [source,width,height,options]=request.args as [string,number,number,Record<string,unknown>];
  if (options?.url !== "https://www.gov.uk/" || typeof source !== "string") return;
  const target=Deno.env.get("GOV_TRACE_DIR");
  if(!target)return;
  const compiled=value as {page?:{webRender?:Record<string,unknown>};layers?:Record<string,unknown>};
  const runs=(compiled.page?.webRender?.glyphRuns??[]) as {text:string;source:number;glyphs:number[][]}[];
  const heading=runs.findIndex((_,i)=>["The","best","place","to","find"].every((word,j)=>runs[i+j]?.text===word));
  const head=heading>=0?runs.slice(heading,heading+9).map(run=>({text:run.text,source:run.source,x:run.glyphs[0]?.[1],y:run.glyphs[0]?.[2]})):[];
  const key=target+"/frame-"+Deno.pid+"-"+(++captures)+".json";
  Deno.writeTextFileSync(key,JSON.stringify({id:request.id,source,width,height,options,head,
    layers:compiled.layers?{top:compiled.layers.top,bandTop:compiled.layers.bandTop}:undefined}));
}

const handle=async(request:WorkerRequest)=>{
  try{
    const start=performance.now();
    if(request.op==="init"){
      if(request.logAll)logGate.setAll(true);
      engine=loadHTML(request.nativeEngine);const e=await engine;
      if(request.font&&typeof (await loadFontFile(e,request.font.path,request.font.family))?.fonts==="number")
        fallbackFonts=fallbackFontHost(fonts=>loadFallbackFonts(e,fonts));
      scope.postMessage({id:request.id,ok:true,ms:performance.now()-start} satisfies WorkerReply);
      return;
    }
    if(request.op==="serifFont"||request.op==="monoFont"){
      if(!engine)throw new Error("engine worker was not initialised");
      const value=await loadFontFile(await engine,request.path,request.family,"bytes",request.op==="serifFont"?"serif":"mono");
      scope.postMessage({id:request.id,ok:true,value,ms:performance.now()-start} satisfies WorkerReply);
      return;
    }
    if(request.op==="pageFonts"){
      if(!fallbackFonts)throw new Error("this engine has no first font, or holds one font: no fallback fonts");
      const value=await fallbackFonts.page(request.source);
      scope.postMessage({id:request.id,ok:true,value,ms:performance.now()-start} satisfies WorkerReply);
      return;
    }
    if(request.op!=="call")return;
    if(!engine)throw new Error("engine worker was not initialised");
    if(!(REMOTE_CALLS as readonly string[]).includes(request.name))throw new Error(`Engine call ${request.name} is not available in the worker`);
    const e=await engine as unknown as Record<string,(...args:unknown[])=>unknown>;
    const measure=request.name==="compileLayers"||request.name==="compile";
    if(measure)e.frameWork(true);
    const started=performance.now();
    const value=e[request.name](...request.args);
    const took=performance.now()-started;
    recordGovHeader(request,value);
    if(measure){
      const layer=(value as {layers?:{bandTop:number;bandHeight:number}})?.layers;
      const work=e.frameWork();
      console.log(JSON.stringify({type:"native-html-worker-work",id:request.id,op:request.name,
        low:request.low??false,width:request.args[1],height:request.args[2],ms:Math.round(took*10)/10,
        band:layer?.bandTop,heightOfBand:layer?.bandHeight,work,inputs:renderInputChanges(request.args)}));
    }
    // The storage floats and tile words move to the main thread, not copied: one scene,
    // or the two layers. With a bytes answer they are views of one buffer, sent once.
    const scenes=[value,(value as {page?:unknown})?.page,(value as {chrome?:unknown})?.chrome] as (Partial<HTMLArtifact>|null|undefined)[];
    const buffers=new Set<ArrayBuffer>();
    for(const scene of scenes)for(const part of [scene?.data,scene?.tiles])
      if(part instanceof Float32Array||part instanceof Uint32Array)buffers.add(part.buffer as ArrayBuffer);
    scope.postMessage({id:request.id,ok:true,value,ms:performance.now()-start} satisfies WorkerReply,[...buffers]);
  }catch(error){
    scope.postMessage({id:request.id,ok:false,error:String(error instanceof Error?error.message:error)} satisfies WorkerReply);
  }
};
const queue=htmlQueue<WorkerRequest>();
let busy=false;
const drop=(request:WorkerRequest)=>scope.postMessage({id:request.id,ok:false,error:"dropped",dropped:true} satisfies WorkerReply);
const pump=async()=>{
  if(busy)return;
  busy=true;
  try{
    for(;;){
      // A Lean call holds this thread. Take in messages waiting as tasks before choosing
      // the next request, even with ordinary work queued: one of them may be input.
      await new Promise(resolve=>setTimeout(resolve,0));
      const next=queue.shift();
      if(!next)break;
      await handle(next);
    }
  }finally{busy=false;}
};
scope.onmessage=event=>{
  const request=event.data;
  if(request.op==="dropLow"){const low=queue.dropLow();if(low)drop(low);scope.postMessage({id:request.id,ok:true,ms:0} satisfies WorkerReply);return;}
  const dropped=queue.push(request);if(dropped)drop(dropped);
  pump();
};
