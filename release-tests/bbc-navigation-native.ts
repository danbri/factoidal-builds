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
const navigation = html.match(/<nav data-testid="level2-navigation-container"[^>]*>[\s\S]*?<\/ul>/)?.[0];
if (!navigation) throw Error("Secondary navigation absent from archive");
const hrefs = Array.from(navigation.matchAll(/<a href="([^"]+)"/g), match => match[1]);
if (hrefs.length < 5) throw Error("Missing archived navigation links");
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
  const links = (meta.webRender.links as unknown[][]).filter(row =>
    typeof row[1] === "string" && hrefs.includes(new URL(row[1],input.url).pathname) &&
    typeof row[3] === "number" && row[3] < 280);
  const labels = new Set(["Canada","Africa","Asia","Australia","Europe","InDepth","Verify"]);
  type Run = {text:string;source:number;glyphs:number[][]};
  const glyphs = (meta.webRender.glyphRuns as Run[]).filter(run =>
    labels.has(run.text) && run.glyphs[0]?.[2] < 280).map(run => [run.text,run.source,...run.glyphs[0].slice(1,3)]);
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
  await Deno.writeFile(directory+"/bbc.ppm",ppm);
  console.log(JSON.stringify({url:input.url,sha:input.snapshotSHA256,resources:resources.length,hrefs,links,glyphs}));
} finally {
  ffi.symbols.web_render_free(ptr);
}
