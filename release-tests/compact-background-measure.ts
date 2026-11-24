const [library,directory] = Deno.args;
const ffi = Deno.dlopen(library, {
  web_document_call: {parameters:["buffer","buffer","u32","u32"],result:"pointer"},
  web_document_call_bin: {parameters:["buffer","buffer","u32","u32","buffer"],result:"pointer"},
  web_render_free: {parameters:["pointer"],result:"void"},
} as const);
const input=JSON.parse(await Deno.readTextFile(directory+"/input.json"));
const html=await Deno.readTextFile(directory+"/page.html");
const encoder=new TextEncoder(),decoder=new TextDecoder();
const zero=(s:string)=>encoder.encode(s+"\0");
const width=1280, height=735;
const request=(options:Record<string,unknown>)=>zero(JSON.stringify({
  ...options,liberal:true,scripting:false,partialNote:false,checks:false,url:input.url,
}));
function inspect(source:string){
  const ptr=ffi.symbols.web_document_call(zero(source),request({op:"inspect"}),width,height);
  if(!ptr)throw Error("No response from inspect");
  try{
    const result=JSON.parse(new Deno.UnsafePointerView(ptr).getCString());
    if(result.error)throw Error(result.error);
    return result;
  }finally{ffi.symbols.web_render_free(ptr);}
}

const sheets=inspect(html).stylesheets as {nodeId:number;url:string}[];
const resources=sheets.flatMap(s=>Object.hasOwn(input.css,s.url) ? [{...s,source:input.css[s.url]}] : []);
const key="https://jvns.ca/stylesheets/noise.png";
if(!input.images[key]||resources.length<1)throw Error("Incomplete archived assets");

function measure(name:string,source:string,points:number[][],options:Record<string,unknown>={}){
  const size=new Uint32Array(1);
  const ptr=ffi.symbols.web_document_call_bin(zero(source),request({
    op:"render",cpu:true,diagnostics:true,...options,
  }),width,height,size);
  if(!ptr)throw Error("No render response");
  try{
    const data=Deno.UnsafePointerView.getArrayBuffer(ptr,size[0]);
    const header=new DataView(data);
    const length=header.getUint32(4,true),sections=header.getUint32(8,true);
    const body=12+4*sections;
    const meta=JSON.parse(decoder.decode(new Uint8Array(data,body,length)));
    if(meta.error || typeof meta.pixelsSection!=="number")throw Error(meta.error??"No CPU pixels");
    let seek=body+length;
    for(let i=0;i<meta.pixelsSection;i++)seek+=(header.getUint32(12+4*i,true)+3)&~3;
    const image=new Uint8Array(data,seek,header.getUint32(12+4*meta.pixelsSection,true));
    if(image.length!==width*height*4)throw Error("Wrong raster bounds");
    const colors=points.map(([x,y])=>[...image.subarray((y*width+x)*4,(y*width+x)*4+3)]);
    console.log(JSON.stringify({name,colors,diagnostics:meta.diagnostics??[]}));
  }finally{ffi.symbols.web_render_free(ptr);}
}

measure("jvns",html,Array.from({length:119},(_,i)=>[25,100+i]),
  {resources,images:[{key,base64:input.images[key]}]});

const png="iVBORw0KGgoAAAANSUhEUgAAAAEAAAACCAIAAAAW4yFwAAAAEElEQVR4nGP4z8DAwMDwHwAIAAH/B2G9UwAAAABJRU5ErkJggg==";
for(const repeat of ["repeat","repeat-x","repeat-y","no-repeat"]){
  const css=`body{margin:0}div{width:400px;height:300px;background:white url(data:image/png;base64,${png}) 7px 5px /`+
    `1px 2px ${repeat}}`;
  measure(repeat,`<!doctype html><style>${css}</style><div></div>`,
    [[7,5],[7,6],[7,123],[199,5],[199,123],[410,123]]);
}
