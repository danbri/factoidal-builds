const engine = Deno.dlopen(Deno.args[0], {
  web_document_call: { parameters: ["buffer", "buffer", "u32", "u32"], result: "pointer" },
  web_render_free: { parameters: ["pointer"], result: "void" },
} as const);
const encoder = new TextEncoder();
const bytes = (value: string) => encoder.encode(value + "\0");
const call = (html: string, request: Record<string, unknown>, width: number, height: number) => {
  const ptr = engine.symbols.web_document_call(bytes(html), bytes(JSON.stringify(request)), width, height);
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
  const css = getComputedStyle(el);
  return [id,b.x,b.y,b.width,b.height,css.width,css.paddingLeft,css.paddingTop,css.marginLeft];
};
console.log(JSON.stringify(Array.from(document.querySelectorAll("[id]"), el => box(el.id))));
</script>`;
const trace = (name: string, contents: string, width: number, height: number) => {
  const start = call("<!doctype html>" + contents + geometry,
    {op:"scriptSession",action:"start",engine:"bubblepop",url,width,height}, width,height);
  try {
    const [records] = start.logs.map(JSON.parse);
    console.log(JSON.stringify({name,width,records,errors:start.errors}));
    if (start.errors.length) throw Error(JSON.stringify(start.errors));
    return records;
  }
  finally { call("", {op:"scriptSession",action:"close",session:start.session},width,height); }
};

type Values = { horizontal: string; vertical: string; inset: string };
const html = ({horizontal, vertical, inset}: Values) => `<style>
body{margin:0}
.frame{width:60%;padding-inline:var(--inset)}
.breakout{position:relative;width:100vw;inset-inline:50%;margin-inline:var(--shift)}
.tall{width:100px;border:2px solid black;padding:var(--tall) var(--inset)}
#inherited{padding-top:inherit}
</style><div class=frame id=frame style="--inset:${inset}">
<div id=breakout class=breakout style="--shift:${horizontal}"><div class=tall id=box style="--tall:${vertical}">
<div style="height:5px" id=inherited></div>
<div style="height:5px;padding-top:0;margin-left:${horizontal};margin-left:1px;padding-left:${inset};padding-left:initial" id=reset></div>
</div></div></div>`;

for (const [width, height] of [[1440,735], [480,500], [480,735]]) {
  const actual = trace("viewport",html({horizontal:"-50vw",vertical:"10vh",inset:"5vw"}),width,height);
  const reference = trace("pixels",html({horizontal:`${-width/2}px`,vertical:`${height/10}px`,inset:`${width/20}px`}),width,height);
  for (const id of ["frame","breakout","box","inherited","reset"]) {
    const row = actual.find((item: unknown[]) => item[0] === id);
    const expected = reference.find((item: unknown[]) => item[0] === id);
    if (!row || !expected || [1,2,3,4].some(i =>
      !Number.isFinite(row[i]) || !Number.isFinite(expected[i]) || Math.abs(row[i]-expected[i]) > 0.05) ||
      [5,6,7,8].some(i => row[i] !== expected[i])) {
      console.error(id, {width, height, row, expected});
      Deno.exitCode = 1;
    }
  }
}
