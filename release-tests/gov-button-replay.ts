const [library, directory, spec] = Deno.args;
const ffi = Deno.dlopen(library, {
  web_document_call: { parameters: ["buffer","buffer","u32","u32"], result: "pointer" },
  web_document_call_bin: { parameters: ["buffer","buffer","u32","u32","buffer"], result: "pointer" },
  web_render_free: { parameters: ["pointer"], result: "void" },
} as const);
const inputs = JSON.parse(await Deno.readTextFile(spec));
const frame=JSON.parse(await Deno.readTextFile(directory+"/frame-1655-2.json"));
const width=frame.width,height=frame.height;
const encoder=new TextEncoder(),decoder=new TextDecoder();
const cstr = (s:string) => encoder.encode(s+"\0");
for(const font of inputs.fonts){
  const result=ffi.symbols.web_document_call(cstr(""),cstr(JSON.stringify({
    op:"fontLoad",webFont:true,fontSha256:font.sha256,fontBase64:font.base64
  })),width,height);
  if(!result)throw Error("font load failed");
  const status=JSON.parse(new Deno.UnsafePointerView(result).getCString());
  ffi.symbols.web_render_free(result);
  if(status.error)throw Error(status.error);
}
const size=new Uint32Array(1);
for(const n of (Deno.env.get("GAP_PREFIXES")??"1,2,9,10,11,12,13,16,168").split(",").map(Number)){
  const before=performance.now();
  const options={...frame.options,op:"render",cpu:true,commands:frame.options.commands.slice(0,n)};
  if(Deno.env.get("GAP_BOX_SIZING")){
    options.commands.push({op:"setAttribute",nodeId:381,name:"style",value:"box-sizing:"+Deno.env.get("GAP_BOX_SIZING")});
  }
  const ptr=ffi.symbols.web_document_call_bin(cstr(frame.source),cstr(JSON.stringify(options)),width,height,size);
  if(!ptr)throw Error("render returned no answer");
  try {
    const buffer=Deno.UnsafePointerView.getArrayBuffer(ptr,size[0]);
    const header=new DataView(buffer);
    const length=header.getUint32(4,true),sections=header.getUint32(8,true);
    const start=12+4*sections;
    const meta=JSON.parse(decoder.decode(new Uint8Array(buffer,start,length)));
    if(meta.error || typeof meta.pixelsSection!=="number")throw Error(JSON.stringify(meta).slice(0,400));
    let offset=start+length;
    for(let i=0;i<meta.pixelsSection;i++)offset+=(header.getUint32(12+4*i,true)+3)&~3;
    const byteCount=header.getUint32(12+4*meta.pixelsSection,true);
    if(byteCount!==width*height*4)throw Error("Unexpected pixel size "+byteCount);
    const pixels=new Uint8Array(buffer,offset,byteCount);
    const lane:number[][]=[];
    for(let y=0;y<height;y++){
      const k=(width*y+2)*4;
      const [r,g,b]=pixels.subarray(k,k+3);
      if(b>g+15 && g>r+15){
        if(lane.length && lane.at(-1)![1]===y-1)lane.at(-1)![1]=y;
        else lane.push([y,y]);
      }
    }
    const head=meta.webRender.glyphRuns.find((x:{source:number;text:string})=>x.source===477&&x.text==="The");
    console.log(JSON.stringify({n,blue:lane,headingY:head?.glyphs[0][2],ms:Math.round(performance.now()-before)}));
  }finally{ffi.symbols.web_render_free(ptr);}
}
