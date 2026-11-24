const [library, fixture, mode, font] = Deno.args;
const directory = new URL("./", import.meta.url);
const width = 1280;
const height = 735;
const url = "https://www.w3.org/TR/css-flexbox-1/";
const engine = Deno.dlopen(library, {
  web_document_call: { parameters: ["buffer", "buffer", "u32", "u32"], result: "pointer" },
  web_render_free: { parameters: ["pointer"], result: "void" },
} as const);
const encoder = new TextEncoder();
function call(source: string, options: Record<string, unknown>) {
  const ptr = engine.symbols.web_document_call(encoder.encode(source + "\0"),
    encoder.encode(JSON.stringify(options) + "\0"), width, height);
  if (!ptr) throw Error("empty native result");
  try {
    const result = JSON.parse(new Deno.UnsafePointerView(ptr).getCString());
    if (result.error) throw Error(result.error);
    return result;
  } finally {
    engine.symbols.web_render_free(ptr);
  }
}
const variants: Record<string, string> = {
  original: "",
  "no-number": ".toc .secno {display:none}",
  "no-negative-float": ".toc .secno {margin-left:0!important}",
  "no-wrap": ".toc .content {white-space:nowrap}",
  "break-anywhere": ".toc .content {overflow-wrap:anywhere}",
  "remove-inline-colors": ".toc .content span {display:contents}",
  "property-wrap": ".toc .content .property {white-space:normal!important}",
};
const query = [
  "body", "#toc", ".toc", ".toc a[href='#flex-containers']", ".toc a[href='#flex-containers'] .secno",
  ".toc a[href='#flex-containers'] .content", ".toc a[href='#flex-containers'] .css:nth-of-type(2)",
  ".toc a[href='#flex-containers'] .property", ".head h1", ".head img", ".head a",
];
const original = await Deno.readTextFile(new URL("page.html", directory));
if (font) {
  const data = await Deno.readFile(font);
  let raw = "";
  for (let i = 0; i < data.length; i += 32768) raw += String.fromCharCode(...data.subarray(i, i + 32768));
  const fontSha256 = [...new Uint8Array(await crypto.subtle.digest("SHA-256", data))]
    .map((n) => n.toString(16).padStart(2, "0")).join("");
  console.log(JSON.stringify({font: call("", {
    op:"fontLoad",fontBase64:btoa(raw),fontFamily:"Noto Sans",fontSha256,
  })}));
}
const source = original.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, "")
  .replace(/<body\b/i, "<style>" + variants[mode] + "</style><body") + `<script>
for(const selector of ${JSON.stringify(query)}) {
  const el = document.querySelector(selector);
  if (!el) continue;
  const r = el.getBoundingClientRect(), s = getComputedStyle(el);
  console.log(JSON.stringify({selector, pos:[r.x,r.y,r.width,r.height],
    display:s.display, float:s.float, width:s.width, marginLeft:s.marginLeft,
    whiteSpace:s.whiteSpace, lineHeight:s.lineHeight, fontWeight:s.fontWeight, fontFamily:s.fontFamily,
    fontSize:s.fontSize, borderRadius:s.borderRadius}));
}
</script></body>`;
if (fixture) await Deno.writeTextFile(fixture, source);
const inspect = call(source, {op:"inspect",url,liberal:true});
const stylesheets = inspect.stylesheets.filter((sheet: {url:string}) => /\/(?:W3C-CRD|dark\.css)$/.test(sheet.url));
console.log(JSON.stringify(stylesheets));
const resources = await Promise.all(stylesheets.map(async (sheet: {url:string}) => ({...sheet,
  source: await Deno.readTextFile(new URL(sheet.url.includes("/dark.css") ? "dark.css" : "base.css", directory)),
})));
const start = call(source, {op:"scriptSession",action:"start",engine:"bubblepop",url,width,height,
  layout:{url,liberal:true,partialNote:false,resources}});
try {
  if (!start.logs.length) throw Error(JSON.stringify(start.errors));
  console.log(JSON.stringify({mode,rows:start.logs.map(JSON.parse),errors:start.errors}));
} finally {
  call("", {op:"scriptSession",action:"close",session:start.session});
}
