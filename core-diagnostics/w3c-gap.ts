const [library, fixture, viewport] = Deno.args;
const width = Number(viewport);
const height = 735;
const url = "https://www.w3.org/";
const doc = JSON.parse(await Deno.readTextFile(fixture));
const engine = Deno.dlopen(library, {
  web_document_call: { parameters: ["buffer", "buffer", "u32", "u32"], result: "pointer" },
  web_render_free: { parameters: ["pointer"], result: "void" },
} as const);
const encoder = new TextEncoder();
function call(source: string, options: Record<string, unknown>) {
  const ptr = engine.symbols.web_document_call(
    encoder.encode(source + "\0"),
    encoder.encode(JSON.stringify(options) + "\0"),
    width,
    height,
  );
  if (!ptr) throw Error("native engine returned no answer");
  try {
    const result = JSON.parse(new Deno.UnsafePointerView(ptr).getCString());
    if (result.error) throw Error(result.error);
    return result;
  } finally {
    engine.symbols.web_render_free(ptr);
  }
}
const selectors = ["html", "body", ".skip-link", ".global-header", ".global-header > [role=status]",
  "#lang-nav", "#lang-nav .l-cluster", "#global-nav", ".logo", ".hero", ".hero h1"];
const script = `<script>
for (const selector of ${JSON.stringify(selectors)}) {
  const el = document.querySelector(selector);
  if (!el) continue;
  const r = el.getBoundingClientRect(), s = getComputedStyle(el);
  console.log(JSON.stringify({
    selector, x:r.x, y:r.y, width:r.width, height:r.height,
    display:s.display, position:s.position, visibility:s.visibility, lineHeight:s.lineHeight,
    marginTop:s.marginTop, marginBottom:s.marginBottom,
    paddingTop:s.paddingTop, paddingBottom:s.paddingBottom
  }));
}
</script>`;
const original = (doc.html as string).replace(/<script\b[^>]*>[\s\S]*?<\/script\s*>/gi, "");
const inspect = call(original, {op:"inspect", url, liberal:true});
const resources = inspect.stylesheets.flatMap((entry: {url:string}) =>
  doc.css[entry.url] ? [{...entry, source:doc.css[entry.url]}] : []);
if (resources.length < 2) throw Error("captured stylesheets are missing");
const images = Object.entries(doc.images).map(([key, base64]) => ({key, base64}));
const reduced = `<!doctype html><style>
body{margin:0;line-height:30px}
.frame{position:relative}
.anchor{position:absolute;width:10px;height:8px}
#next{height:20px}
</style>
<div class="frame">
  <span class="anchor" id="anchor"></span>
  IN_FLOW
  <div id="next"></div>
</div>
<script>
const a = document.querySelector("#anchor").getBoundingClientRect();
const b = document.querySelector("#next").getBoundingClientRect();
console.log(JSON.stringify({anchor:[a.y,a.width,a.height], next:b.y}));
</script>`;
for (const [text, expected] of [["", 0], ["Visible text", 30]] as const) {
  const start = call(reduced.replace("IN_FLOW", text), {
    op:"scriptSession", action:"start", engine:"bubblepop", url, width, height,
  });
  try {
    if (start.errors.length) throw Error(JSON.stringify(start.errors));
    const [result] = start.logs.map(JSON.parse);
    console.log(JSON.stringify({width,mode:"reduced",text,result}));
    if (Math.abs(result.next - expected) > 0.1 || String(result.anchor) !== "0,10,8") {
      throw Error("incorrect height or missing static anchor");
    }
  } finally {
    call("", {op:"scriptSession",action:"close",session:start.session});
  }
}
for (const [mode, rule] of [
  ["original", ""],
  ["skip-absent", ".skip-link{display:none!important}"],
  ["status-absent", ".global-header > [role=status]{display:none!important}"],
  ["hidden-absent", ".skip-link,.global-header > [role=status],.visuallyhidden{display:none!important}"],
  ["bare-top", "html,body,.global-header,#lang-nav{margin:0!important;padding:0!important}"],
]) {
  const source = original.replace(/<\/head>/i, "<style>" + rule + "</style></head>")
    .replace(/<\/body>/i, script + "</body>");
  const start = call(source, {
    op:"scriptSession", action:"start", engine:"bubblepop", url, width, height,
    layout:{url, liberal:true, partialNote:false, resources, images},
  });
  try {
    if (start.errors.length) throw Error(JSON.stringify(start.errors));
    const rows = start.logs.map(JSON.parse);
    if (!rows.some((row: {selector: string}) => row.selector === "#lang-nav")) {
      throw Error("missing language navigation geometry");
    }
    console.log(JSON.stringify({width,mode,rows}));
    if (mode === "original") {
      const lang = rows.find((row: {selector:string}) => row.selector === "#lang-nav");
      if (Math.abs(lang.y) > 0.1) throw Error("W3C language bar still has a leading gap");
    }
  } finally {
    call("", {op:"scriptSession",action:"close",session:start.session});
  }
}
