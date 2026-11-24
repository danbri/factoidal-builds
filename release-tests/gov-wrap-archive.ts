const [library, directory] = Deno.args;
const ffi = Deno.dlopen(library, {
  web_document_call: { parameters:["buffer","buffer","u32","u32"], result:"pointer" },
  web_document_call_bin: { parameters:["buffer","buffer","u32","u32","buffer"], result:"pointer" },
  web_render_free: { parameters:["pointer"], result:"void" },
} as const);
const input = JSON.parse(await Deno.readTextFile(directory + "/input.json"));
const html = await Deno.readTextFile(directory + "/page.html");
const decoder = new TextDecoder();
const encoder = new TextEncoder();
const cstr = (value:string) => encoder.encode(value + "\0");
const width = input.width, height = 800;
const source = cstr(html);
const request = (extra:Record<string,unknown>) => cstr(JSON.stringify({
  url:input.url,liberal:true,partialNote:false,scripting:false,...extra,
}));
function call(extra:Record<string,unknown>){
  const ptr = ffi.symbols.web_document_call(source,request(extra),width,height);
  if (!ptr) throw Error("no document answer");
  try {
    return JSON.parse(new Deno.UnsafePointerView(ptr).getCString());
  } finally {
    ffi.symbols.web_render_free(ptr);
  }
}
const inspect = call({op:"inspect"});
if (inspect.error) throw Error(inspect.error);
const resources = inspect.stylesheets.flatMap((sheet:{nodeId:number;url:string}) =>
  Object.hasOwn(input.css,sheet.url) ? [{nodeId:sheet.nodeId,url:sheet.url,source:input.css[sheet.url]}] : []);

if (resources.length < 2) throw Error("Missing GOV.UK stylesheets");
const fontStatus = (input.fonts as {url:string;sha256:string;base64:string}[]).map(font => ({
  url:font.url, sha256:font.sha256,
  result:call({op:"fontLoad",webFont:true,fontSha256:font.sha256,fontBase64:font.base64}),
}));
const webFonts = fontStatus.filter(font => !font.result.error).map(({url,sha256}) => ({url,sha256}));
const size = new Uint32Array(1);
const ptr = ffi.symbols.web_document_call_bin(source,request({op:"render",checks:false,cpu:true,resources,webFonts}),width,height,size);
if (!ptr) throw Error("render returned no answer");
try {
  const buffer = Deno.UnsafePointerView.getArrayBuffer(ptr,size[0]);
  const header = new DataView(buffer);
  const length = header.getUint32(4,true), sections = header.getUint32(8,true);
  const start = 12 + 4*sections;
  const meta = JSON.parse(decoder.decode(new Uint8Array(buffer,start,length)));
  if (meta.error || typeof meta.pixelsSection !== "number") throw Error(JSON.stringify(meta).slice(0,500));
  type Run = {text:string;source:number;glyphs:number[][];width?:number};
  const runs = meta.webRender.glyphRuns as Run[];
  const text = "The best place to find government services and information".split(" ");
  const at = runs.findIndex((_,i) => text.every((word,j)=>runs[i+j]?.text===word));
  if (at < 0) throw Error("No heading glyph runs");
  const heading = runs.slice(at,at+text.length).map(run => ({
    text:run.text,x:run.glyphs[0][1],y:run.glyphs[0][2],
    right:run.glyphs.at(-1)?.[1],
  }));
  let offset = start+length;
  for (let i=0;i<meta.pixelsSection;i++) offset += (header.getUint32(12+4*i,true)+3)&~3;
  const byteCount = header.getUint32(12+4*meta.pixelsSection,true);
  if (byteCount !== width*height*4) throw Error("Unexpected pixel size");
  const pixels = new Uint8Array(buffer,offset,byteCount);
  const ppmHeader = encoder.encode(`P6\n${width} ${height}\n255\n`);
  const ppm = new Uint8Array(ppmHeader.length+width*height*3);
  ppm.set(ppmHeader);
  for (let i=0,k=ppmHeader.length;i<pixels.length;i+=4) {
    ppm[k++]=pixels[i]; ppm[k++]=pixels[i+1]; ppm[k++]=pixels[i+2];
  }
  await Deno.writeFile(directory+"/govuk.ppm",ppm);
  console.log(JSON.stringify({url:input.url,sha:input.snapshotSHA256,resources:resources.length,fontStatus,heading}));
} finally {
  ffi.symbols.web_render_free(ptr);
}
