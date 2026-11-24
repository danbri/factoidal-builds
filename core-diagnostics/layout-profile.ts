const [lib, directory, mode = "layout", fontPath] = Deno.args;
const native = Deno.dlopen(lib, {
  web_document_call: {parameters:["buffer","buffer","u32","u32"],result:"pointer"},
  web_render_free: {parameters:["pointer"],result:"void"},
} as const);
const input = JSON.parse(await Deno.readTextFile(directory + "/input.json"));
const html = await Deno.readTextFile(directory + "/page.html");
const utf8 = new TextEncoder();
const z = (s: string) => utf8.encode(s + "\0");
const source = z(html);
function call(op: string, extra: Record<string, unknown> = {}, width = input.width) {
  const request = z(JSON.stringify({op,url:input.url,liberal:true,scripting:false,partialNote:false,...extra}));
  const start = performance.now();
  const ptr = native.symbols.web_document_call(source,request,width,736);
  const nativeMs = Math.round(performance.now() - start);
  if (!ptr) throw Error("No native result");
  try {
    const result = JSON.parse(new Deno.UnsafePointerView(ptr).getCString());
    console.log(JSON.stringify({op,width,nativeMs,error:result.error??null}));
    if (result.error) throw Error(result.error);
    return result;
  } finally {
    native.symbols.web_render_free(ptr);
  }
}
console.log(JSON.stringify({stage:"start", pid:Deno.pid,mode,url:input.url,snapshot:input.snapshotSHA256}));
if (fontPath) {
  const bytes=await Deno.readFile(fontPath);
  let text="";
  for(let i=0;i<bytes.length;i+=32768) text+=String.fromCharCode(...bytes.subarray(i,i+32768));
  const sha256=[...new Uint8Array(await crypto.subtle.digest("SHA-256",bytes))].map(x=>x.toString(16).padStart(2,"0")).join("");
  call("fontLoad",{fontBase64:btoa(text),fontFamily:"Noto Sans",fontSha256:sha256});
}
const inspect = call("inspect");
const resources = [];
for (const sheet of inspect.stylesheets) {
  if (Object.hasOwn(input.css,sheet.url)) resources.push({nodeId:sheet.nodeId,url:sheet.url,source:input.css[sheet.url]});
}
console.log(JSON.stringify({stage:"layout",sheets:resources.length,listedSheets:inspect.stylesheets.length}));
if (mode === "sample") await new Promise(resolve => setTimeout(resolve,1600));
if (mode === "fonts") call("fontFaces",{resources});
else {
  for (const dw of mode === "sample" ? [0,9,19,29,39,49,59,69,79,89,99,109] : [0]) call("nodeAt",{x:10,y:10,resources}, input.width + dw);
}
