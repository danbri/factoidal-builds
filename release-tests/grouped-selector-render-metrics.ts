import {createHash} from "node:crypto";

const [library, inputPath, primary] = Deno.args;
const ffi = Deno.dlopen(library,{
  web_document_call:{parameters:["buffer","buffer","u32","u32"],result:"pointer"},
  web_document_call_bin:{parameters:["buffer","buffer","u32","u32","buffer"],result:"pointer"},
  web_render_free:{parameters:["pointer"],result:"void"},
} as const);
const encode = new TextEncoder();
const decode = new TextDecoder();
const z = (x:string)=>encode.encode(x+"\0");
const input = JSON.parse(await Deno.readTextFile(inputPath+"/input.json"));
const source=z(await Deno.readTextFile(inputPath+"/page.html"));
const height=800;
const request=(extra:Record<string,unknown>)=>z(JSON.stringify({url:input.url,
  liberal:true,partialNote:false,scripting:false,...extra}));
function call(fields:Record<string,unknown>) {
  const ptr=ffi.symbols.web_document_call(source,request(fields),input.width,height);
  if(!ptr)throw Error("No native response");
  try{
    const value=JSON.parse(new Deno.UnsafePointerView(ptr).getCString());
    if(value.error)throw Error(value.error);
    return value;
  }finally{
    ffi.symbols.web_render_free(ptr);
  }
}
const baseFont=await Deno.readFile(primary);
const baseSha=createHash("sha256").update(baseFont).digest("hex");
function base64(data:Uint8Array) {
  let s="";
  for(let i=0;i<data.length;i+=16_384)s+=String.fromCharCode(...data.subarray(i,i+16_384));
  return btoa(s);
}
const font=call({op:"fontLoad",fontFamily:"Noto Sans",fontSha256:baseSha,fontBase64:base64(baseFont)});
const inspect=call({op:"inspect"});
const resources=inspect.stylesheets.flatMap((sheet:{nodeId:number;url:string})=>
  Object.hasOwn(input.css,sheet.url)?[{nodeId:sheet.nodeId,url:sheet.url,source:input.css[sheet.url]}]:[]);
const misses=inspect.stylesheets.filter((sheet:{url:string})=>!Object.hasOwn(input.css,sheet.url)).map((sheet:{url:string})=>sheet.url);
const webFonts=[];
const refusedFonts:string[]=[];
for(const f of input.fonts as {url:string;sha256:string;base64:string}[]){
  try {
    call({op:"fontLoad",webFont:true,fontSha256:f.sha256,fontBase64:f.base64});
    webFonts.push({url:f.url,sha256:f.sha256});
  } catch {
    refusedFonts.push(f.url);
  }
}

for(const [index,width] of [input.width,input.width+1,input.width+2,input.width+3].entries()){
  call({op:"frameWork",reset:true});
  const options=request({op:"render",checks:false,resources,webFonts});
  const size=new Uint32Array(1);
  const start=performance.now();
  const ptr=ffi.symbols.web_document_call_bin(source,options,width,height,size);
  const ms=performance.now()-start;
  if(!ptr)throw Error("No native render");
  try{
    const buffer=Deno.UnsafePointerView.getArrayBuffer(ptr,size[0]);
    const header=new DataView(buffer);
    const length=header.getUint32(4,true), sections=header.getUint32(8,true);
    const from=12+4*sections;
    const meta=JSON.parse(decode.decode(new Uint8Array(buffer,from,length)));
    if(meta.error||typeof meta.wgsl!=="string")throw Error(meta.error??"Missing render program");
    const hash=createHash("sha256").update(meta.wgsl).update(JSON.stringify(meta.webRender));
    let offset=from+length;
    for(let i=0;i<sections;i++){
      const bytes=header.getUint32(12+4*i,true);
      hash.update(new Uint8Array(buffer,offset,bytes));
      offset+=(bytes+3)&~3;
    }
    const work=call({op:"frameWork"});
    if(work.layouts!==1||work.kept!==0)throw Error(JSON.stringify(work));
    console.log(JSON.stringify({url:input.url,snapshot:input.snapshotSHA256,width,warmup:index===0,ms,
      font:font.family,resources:resources.length,misses,webFonts:webFonts.length,refusedFonts,work,hash:hash.digest("hex")}));
  }finally{
    ffi.symbols.web_render_free(ptr);
  }
}
