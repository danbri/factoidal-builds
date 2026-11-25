const engine = Deno.dlopen(Deno.args[0], {
  web_document_call: {parameters: ["buffer", "buffer", "u32", "u32"], result: "pointer"},
  web_render_free: {parameters: ["pointer"], result: "void"},
} as const);
const bytes = (s: string) => new TextEncoder().encode(s + "\0");
const url = "https://www.w3.org/help/search/";
function call(source: string, req: Record<string, unknown>) {
  const p = engine.symbols.web_document_call(bytes(source), bytes(JSON.stringify(req)), 1280, 735);
  if (!p) throw Error("Missing native answer");
  try {
    const r = JSON.parse(new Deno.UnsafePointerView(p).getCString());
    if (r.error) throw Error(r.error);
    return r;
  } finally { engine.symbols.web_render_free(p); }
}
const actual = ":where(input:not([type=checkbox], [type=radio], textarea), select){min-block-size:2.9375rem}";
for (const [variant, rule] of Object.entries({
  none: "",
  actual,
  logical: "#search{min-block-size:2.9375rem}",
  physical: "#search{min-height:2.9375rem}",
  explicit: "#search{height:2.9375rem}",
})) {
  const source = `<!doctype html><html><head><style>
    *{box-sizing:border-box} form{display:flex} .wide{flex:1} input{padding:5px;border:2px solid;width:100%;position:relative}
    ${rule}</style></head><body><form><div class=wide><input type=search id=search></div><button>Search</button></form>
    <script>const el=document.getElementById("search"), style=getComputedStyle(el);
      console.log(JSON.stringify([el.getBoundingClientRect().height,style.minHeight,style.minBlockSize,style.height]));
    </script></body></html>`;
  const r = call(source,{op:"scriptSession",action:"start",engine:"bubblepop",url,width:1280,height:735,resources:[],layout:{url,liberal:true,partialNote:false,resources:[]}});
  try { console.log(JSON.stringify({variant,logs:r.logs,errors:r.errors})); }
  finally { if (r.session) call("",{op:"scriptSession",action:"close",session:r.session}); }
}
