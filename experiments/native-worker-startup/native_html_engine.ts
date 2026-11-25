// Byte/JSON transport for the published Lean HTML engine. No host markup parser.
import type {NetWire} from "./native_net.ts";
import {allFinite} from "./finite_floats.ts";
// This ignored runtime is installed only after checking the Builds manifest.
// @ts-ignore generated release module
import createModule from "./.build/native-html/runtime/web-render.mjs";
import {traceBackends} from "../../../docs/web/hub/foafnaut/host-trace.mjs";

/** What a tab or scroll command needs: tab count and active tab; scroll, view height, scroll limit and screen scale. */
/** The answer of accessibilityTree: the nodes in tree order, or `unchanged` for the layout of `since`. */
export type AccessibilityAnswer={serial:number;top:number;scroll:number;unchanged?:boolean;
  nodes?:Record<string,unknown>[];announce?:{live:string;text:string}[]};
/** The answer of findInPage: matches, the current one from 0, and its rectangles [x,y,w,h] in page rows. */
/** What the desktop program reports to about:foafnaut: rows to show, and its build record. */
export type AboutHost={rows?:[string,string][];version?:string;commit?:string};
export type FindAnswer={count:number;current:number;rects:number[][]};
export type CommandState={tabs?:number;active?:number;scroll?:number;view?:number;scrollLimit?:number;scale?:number;zoomUnit?:number};
export type HTMLArtifact = {
  abi:string; width:number; height:number; data:number[]|Float32Array; wgsl:string; tiles:number[]|Uint32Array;
  primitiveCount:number; checks:{x:number;y:number;rgb:number[]}[];
  webRender:{links:unknown[][];[name:string]:unknown};
  /** In liberal mode, what Lean skipped to draw the page (WebAccept). */
  diagnostics?:{source:"System";severity:string;feature:string;where:string;action:string;message:string}[];
};
/** A render with `layers:true` (WebDocument.layersJSON): the chrome layer in window
rows, the page layer in band rows from page row `bandTop`, and the WGSL that puts them
in the window. `keepFrom`..`keepTo` are the scrolls that this band shows with no new render. */
/** The answer of fontFaces: the used faces and how many @font-face rules the page has. */
export type WebFontFaces={faces:{family:string;sources:string[]}[];rules:number};
export type HTMLLayerPlace = {top:number;view:number;bandTop:number;bandHeight:number;keepFrom:number;keepTo:number;composite:string;hoverRules?:boolean;scrollLimit?:number;
  /** WebPaint: an SVG animation runs or will begin by the clock (draw the next frame); the page has animations (send its clicks). */
  animating?:boolean;animations?:boolean;
  /** The splash (WebShell.splashNodes) is in this frame: ask for the next one. */
  splash?:boolean};
/** Lean's answer to a pointer press: the chrome control or the link pressed, and the rectangles the composite darkens. */
export type PressAnswer = {control:string|null;sourceNode?:number|null;href?:string;rects:number[][]};
/** A skip of liberal mode (WebAccept.Diagnostic.json): what Lean did not draw or run, and why. */
export type Diagnostic = {source:"System";severity:string;feature:string;where:string;action:string;message:string};
/** `wantsSerif`, `wantsMono`: the page's text resolves to serif, or to monospace, and the engine
holds no such face (serif_font.ts). */
export type HTMLLayers = {layers:HTMLLayerPlace;page:HTMLArtifact;chrome:HTMLArtifact;diagnostics?:Diagnostic[];wantsSerif?:boolean;wantsMono?:boolean};
export type Inspection = {
  baseURL:string;
  title:string;
  scripts:{kind:string;type:string;src:string;nodeId:number;url:string}[];
  stylesheets:{nodeId:number;url:string}[];
  /** Images that Lean wants (SVG `image`, HTML `img`), by store key; an older engine lists none for `img`. */
  images?:{key:string;url:string}[];
  /** The icon Lean chose for the tab (HTML §4.6.7.8), or null. */
  icon?:string|null;
  /** In liberal mode, what Lean skipped (none in strict mode). */
  diagnostics?:Diagnostic[];
};
/** A tab icon as Lean prepared it (WebDocument.iconPrepare). */
export type TabIcon={kind:"svg";source:string}|{kind:"bitmap";width:number;height:number;rgba:string};
export type History = {entries:string[];index:number};
/** The answer of a font load: the font's family and glyph count, and how many fonts the engine holds. */
export type FontLoaded = {family:string;glyphs:number;fonts:number};
export type HistoryAnswer = {history:History;url:string|null;canBack:boolean;canForward:boolean};
export type GraphFrame = {model:string;commands:string[]};
/** The address bar's edit state; the host keeps it and sends it back in `shell`. */
export type ShellEdit = {address:string;cursor:number;anchor:number;undo:unknown;redo:unknown;typing:boolean;menu?:boolean};
/** One button of the address menu (WebShell.menuActions): its rectangle in CSS px, and for copy the text. */
export type MenuAction = {action:"copy"|"paste";control:string;rect:[number,number,number,number];text?:string};
export type PrintLayout = {contentHeight:number;pages:[number,number][]};
export type WasmValue = {type:string;value:string;shown?:string};
export type WasmRequest = {wasmBase64:string;export?:string;args?:WasmValue[];fuel?:number};
export type WasmInfo = {engine:string;ops:string[];maxModuleBytes:number;defaultFuel:number;maxFuel:number;pageLimit:number;imports:string[]};
/** A run: the stage reached, and the values, trap or exception, with counts and time. */
export type WasmRun = {engine:string;bytes:number;stage:string;outcome:string;message?:string;values?:WasmValue[];
  stages?:{decode:number;validate:number;instantiate:number};exports?:{name:string;kind:string;params?:string[];results?:string[]}[];
  imports?:{module:string;name:string}[];instructions?:number;ns?:number;perSecond?:number;fuel?:number;prints?:string[]};
export type WasmSpecSample = {pass:number;fail:number;notRun:number;files:{name:string;pass:number;fail:number;notRun:number;ns:number;fails:string[]}[]};
/** An operator of a SPARQL plan, in execution order; `children` are earlier operators. */
export type SparqlOperator = {id:number;kind:string;label:string;why:string;children:number[];estimate:number|null;actual:number|null;ns:number};
export type SparqlCapabilityPlan = {bgp:number;family:number;approximate:boolean;cost:number;rows:number;note:string;
  steps:{source:string;args:string;inputs:string;estimatedCalls:number;estimatedRows:number;estimatedCost:number;rows:number}[]};
export type SparqlExplain = {ok:true;form:string;operators:SparqlOperator[];root:number;capability:SparqlCapabilityPlan[];
  capabilityWholeQuery:boolean;answer:string;ns:number;vars:string[];rows:Record<string,string|null>[];rowCount:number};
export type ShellGo = {go:"page";url:string}|{go:"system";url:string}|{go:"command";name:string;argument:string};
/** What a touch or a trackpad gesture means (WebGesture.lean, op gesture). */
export type GestureAnswer = {phase:"pending"|"swipe"|"other";direction:"back"|"forward"|null;progress:number;navigate:boolean;hint:number};
/** Where a link or an address goes (WebRoute.lean, docs/web/hub/foafnaut/link-route.mjs). */
export type LinkRoute = {route:"page";name:string;url:string}|{route:"graph";url:string}|{route:"navigate";url:string}|
  {route:"outside";url:string}|{route:"system";url:string}|{route:"command";name:string;argument:string}|{route:"refuse";url:string;reason:string};
export type HTMLResource = {nodeId:number;url:string;source:string};
/** One turn of a script session (WebScripts.turnAnswer). `commands` is the whole command
list, given only when `changed`: a host lays the page out again only then. */
/** What a page script setting means for a page (WebRenderScript.Plan). */
export type ScriptPlan={engine:string;name:string;run:boolean;marker:string;notice:string};
export type ScriptTurn = {session:number;clock:number;changed:boolean;commandCount:number;commands?:unknown[];
  /** The values of the page's running animations and transitions at this turn: [node, longhand, computed text, isTransition]. */
  animated?:[number,string,string,boolean][];
  navigations?:{nodeId:number;url:string}[];frameLoads?:number;
  /** A navigation of the page itself that Lean planned (a form's submission): the URL, the
   * method, and for POST the body and its type; target `_blank` for a new tab. Said once. */
  navigate?:{url:string;method:"get"|"post";body?:string;contentType?:string;target?:string};
  /** Requests the page asked for (XMLHttpRequest): the policy is the engine's; the host only makes them. */
  netRequests?:NetWire[];
  netCancels?:number[];
  /** A sync request: the turn changed nothing; answer it with action `syncAnswer` and the turn comes again. */
  netSync?:NetWire;
  logs:string[];errors:string[];timers:number;nextTimer:number|null;frames:number;nextWake:number|null;quiet:boolean;
  /** The page's start stopped at its step budget (`sliceSteps`): the rest is due at once. */
  startMore?:boolean;
  instructions:number;jobs:number;tasks:number;ns:number;layouts?:number;reads?:number;readOps?:string;
  /** Lean-validated page GPU commands of this turn (L4Factoidal.PageGpu) and their page session. */
  gpu?:unknown[];gpuPage?:number;
  /** Action `key`: whether the host may scroll for the key (its keydown was not canceled and
   * went to no text control or editing host; WebScripts `key`). */
  keyDefault?:boolean;
  /** BubblePopJS dedicated workers: how many the page has, and the scripts they wait for
   * (answered with the action `fetched`; docs/designissues/2026-11-09-dedicated-workers.md). */
  workers?:number;fetches?:{id:number;url:string;kind:string}[]};
type Module = {ccall(name:string,result:string|null,types:string[],values:unknown[]):number;
  UTF8ToString(pointer:number):string;HEAPU8:Uint8Array;_malloc?(size:number):number;_free?(pointer:number):void};
const encoder = new TextEncoder();
// One HTML document or stylesheet; the same limit as WebRender.maxSourceBytes.
export const MAX_SOURCE_BYTES = 16*1048576;
export function sourceBound(source:string) {
  if(source.includes("\0") || encoder.encode(source).length>MAX_SOURCE_BYTES)
    throw new Error("HTML/CSS input contains NUL or exceeds 16 MiB");
}
/** One call into Lean's document engine: HTML text, a JSON request, a viewport; a JSON answer. */
export type DocumentBackend=(html:string,requestJSON:string,width:number,height:number)=>string;
/** The same call with a bytes answer (`web_document_call_bin`, WebDocument.packAnswer):
a JSON head and raw sections, with no Base64. The buffer is the host's own copy. */
export type BytesBackend=(html:string,requestJSON:string,width:number,height:number)=>ArrayBuffer;
/** A font file as bytes (`web_document_font_call_bin`, WebDocument.fontLoadBin): no Base64
and no JSON, so the file is not copied onto the call stack. The answer is the fontLoad JSON. */
/** `fallback`: "mono" holds the monospace face (mode 4, WebDocument.loadMonoFont), "serif" the
serif face (3, WebDocument.loadSerifFont), "web" a web font (2), true a fallback font (1), false
replaces the held list (0). */
export type FontBackend=(bytes:Uint8Array,family:string,sha256:string,fallback:boolean|"web"|"serif"|"mono")=>string;
const fontMode=(fallback:boolean|"web"|"serif"|"mono")=>fallback==="mono"?4:fallback==="serif"?3:fallback==="web"?2:fallback?1:0;
/** An image as bytes (`web_document_image_call_bin`, WebDocument.imageLoadBin), held by key
and SHA-256; undefined when the engine has no such export. The answer is the imageLoad JSON. */
export type ImageBackend=(bytes:Uint8Array,key:string,sha256:string)=>string;
/** A page's bytes as text, decoded by Lean (`web_document_decode_call_bin`, WebDocument.decodeBin:
HTML encoding sniffing and the Encoding Standard's decoders), given the HTTP charset label
("" for none); undefined when the engine has no such export. The answer is the encoding's
name, a line feed and the text. */
export type DecodeBackend=(bytes:Uint8Array,charset:string,fallback:string,locale:string)=>string;
type LinkPicker=(text:string,width:number,height:number,x:number,y:number)=>string;
type Backends={text:DocumentBackend;bytes:BytesBackend;font:FontBackend;image?:ImageBackend;decode?:DecodeBackend;hit?:LinkPicker};
/** The answer of `imageInfo`: the engine holds images (WebDocument, issue 1292). */
export type ImageInfo={engine:string;ops:string[];maxImages:number;maxBytes:number;held:number;layoutSlots:number};
/** The answer of `frameWork`: layouts, kept layouts used and pointer states painted with no layout. */
export type FrameWork={layouts:number;kept:number;repaints:number;layoutSlots:number;pagesMade?:number;pagesKept?:number;paintOnly?:number;recompiled?:number;reused?:number;moved?:number};
/** Backend 2: a native dylib of the same Lean objects. Every call must come from one thread; no nonblocking FFI. */
export function nativeBackends(path:string):Backends {
  const library=Deno.dlopen(path,{
    web_document_call:{parameters:["buffer","buffer","u32","u32"],result:"pointer"},
    web_document_call_bin:{parameters:["buffer","buffer","u32","u32","buffer"],result:"pointer"},
    web_document_font_call_bin:{parameters:["buffer","u32","buffer","buffer","u32"],result:"pointer"},
    // An engine from before held images has no such symbol (issue 1274): it stays null.
    web_document_image_call_bin:{parameters:["buffer","u32","buffer","buffer"],result:"pointer",optional:true},
    // An engine from before Lean decoded pages has no such symbol: it stays null.
    web_document_decode_call_bin:{parameters:["buffer","u32","buffer"],result:"pointer",optional:true},
    // With the user's default for undeclared pages and the system's language (WebDocument.decodeBinWith).
    web_document_decode2_call_bin:{parameters:["buffer","u32","buffer","buffer","buffer"],result:"pointer",optional:true},
    web_render_hit:{parameters:["buffer","u32","u32","f64","f64"],result:"pointer",optional:true},
    web_render_free:{parameters:["pointer"],result:"void"},
  } as const);
  const cstring=(text:string)=>{if(text.includes("\0"))throw new Error("Native engine input contains NUL");return encoder.encode(text+"\0");};
  const size=new Uint32Array(1);
  const hit=library.symbols.web_render_hit;
  return {
    hit:hit?(text,width,height,x,y)=>{
      const pointer=hit(cstring(text),width,height,x,y);
      if(!pointer)throw new Error("Published Lean HTML engine allocation failed");
      try{return new Deno.UnsafePointerView(pointer).getCString();}
      finally{library.symbols.web_render_free(pointer);}
    }:undefined,
    text:(html,request,width,height)=>{
      const pointer=library.symbols.web_document_call(cstring(html),cstring(request),width,height);
      if(!pointer)throw new Error("Published Lean HTML engine allocation failed");
      try{return new Deno.UnsafePointerView(pointer).getCString();}
      finally{library.symbols.web_render_free(pointer);}
    },
    bytes:(html,request,width,height)=>{
      const pointer=library.symbols.web_document_call_bin(cstring(html),cstring(request),width,height,size);
      if(!pointer)throw new Error("Published Lean HTML engine allocation failed");
      // One copy out of the engine's memory; the engine frees its buffer.
      try{return Deno.UnsafePointerView.getArrayBuffer(pointer,size[0]).slice(0);}
      finally{library.symbols.web_render_free(pointer);}
    },
    font:(bytes,family,sha256,fallback)=>{
      const pointer=library.symbols.web_document_font_call_bin(bytes,bytes.length,cstring(family),cstring(sha256),fontMode(fallback));
      if(!pointer)throw new Error("Published Lean HTML engine allocation failed");
      try{return new Deno.UnsafePointerView(pointer).getCString();}
      finally{library.symbols.web_render_free(pointer);}
    },
    image:library.symbols.web_document_image_call_bin?(bytes,key,sha256)=>{
      const pointer=library.symbols.web_document_image_call_bin!(bytes,bytes.length,cstring(key),cstring(sha256));
      if(!pointer)throw new Error("Published Lean HTML engine allocation failed");
      try{return new Deno.UnsafePointerView(pointer).getCString();}
      finally{library.symbols.web_render_free(pointer);}
    }:undefined,
    decode:library.symbols.web_document_decode2_call_bin||library.symbols.web_document_decode_call_bin?(bytes,charset,fallback,locale)=>{
      const pointer=library.symbols.web_document_decode2_call_bin
        ?library.symbols.web_document_decode2_call_bin(bytes,bytes.length,cstring(charset),cstring(fallback),cstring(locale))
        :library.symbols.web_document_decode_call_bin!(bytes,bytes.length,cstring(charset));
      if(!pointer)throw new Error("Published Lean HTML engine allocation failed");
      try{return new Deno.UnsafePointerView(pointer).getCString();}
      finally{library.symbols.web_render_free(pointer);}
    }:undefined,
  };
}
export function nativeBackend(path:string):DocumentBackend {return nativeBackends(path).text;}
/** Backend 1: the Wasm module. */
function wasmBackends(module:Module):Backends & {hit:LinkPicker} {
  const callDocument=(name:string,html:string,request:string,width:number,height:number,extra:number[]=[])=>{
    const args=[width,height,...extra],numeric=args.map(()=>"number");
    if(html.length+request.length<=512*1024)
      return module.ccall(name,"number",["string","string",...numeric],[html,request,...args]);

    // ccall copies string arguments onto the Wasm stack. EPUB archives and
    // image-bearing reader pages can exceed that stack even within source limits.
    if(!module._malloc||!module._free)throw new Error("Published Lean HTML engine has no heap allocator");
    const source=encoder.encode(html),options=encoder.encode(request);
    const input=module._malloc(source.length+options.length+2);
    if(!input)throw new Error("Published Lean HTML engine allocation failed");
    try{
      const requestAt=input+source.length+1,heap=module.HEAPU8;
      heap.set(source,input);
      heap[requestAt-1]=0;
      heap.set(options,requestAt);
      heap[requestAt+options.length]=0;
      return module.ccall(name,"number",["number","number",...numeric],[input,requestAt,...args]);
    }finally{module._free(input);}
  };
  return {
    hit:(text,width,height,x,y)=>{
      const pointer=module.ccall("web_render_hit","number",["string","number","number","number","number"],[text,width,height,x,y]);
      if(!pointer)throw new Error("Published Lean HTML engine allocation failed");
      try{return module.UTF8ToString(pointer);}
      finally{module.ccall("web_render_free",null,["number"],[pointer]);}
    },
    text:(html,request,width,height)=>{
      const pointer=callDocument("web_document_call",html,request,width,height);
      if(!pointer)throw new Error("Published Lean HTML engine allocation failed");
      try{return module.UTF8ToString(pointer);}
      finally{module.ccall("web_render_free",null,["number"],[pointer]);}
    },
    bytes:(html,request,width,height)=>{
      const pointer=callDocument("web_document_call_bin",html,request,width,height,[0]);
      if(!pointer)throw new Error("Published Lean HTML engine allocation failed");
      // The first word is the total length. One copy out of the Wasm memory.
      try{const heap=module.HEAPU8,total=new DataView(heap.buffer,heap.byteOffset+pointer,4).getUint32(0,true);
        return heap.slice(pointer,pointer+total).buffer;}
      finally{module.ccall("web_render_free",null,["number"],[pointer]);}
    },
    font:(bytes,family,sha256,fallback)=>{
      if(!module._malloc||!module._free)throw new Error("Published Lean HTML engine has no font bytes call");
      // The file goes into the engine's heap, not onto its 4 MB stack.
      const input=module._malloc(Math.max(1,bytes.length));
      if(!input)throw new Error("Published Lean HTML engine allocation failed");
      try{
        module.HEAPU8.set(bytes,input);
        const pointer=module.ccall("web_document_font_call_bin","number",["number","number","string","string","number"],[input,bytes.length,family,sha256,fontMode(fallback)]);
        if(!pointer)throw new Error("Published Lean HTML engine allocation failed");
        try{return module.UTF8ToString(pointer);}
        finally{module.ccall("web_render_free",null,["number"],[pointer]);}
      }finally{module._free(input);}
    },
    // An engine from before held images has no such export (issue 1274).
    image:typeof (module as unknown as Record<string,unknown>)._web_document_image_call_bin==="function"&&module._malloc&&module._free?(bytes,key,sha256)=>{
      const input=module._malloc!(Math.max(1,bytes.length));
      if(!input)throw new Error("Published Lean HTML engine allocation failed");
      try{
        module.HEAPU8.set(bytes,input);
        const pointer=module.ccall("web_document_image_call_bin","number",["number","number","string","string"],[input,bytes.length,key,sha256]);
        if(!pointer)throw new Error("Published Lean HTML engine allocation failed");
        try{return module.UTF8ToString(pointer);}
        finally{module.ccall("web_render_free",null,["number"],[pointer]);}
      }finally{module._free!(input);}
    }:undefined,
    decode:typeof (module as unknown as Record<string,unknown>)._web_document_decode_call_bin==="function"&&module._malloc&&module._free?(bytes,charset,fallback,locale)=>{
      const two=typeof (module as unknown as Record<string,unknown>)._web_document_decode2_call_bin==="function";
      const input=module._malloc!(Math.max(1,bytes.length));
      if(!input)throw new Error("Published Lean HTML engine allocation failed");
      try{
        module.HEAPU8.set(bytes,input);
        const pointer=two
          ?module.ccall("web_document_decode2_call_bin","number",["number","number","string","string","string"],[input,bytes.length,charset,fallback,locale])
          :module.ccall("web_document_decode_call_bin","number",["number","number","string"],[input,bytes.length,charset]);
        if(!pointer)throw new Error("Published Lean HTML engine allocation failed");
        try{return module.UTF8ToString(pointer);}
        finally{module.ccall("web_render_free",null,["number"],[pointer]);}
      }finally{module._free!(input);}
    }:undefined,
  };
}
const decoder=new TextDecoder();
/** Read a bytes answer (WebDocument.packAnswer): the JSON head, and for each section its
byte offset and length in `buffer`. Every section starts at a multiple of 4 bytes. */
export function unpackAnswer(buffer:ArrayBuffer):{head:Record<string,unknown>;sections:[number,number][]} {
  const view=new DataView(buffer);
  if(buffer.byteLength<12||view.getUint32(0,true)!==buffer.byteLength)throw new Error("Unexpected Lean bytes answer length");
  const headSize=view.getUint32(4,true),count=view.getUint32(8,true);
  let offset=12+4*count;
  const head=JSON.parse(decoder.decode(new Uint8Array(buffer,offset,headSize)));
  offset+=headSize;
  const sections:[number,number][]=[];
  for(let i=0;i<count;i++){
    const length=view.getUint32(12+4*i,true);
    if(offset+length>buffer.byteLength)throw new Error("Lean bytes answer section out of range");
    sections.push([offset,length]);offset+=(length+3)&~3;
  }
  return {head,sections};
}
/** Put the sections that a scene names in place: storage floats as a Float32Array and
tile words as a Uint32Array, views of the one buffer, with no copy. */
function placeSections(scene:Record<string,unknown>,buffer:ArrayBuffer,sections:[number,number][]) {
  const at=(key:string)=>{
    const k=scene[key];if(typeof k!=="number")return undefined;
    const s=sections[k];if(!s||s[1]%4)throw new Error("Unexpected Lean bytes answer section");
    delete scene[key];return s;
  };
  const data=at("dataSection"),tiles=at("tilesSection");
  if(data)scene.data=new Float32Array(buffer,data[0],data[1]/4);
  if(tiles)scene.tiles=new Uint32Array(buffer,tiles[0],tiles[1]/4);
}
/** Lean sends the storage floats as the bytes the GPU reads; this only decodes and checks them. */
function sceneOf(result:Record<string,unknown>&{dataBase64?:unknown},width:number,height:number):HTMLArtifact {
  if(typeof result.dataBase64==="string"){
    const text=atob(result.dataBase64),bytes=new Uint8Array(text.length);
    for(let i=0;i<text.length;i++)bytes[i]=text.charCodeAt(i);
    result.data=new Float32Array(bytes.buffer);delete result.dataBase64;
  }
  const data=result.data as number[]|Float32Array,web=result.webRender as {links?:unknown}|undefined;
  if(result.abi!=="lean-svg-v1" || result.width!==width || result.height!==height ||
     !(Array.isArray(data)||data instanceof Float32Array) || !data.length || !allFinite(data) ||
     typeof result.wgsl!=="string" || !Array.isArray(result.checks) || !Array.isArray(web?.links))
    throw new Error("Unexpected published Lean HTML scene ABI");
  return result as unknown as HTMLArtifact;
}
/** `answers:"bytes"` (the default) takes render answers as bytes with raw sections;
`"text"` takes the JSON text with Base64, the reference that tests compare with. */
type LinkTarget = {href:string;sourceNode:number};
type LinkChunk = {text:string;start:number;end:number;top:number;bottom:number};
const linkChunkLimit=512*1024;
const pressFragmentCount=8; // WebDocument.maxPressRects
const linkWire=new WeakMap<unknown[],LinkChunk[]>();

/** Keep the common single-payload path. Larger pages use contiguous, bounded
 * chunks so Lean can pick in reverse paint order without increasing its input limit. */
export function linkChunks(links:unknown[]):LinkChunk[] {
  const kept=linkWire.get(links);
  if(kept)return kept;
  const full=JSON.stringify(links);
  if(encoder.encode(full).length<=linkChunkLimit) {
    const one=[{text:full,start:0,end:links.length,top:-Infinity,bottom:Infinity}];
    linkWire.set(links,one);
    return one;
  }
  const chunks:LinkChunk[]=[];
  let start=0,bytes=2,top=Infinity,bottom=-Infinity;
  let rows:string[]=[];
  const flush=(end:number)=>{
    if(!rows.length)return;
    chunks.push({text:"["+rows.join(",")+"]",start,end,top,bottom});
    rows=[];start=end;bytes=2;top=Infinity;bottom=-Infinity;
  };
  for(const [index,row] of links.entries()){
    const encoded=JSON.stringify(row);
    const size=encoder.encode(encoded).length;
    if(bytes+size+(rows.length?1:0)>linkChunkLimit)flush(index);
    rows.push(encoded);
    bytes+=size+(rows.length>1?1:0);
    const y=Array.isArray(row)?row[3]:undefined,h=Array.isArray(row)?row[5]:undefined;
    // Do not exclude a malformed row here. The Lean decoder remains authoritative.
    if(typeof y==="number"&&typeof h==="number"&&Math.abs(y)<2**31&&h>=0&&h<2**31){
      top=Math.min(top,Math.floor(y)-1);bottom=Math.max(bottom,Math.ceil(y+h)+1);
    }else {top=-Infinity;bottom=Infinity;}
  }
  flush(links.length);
  linkWire.set(links,chunks);
  return chunks;
}

export function pickLinkChunk(chunks:LinkChunk[],row:number,pick:(text:string)=>LinkTarget|null) {
  for(let i=chunks.length-1;i>=0;i--){
    const chunk=chunks[i];
    if(row<chunk.top||row>=chunk.bottom)continue;
    const target=pick(chunk.text);
    if(target)return {target,chunk};
  }
  return null;
}

/** The winning chunk supplies the target. Earlier or later fragments of that
 * source supply the same press highlight rectangles as the full link list. */
export function pressLinksText(links:unknown[],chunk:LinkChunk,sourceNode:number):string {
  const before:string[]=[],after:string[]=[];
  let fragments=0;
  for(const [index,row] of links.entries()){
    if(!Array.isArray(row)||row[0]!==sourceNode)continue;
    if(index<chunk.start)before.push(JSON.stringify(row));
    else if(index>=chunk.end)after.push(JSON.stringify(row));
    if(++fragments===pressFragmentCount)break;
  }
  const chunks=[...before,chunk.text.slice(1,-1),...after].filter(Boolean);
  return "["+chunks.join(",")+"]";
}
/** Test mode: with FOAFNAUT_HOST_TRACE set to a file, every engine call adds one JSON line to it
(docs/web/hub/foafnaut/host-trace.mjs; checked by host_contract_check.ts against the host contract).
Unset, or with no permission to read the environment (the compiled app), the backends are returned
as they are and nothing is recorded. */
function hostTrace(backends:Backends):Backends {
  let path:string|undefined;
  try{path=Deno.env.get("FOAFNAUT_HOST_TRACE");}catch{return backends;}
  if(!path)return backends;
  const file=path,encode=new TextEncoder();
  let warned=false;
  return traceBackends(backends,(line:unknown)=>{
    try{Deno.writeFileSync(file,encode.encode(JSON.stringify(line)+"\n"),{append:true});}
    catch(error){if(!warned){warned=true;console.error(`host trace: not written to ${file}: ${error}`);}}
  }) as Backends;
}
export async function loadHTML(nativeEngine?:string,answers:"bytes"|"text"="bytes") {
  const native=nativeEngine?nativeBackends(nativeEngine):undefined;
  // Older native libraries can still use the Wasm link picker. Current ones
  // provide the same C entry point and need no second document engine.
  const wasm=native?.hit?undefined:wasmBackends(await createModule() as unknown as Module);
  const backends=hostTrace(native??wasm!);
  const backend=backends.text;
  const hit=native?.hit??wasm!.hit;
  const pickLinks=(text:string,width:number,height:number,x:number,y:number):LinkTarget|null=>{
    const result=JSON.parse(hit(text,width,height,x,y));
    if(result?.error)throw new Error(`Lean HTML: ${result.error}`);
    return result;
  };
  // Bytes of JSON request sent to Lean for renders: the last one and the most (frame_work_test.ts).
  const sent={renders:0,lastRenderBytes:0,maxRenderBytes:0};
  const countRender=(request:string)=>{
    const n=encoder.encode(request).length;
    sent.renders++;sent.lastRenderBytes=n;sent.maxRenderBytes=Math.max(sent.maxRenderBytes,n);
    return n;
  };
  const documentCall=(source:string,options:Record<string,unknown>,width=1,height=1)=>{
    sourceBound(source);
    if(![width,height].every(n=>Number.isInteger(n)&&n>0&&n<=4096))
      throw new Error("Native HTML viewport must be 1..4096 backing pixels");
    const request=JSON.stringify(options);
    if(options.op==="render")countRender(request);
    if(encoder.encode(request).length>20971520)throw new Error("Document request exceeds 20 MiB");
    const result=JSON.parse(backend(source,request,width,height));
    if(result?.error)throw new Error(`Lean HTML: ${result.error}`);
    return result;
  };
  /** A render through the bytes answer; the scenes get their sections as views. */
  const renderCall=(source:string,options:Record<string,unknown>,width:number,height:number)=>{
    // Decimal floats (binary:false) are a text answer only.
    if(answers==="text"||options.binary===false)return documentCall(source,options,width,height);
    sourceBound(source);
    if(![width,height].every(n=>Number.isInteger(n)&&n>0&&n<=4096))
      throw new Error("Native HTML viewport must be 1..4096 backing pixels");
    const request=JSON.stringify(options);
    if(countRender(request)>20971520)throw new Error("Document request exceeds 20 MiB");
    const buffer=backends.bytes(source,request,width,height);
    const {head,sections}=unpackAnswer(buffer);
    if(head?.error)throw new Error(`Lean HTML: ${head.error}`);
    for(const scene of [head,head.page,head.chrome])
      if(scene&&typeof scene==="object")placeSections(scene as Record<string,unknown>,buffer,sections);
    return head;
  };
  return {
    xmlStylesheet:(source:string,options:Record<string,unknown>)=>documentCall(source,{...options,op:"xmlStylesheet"}) as {url:string|null},
    xslt:(source:string,options:Record<string,unknown>)=>documentCall(source,{...options,op:"xslt"}) as {source:string;engine:string},
    inspect:(source:string,options:Record<string,unknown>)=>documentCall(source,{...options,op:"inspect"}) as Inspection,
    // Lean reads the font once and holds it; later renders draw with it.
    // fallback:true adds the font to the engine's list, after the fonts it holds;
    // otherwise the font replaces the list. The answer counts the fonts held.
    fontLoad:(fontBase64:string,fontFamily:string,fontSha256:string,fallback:boolean|"serif"|"mono"=false)=>
      documentCall("",{op:"fontLoad",fontBase64,fontFamily,fontSha256,...(fallback==="serif"?{serif:true}:fallback==="mono"?{mono:true}:fallback?{fallback:true}:{})}) as FontLoaded,
    // The same, with the file as bytes: no Base64, and no size limit from the call stack.
    // fallback:"serif" holds the serif face, which draws the text whose family resolves to
    // serif (FontFaceRule.genericOf); a host gives it when a render answers wantsSerif.
    // fallback:"mono" holds the monospace face, likewise for monospace text and wantsMono.
    fontLoadBytes:(bytes:Uint8Array,fontFamily:string,fontSha256:string,fallback:boolean|"serif"|"mono"=false)=>{
      const result=JSON.parse(backends.font(bytes,fontFamily,fontSha256,fallback));
      if(result?.error)throw new Error(`Lean HTML: ${result.error}`);
      return result as FontLoaded;
    },
    fontRequests:(source:string,options:Record<string,unknown>)=>documentCall(source,{...options,op:"fontRequests"}),
    // Web fonts (CSS Fonts 4 §4, WebDocument.fontFaces): the @font-face faces the page's
    // rendered text uses, each with its URLs to try in order; then each fetched face goes
    // in with webFontLoad (Lean checks it with the font policy and holds it by SHA-256).
    fontFaces:(source:string,options:Record<string,unknown>)=>documentCall(source,{...options,op:"fontFaces"}) as WebFontFaces,
    webFontLoad:(bytes:Uint8Array,fontSha256:string)=>{
      const result=JSON.parse(backends.font(bytes,"",fontSha256,"web"));
      if(result?.error)throw new Error(`Lean HTML: ${result.error}`);
      return result as {webFont:string;glyphs:number;held:number};
    },
    // One step of a subresource transfer (WebDocument op `subresource`, Net.Subresource): the
    // request the host makes next, or what is used, or the refusal. An engine from before it
    // throws "unknown document operation".
    subresource:(request:Record<string,unknown>)=>documentCall("",{...request,op:"subresource"}),
    // Held images (WebDocument, issue 1292): sent once, named by renders in `heldImages`.
    // `imageInfo` answers undefined for an engine from before them, which then gets
    // `images` with the bytes in each request, as before (issue 1274).
    imageInfo:():ImageInfo|undefined=>{
      try{const info=documentCall("",{op:"imageInfo"}) as ImageInfo;return Array.isArray(info?.ops)&&info.ops.includes("imageLoad")?info:undefined;}
      catch{return undefined;}
    },
    /** The page's bytes as text, decoded by Lean (HTML encoding sniffing, the Encoding
    Standard's decoders); undefined for an engine from before (the host then reads UTF-8). */
    /** The setting for pages that declare no encoding, as Lean stores it (WebState.encodingSetting),
    and the settings page section for it; undefined for an engine from before. */
    encodingSetting:(setting:string)=>{try{return (documentCall("",{op:"encodingSetting",setting}) as {setting:string}).setting;}catch{return undefined;}},
    encodingChoices:(setting:string,locale:string)=>{try{return (documentCall("",{op:"encodingChoices",setting,locale}) as {html:string}).html;}catch{return undefined;}},
    /** The search engine chosen in Settings, as Lean keeps it (WebRoute.searchSetting: "" for
    none), the settings section for it, the browser's search page for typed words, and the
    Outside page; undefined for an engine from before (the feature is then off). */
    searchSetting:(setting:string)=>{try{return documentCall("",{op:"searchSetting",setting}) as {setting:string;name:string};}catch{return undefined;}},
    searchChoices:(setting:string)=>{try{return (documentCall("",{op:"searchChoices",setting}) as {html:string}).html;}catch{return undefined;}},
    searchPage:(request:{argument:string;tabs:{url:string;title:string}[];resources:unknown[];state:boolean;search:string})=>
      documentCall("",{...request,op:"searchPage"}) as {title:string;source:string},
    outsidePage:(url:string,hub=false,textnaut=false)=>{try{return documentCall("",{op:"outsidePage",url,hub,textnaut}) as {title:string;source:string};}catch{return undefined;}},
    /** What a navigation's response does (WebDocument op `download`, Net.Subresource.navigated):
    shown, or saved under the name Lean made safe. Undefined for an engine from before the op
    (every response is then shown, as before). */
    /** The browser's cookies for page loads (WebDocument op `cookies`, Net.Cookies): the jar is
    text the host keeps; `request` gives a hop's Cookie field, `response` the jar after its
    Set-Cookie fields, `keep` the part that may be written to disk. Undefined for an engine from
    before the op (page loads then carry no cookies, as before). */
    cookies:(request:{action:"request"|"response"|"keep";jar:string;now:string;url?:string;initiator?:string;method?:string;setCookie?:string})=>{
      try{return documentCall("",{...request,op:"cookies"}) as {cookie?:string;jar?:string;error?:string};}catch{return undefined;}},
    download:(request:{contentType:string;disposition:string;url:string})=>{
      try{return documentCall("",{...request,op:"download"}) as {action:"show"}|{action:"save";name:string};}catch{return undefined;}},
    epubReader:(bytes:Uint8Array,epubChapter:number)=>{
      let text="";
      for(let i=0;i<bytes.length;i+=32768)text+=String.fromCharCode(...bytes.subarray(i,i+32768));
      return documentCall(btoa(text),{op:"epubReader",epubChapter}) as {source:string};
    },
    decodeDocument:(bytes:Uint8Array,charset="",fallback="",locale="")=>{
      if(!backends.decode)return undefined;
      const answer=backends.decode(bytes,charset,fallback,locale),i=answer.indexOf("\n");
      return {encoding:answer.slice(0,i),source:answer.slice(i+1)};
    },
    imageLoad:(bytes:Uint8Array,key:string,sha256:string)=>{
      if(backends.image){
        const result=JSON.parse(backends.image(bytes,key,sha256));
        if(result?.error)throw new Error(`Lean HTML: ${result.error}`);
        return result as {key:string;sha256:string;bytes:number;held:number};
      }
      let text="";
      for(let i=0;i<bytes.length;i+=32768)text+=String.fromCharCode(...bytes.subarray(i,i+32768));
      return documentCall("",{op:"imageLoad",key,sha256,imageBase64:btoa(text)}) as {key:string;sha256:string;bytes:number;held:number};
    },
    imageDrop:()=>documentCall("",{op:"imageDrop"}) as {held:number},
    /** Lean's count of its frame work; undefined for an engine without it. */
    frameWork:(reset=false):FrameWork|undefined=>{
      try{return documentCall("",{op:"frameWork",...(reset?{reset:true}:{})}) as FrameWork;}catch{return undefined;}
    },
    /** Bytes of JSON request this host sent to Lean for renders. */
    requestBytes:()=>({...sent}),
    // The CSS declarations that Lean's profile can not read and drops, "property: value (reason)".
    droppedCSS:(source:string,options:Record<string,unknown>)=>(documentCall(source,{...options,op:"droppedCSS"}) as {dropped:string[]}).dropped,
    compile(source:string,width:number,height:number,options:Record<string,unknown>):HTMLArtifact {
      return sceneOf(renderCall(source,{binary:true,...options,op:"render"},width,height),width,height);
    },
    /** One render as two layers; the options must carry a shell. */
    compileLayers(source:string,width:number,height:number,options:Record<string,unknown>):HTMLLayers {
      const result=renderCall(source,{binary:true,...options,layers:true,op:"render"},width,height);
      const place=result.layers as HTMLLayerPlace|undefined;
      if(!place||!["top","view","bandTop","bandHeight","keepFrom","keepTo"].every(k=>Number.isSafeInteger((place as Record<string,unknown>)[k]))||typeof place.composite!=="string")
        throw new Error("Unexpected published Lean HTML layers ABI");
      const layers:HTMLLayers={layers:place,page:sceneOf(result.page,width,place.bandHeight),chrome:sceneOf(result.chrome,width,Math.max(1,place.top))};
      if(Array.isArray(result.diagnostics))layers.diagnostics=result.diagnostics as Diagnostic[];
      if(result.wantsSerif===true)layers.wantsSerif=true;
      if(result.wantsMono===true)layers.wantsMono=true;
      return layers;
    },
    // Lean decides what a chrome click, a key, an address and a link mean.
    shellHit:(shell:unknown,x:number,y:number,width:number)=>(documentCall("",{op:"shellHit",shell,x,y,width}) as {control:string|null}).control,
    // The control under a press, and whether this press opens the address menu (`how`: tap, hold or context).
    shellMenu:(shell:unknown,x:number,y:number,width:number,how:string,touch=false)=>
      documentCall("",{op:"shellHit",shell,x,y,width,how,touch}) as {control:string|null;menu?:boolean},
    // The address menu's buttons and the text Copy writes; empty with the menu closed.
    shellActions:(shell:unknown,width:number)=>(documentCall("",{op:"shellActions",shell,width}) as {actions:MenuAction[]}).actions,
    // A press: the control or the link under the pointer (`row` is the page-layer row) and what to darken.
    press(shell:unknown,x:number,y:number,width:number,row:number,links:unknown[]):PressAnswer {
      const pageRow=Math.max(0,Math.floor(row));
      const press=(linksText:string)=>documentCall("",{op:"press",shell,x,y,width,row:pageRow,linksText}) as PressAnswer;
      const chunks=linkChunks(links);
      if(chunks.length===1)return press(chunks[0].text);
      const chrome=press("[]");
      if(chrome.control||!Number.isFinite(pageRow))return chrome;
      const pressX=Number.isInteger(x)&&x>=0?x:0;
      // Press coordinates are natural page rows. The window hit operation checks
      // a viewport, while press may use any row of the retained page.
      const hit=pickLinkChunk(chunks,pageRow,text=>pickLinks(text,0xffffffff,0xffffffff,pressX,pageRow));
      return hit?press(pressLinksText(links,hit.chunk,hit.target.sourceNode)):chrome;
    },
    // The system pointer for a window point: "arrow", "hand" or "text" (issue 1268).
    pointerCursor(request:{shell:unknown;x:number;y:number;width:number;model?:string;links?:string;pageY?:number},
        regions?:unknown[]):string {
      let links=request.links;
      const row=request.pageY;
      if(regions&&row!==undefined){
        const chunks=linkChunks(regions);
        links=chunks.length===1?chunks[0].text:
          pickLinkChunk(chunks,row,text=>pickLinks(text,0xffffffff,0xffffffff,request.x,row))?.chunk.text;
      }
      return (documentCall("",{...request,op:"pointerCursor",links}) as {cursor:string}).cursor;
    },
    shellText:(shell:unknown,text:string)=>documentCall("",{op:"shellText",shell,text}) as ShellEdit,
    shellKey:(shell:unknown,key:number,modifiers=0)=>documentCall("",{op:"shellKey",shell,key,modifiers}) as ShellEdit,
    // Select all, copy, cut, paste, undo, redo and focus in the address bar; `clipboard` is the text to copy.
    shellEdit:(shell:unknown,action:string,text="")=>documentCall("",{op:"shellEdit",shell,action,text}) as ShellEdit&{clipboard?:string|null;go?:string|null},
    // Where the pages of a print layout break (`media:"print"` in the options).
    printLayout:(source:string,width:number,height:number,options:Record<string,unknown>)=>
      documentCall(source,{...options,op:"printLayout"},width,height) as PrintLayout,
    shellSubmit:(address:string)=>documentCall("",{op:"shellSubmit",address}) as ShellGo,
    // The FOAF graph page: the model is Lean's; the host keeps it as text.
    graphStart:(rdf:string,width:number,height:number,shell:unknown)=>documentCall("",{op:"graphStart",rdf,width,height,shell}) as GraphFrame,
    graphEvent:(model:string,kind:number,a:number,b:number,width:number,shell:unknown)=>documentCall("",{op:"graphEvent",model,kind,a,b,width,shell}) as GraphFrame,
    graphPage:(model:string)=>(documentCall("",{op:"graphPage",model}) as {source:string}).source,
    sourcePage:(kind:string,url:string,source:string)=>(documentCall("",{op:"sourcePage",kind,url,source}) as {source:string}).source,
    // WebAssembly run by WasmVM, Lean's engine, inside this engine (WebWasm.lean, issue 1244).
    // Modules are Base64 in the request; values use the spec-test JSON form.
    wasmInfo:()=>documentCall("",{op:"wasmInfo"}) as WasmInfo,
    wasmRun:(request:WasmRequest)=>documentCall("",{...request,op:"wasmRun"}) as WasmRun,
    wasmSpecSample:()=>documentCall("",{op:"wasmSpecSample"}) as WasmSpecSample,
    /** The page foafnaut:wasm, as HTML that Lean then lays out. */
    wasmPage:(request:Partial<WasmRequest>&{url?:string}={})=>documentCall("",{...request,op:"wasmPage"}) as {source:string;title:string},
    // The SPARQL planner drawn as live debug (WebSparql.lean). An older engine answers
    // "unknown document operation".
    sparqlInfo:()=>documentCall("",{op:"sparqlInfo"}) as {engine:string;ops:string[];datasets:string[];examples:{name:string;query:string}[]},
    sparqlExplain:(request:{query:string;dataset?:string;data?:string;run?:boolean})=>documentCall("",{...request,op:"sparqlExplain"}) as SparqlExplain,
    /** The page foafnaut:sparql; `argument` is the address after `foafnaut:sparql/`. */
    sparqlPage:(argument:string)=>documentCall("",{op:"sparqlPage",argument}) as {source:string;title:string;next:string},
    /** The console tab of a page (WebConsole): Lean writes the page from the entries the host kept. */
    consolePage:(request:Record<string,unknown>)=>documentCall("",{...request,op:"consolePage"}) as {source:string;title:string},
    shellLink:(href:string)=>documentCall("",{op:"shellLink",href}) as ShellGo,
    // The final action for a link (`href`) or a typed address (`address`). An older engine
    // answers "unknown document operation" (link-route.mjs then answers instead).
    shellRoute:(request:Record<string,unknown>)=>documentCall("",{...request,op:"shellRoute"}) as LinkRoute,
    // A back or forward swipe (WebGesture.lean): `action` info, touch or wheel. An older engine
    // answers "unknown document operation"; a host then has no swipes.
    gesture:(request:Record<string,unknown>)=>documentCall("",{...request,op:"gesture"}) as GestureAnswer,
    // Browser state (WebState.lean): bookmarks, history, settings and tabs as LWS resources.
    state:(op:string,request:Record<string,unknown>={})=>documentCall("",{...request,op}),
    // Page scripts run by Lean (WebScripts.lean): QuickJS-NG in WasmVM on the page's arena,
    // the Lean event loop deciding each callback. An older engine answers "unknown document
    // operation" to scriptInfo; a host then keeps refusing scripted pages (issue 1274).
    scriptInfo:()=>documentCall("",{op:"scriptSession",action:"info"}) as {ops:string[];module:boolean;bytes:number;engine:string;engines?:string[]},
    // The page script setting (WebRenderScript.plan): Lean says what a setting means on a host
    // ("native" or "hub"): the engine, whether the scripts run, the chrome marker, a notice.
    scriptSetting:(setting:string)=>documentCall("",{op:"scriptSetting",setting}) as {setting:string;name:string},
    scriptPlan:(request:{setting:string;scripts:number;host?:string;unavailable?:string;failure?:string})=>
      documentCall("",{...request,op:"scriptPlan"}) as ScriptPlan,
    /** The settings page's rows of the engines, the current one ticked. */
    scriptChoices:(setting:string,host="native")=>(documentCall("",{op:"scriptChoices",setting,host}) as {html:string}).html,
    /** The guest module, as bytes through the font byte call (family `guest:quickjs`). */
    scriptLoad:(bytes:Uint8Array)=>{
      const result=JSON.parse(backends.font(bytes,"guest:quickjs","",false));
      if(result?.error)throw new Error(`Lean HTML: ${result.error}`);
      return result as {module:boolean;bytes:number};
    },
    scriptSession:(source:string,request:Record<string,unknown>)=>documentCall(source,{...request,op:"scriptSession"}) as ScriptTurn,
    /** The node under a window point, for a click that page scripts receive. */
    nodeAt:(source:string,width:number,height:number,options:Record<string,unknown>)=>
      (documentCall(source,{...options,op:"nodeAt"},width,height) as {node:number|null}).node,
    /** The node under a window point and the coordinates of its pointer events (WebHit). */
    pointerAt:(source:string,width:number,height:number,options:Record<string,unknown>)=>
      documentCall(source,{...options,op:"nodeAt"},width,height) as {node:number|null}&Record<string,number>,
    // Lean decides what a menu command and a pointer release mean.
    // `state` gives the tab count, the scroll and the view, from which Lean answers a tab or a scroll.
    command:(command:number,textScalePercent:number,history?:History,focused=false,state:CommandState={})=>documentCall("",{op:"command",command,textScalePercent,focused,...state,...(history?{history}:{})}) as
      {action:string;target?:"address"|"page";textScalePercent:number;tab?:number;scrollTo?:number;refused?:string}&Partial<HistoryAnswer>,
    // The settings page's text size (WebSelection.textZoom): the zoom for `zoom` (up, down,
    // reset, a percent; empty: no change) and the text size shown. An older engine answers
    // "unknown document operation".
    textZoom:(zoom:string,textScalePercent:number,zoomUnit=100)=>documentCall("",{op:"textZoom",zoom,textScalePercent,zoomUnit}) as
      {textScalePercent:number;shown:number;default:number;min:number;max:number;step:number;refused?:string},
    // The tab icon from the Base64 bytes of an icon resource, for a screen of `scale`.
    iconPrepare:(base64:string,scale:number)=>documentCall("",{op:"iconPrepare",base64,scale}) as TabIcon,
    // A key that the macOS menu did not take: the command of Lean's key table, or null.
    pageKey:(key:number,modifiers:number)=>(documentCall("",{op:"pageKey",key,modifiers}) as {command:number|null}).command,
    keyTable:(platform:string)=>documentCall("",{op:"keyTable",platform}) as {modifier:string;key:string;command:number}[],
    historyPush:(history:History,url:string)=>documentCall("",{op:"historyPush",history,url}) as HistoryAnswer,
    keyCommand:(platform:string,modifier:string,key:string)=>(documentCall("",{op:"keyCommand",platform,modifier,key}) as {command:number|null}).command,
    pointerUp:(selection:number[])=>(documentCall("",{op:"pointerUp",selection}) as {action:string}).action,
    selectedText:(source:string,width:number,height:number,options:Record<string,unknown>)=>
      (documentCall(source,{...options,op:"selectedText"},width,height) as {text:string}).text,
    // Find in page (WebSelection.findMatches): `options.find` is {query, current}. The count,
    // the current match (from 0) and its rectangles in page rows.
    findInPage:(source:string,width:number,height:number,options:Record<string,unknown>)=>
      documentCall(source,{...options,op:"findInPage"},width,height) as FindAnswer,
    // The accessibility tree of the page of a frame's request (HTML/AccessibleTree.lean): asked
    // only while assistive technology is attached. `options.since` is the `serial` of the last
    // answer: the engine then answers `unchanged` for the same layout and makes no tree.
    accessibilityTree:(source:string,width:number,height:number,options:Record<string,unknown>)=>
      documentCall(source,{...options,op:"accessibilityTree"},width,height) as AccessibilityAnswer,
    // about:foafnaut, written by the engine (WebAbout) from its own build facts; `host` is
    // what this program reports, which the page shows as reported and does not check.
    aboutPage:(host:AboutHost)=>(documentCall("",{op:"aboutPage",host}) as {source:string}).source,
    // The engine's own build facts (WebBuild), its --version line, and a line when `host`'s record disagrees.
    engineBuild:(host:AboutHost={})=>documentCall("",{op:"engineBuild",host}) as
      {version:string;commit:string;builtAt:string;dirty:boolean;release:boolean;line:string;mismatch?:string},
    // A key (macOS key code and modifier bits) or typed text in the find field (WebShell.findEdit).
    findEdit:(query:string,edit:{text?:string;key?:number;modifiers?:number})=>
      documentCall("",{op:"findEdit",query,...edit}) as {query:string;step:"none"|"next"|"previous"|"close"},
    hit(artifact:HTMLArtifact,x:number,y:number):{href:string;sourceNode:number}|null {
      if(!Number.isFinite(x)||!Number.isFinite(y))return null;
      const chunks=linkChunks(artifact.webRender.links);
      return pickLinkChunk(chunks,y,text=>pickLinks(text,artifact.width,artifact.height,x,y))?.target??null;
    },
  };
}
export type HTMLEngine = Awaited<ReturnType<typeof loadHTML>>;
