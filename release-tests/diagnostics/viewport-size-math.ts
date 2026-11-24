const engine = Deno.dlopen(Deno.args[0], {
  web_document_call: { parameters: ["buffer", "buffer", "u32", "u32"], result: "pointer" },
  web_render_free: { parameters: ["pointer"], result: "void" },
} as const);
const encoder = new TextEncoder();
const bytes = (value: string) => encoder.encode(value + "\0");
const call = (html: string, request: Record<string, unknown>, width = 1280) => {
  const ptr = engine.symbols.web_document_call(bytes(html), bytes(JSON.stringify(request)), width, 736);
  if (ptr === null) throw Error("native engine returned no answer");
  try {
    const result = JSON.parse(new Deno.UnsafePointerView(ptr).getCString());
    if (result.error) throw Error(result.error);
    return result;
  } finally { engine.symbols.web_render_free(ptr); }
};
const url = "https://example.test/";
const geometry = `<script>
const box = id => {
  const el = document.getElementById(id);
  const b = el.getBoundingClientRect();
  return [id,b.x,b.y,b.width,b.height,getComputedStyle(el).width];
};
console.log(JSON.stringify(Array.from(document.querySelectorAll("[id]"), el => box(el.id))));
</script>`;
const trace = (name: string, contents: string, width: number) => {
  const start = call("<!doctype html>" + contents + geometry,
    {op:"scriptSession",action:"start",engine:"bubblepop",url,width,height:736}, width);
  try {
    const [records] = start.logs.map(JSON.parse);
    console.log(JSON.stringify({name,width,records,errors:start.errors}));
    if (start.errors.length) throw Error(JSON.stringify(start.errors));
    return records;
  }
  finally { call("", {op:"scriptSession",action:"close",session:start.session},width); }
};
const picture = btoa("<svg xmlns='http://www.w3.org/2000/svg' width='358' height='358'><rect width='358' height='358'/></svg>");
const logo = (size: string) => `<style>
body{margin:0}.header{width:90%;display:flex;align-items:center}
.logo{display:block;width:${size}}.large{max-inline-size:100%;display:block}
</style><div class=header><a href="/"><span class=logo id=logo><img class=large id=image
src="data:image/svg+xml;base64,${picture}"></span></a><div id=nav>Navigation</div></div>`;

for(const [viewport, expected] of [[1280,120],[480,69.9104]]) {
  const actual=trace("logo-clamp",logo("clamp(3.75rem, 2.51rem + 6.198vw, 7.5rem)"),viewport);
  const reference=trace("logo-explicit",logo(expected+"px"),viewport);
  for(const id of ["logo","image"]) {
    const w=actual.find((r:unknown[])=>r[0]===id)[3];
    const old=reference.find((r:unknown[])=>r[0]===id)[3];
    if (!Number.isFinite(w)||!Number.isFinite(old)||Math.abs(w-expected)>0.05||Math.abs(w-old)>0.05) {
      console.error(id, viewport, {w,old,expected});
      Deno.exitCode=1;
    }
  }
}
