const [library, directory, mode = "closed"] = Deno.args;
const ffi = Deno.dlopen(library, {
  web_document_call: { parameters:["buffer","buffer","u32","u32"], result:"pointer" },
  web_document_call_bin: { parameters:["buffer","buffer","u32","u32","buffer"], result:"pointer" },
  web_render_free: { parameters:["pointer"], result:"void" },
} as const);
const input = JSON.parse(await Deno.readTextFile(directory + "/input.json"));
let html = await Deno.readTextFile(directory + "/page.html");
const decoder = new TextDecoder();
const encoder = new TextEncoder();
const cstr = (value:string) => encoder.encode(value + "\0");
const width = 1280, height = 800;
const marker = /<details\b[^>]*>\s*<summary>More details about this document<\/summary>/i;
const match = html.match(marker);
if (!match) throw Error("Could not locate the archived document summary");
const changed = match[0].replace(/<details\b[^>]*>/, (tag) => {
  const closed = tag.replace(/\s+open\b(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^\s>]+))?/i, "");
  return mode === "open" ? closed.slice(0,-1)+" open>" : closed;
});
html = html.replace(marker, changed);
const source = cstr(html);
const request = (extra:Record<string,unknown>) => cstr(JSON.stringify({
  url:input.url,liberal:true,partialNote:false,scripting:false,...extra,
}));
const inspectPointer = ffi.symbols.web_document_call(source,request({op:"inspect"}),width,height);
if (!inspectPointer) throw Error("inspect returned no answer");
let inspect;
try {
  inspect = JSON.parse(new Deno.UnsafePointerView(inspectPointer).getCString());
} finally {
  ffi.symbols.web_render_free(inspectPointer);
}
if (inspect.error) throw Error(inspect.error);
const resources = inspect.stylesheets.flatMap((sheet:{nodeId:number;url:string}) =>
  Object.hasOwn(input.css,sheet.url) ? [{nodeId:sheet.nodeId,url:sheet.url,source:input.css[sheet.url]}] : []);
if (resources.length === 0) throw Error("No archived stylesheets were delivered");
const size = new Uint32Array(1);
const ptr = ffi.symbols.web_document_call_bin(source,request({op:"render",checks:false,cpu:true,resources}),width,height,size);
if (!ptr) throw Error("render returned no answer");
try {
  const buffer = Deno.UnsafePointerView.getArrayBuffer(ptr,size[0]);
  const header = new DataView(buffer);
  const length = header.getUint32(4,true), sections = header.getUint32(8,true);
  const start = 12 + 4*sections;
  const meta = JSON.parse(decoder.decode(new Uint8Array(buffer,start,length)));
  if (meta.error || typeof meta.pixelsSection !== "number") throw Error(JSON.stringify(meta).slice(0,500));
  type Run = {text:string;source:number;glyphs:number[][]};
  const runs:Run[] = meta.webRender.glyphRuns;
  const words = ["More","details","about","this","document"];
  const at = runs.findIndex((_,i)=>words.every((word,j)=>runs[i+j]?.text === word));
  if (at < 2) throw Error("No summary words in the rendered glyph runs");
  const summary = runs.slice(at-2,at+words.length).map(r=>({text:r.text,source:r.source,x:r.glyphs[0]?.[1],y:r.glyphs[0]?.[2]}));
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
  await Deno.writeFile(directory+"/"+mode+".ppm",ppm);
  console.log(JSON.stringify({url:input.url,sha:input.snapshotSHA256,mode,resources:resources.length,summary}));
} finally {
  ffi.symbols.web_render_free(ptr);
}
