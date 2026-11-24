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
  return [id,b.x,b.y,b.width,b.height,getComputedStyle(el).width,getComputedStyle(el).display];
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

const css=`<style>body{margin:0}.form{width:630px;background:#176aba}.table{display:table;width:100%;background:white}
.cell{display:table-cell}.submit{width:1%}input{box-sizing:border-box;width:100%;height:50px}button{width:50px;height:50px}</style>`;
const markup=(first:string,second:string,tableClass="table")=>css+
 `<form class=form><label>Search</label><div id=table class="${tableClass}"><div class="${first}" id=input-wrap>
 <input type=search id=input></div><div class="${second}" id=submit-wrap><button id=button>Go</button></div></div></form>`;

const ordinary=trace("ordinary-search-input",markup("","cell submit"),1280);
const replaced=trace("internal-atomic-search-input",
  markup("","cell submit").replace("input type=search","input class=cell type=search"),1280);
const byId=(rows:unknown[][],id:string)=>rows.find(row=>row[0]===id);
const width=(rows:unknown[][],id:string)=>Number(byId(rows,id)?.[3]);
const norm=width(ordinary,"input"), got=width(replaced,"input");
if (!Number.isFinite(got)||!Number.isFinite(norm)||norm<500||Math.abs(got-norm)>0.05) {
  console.error({ordinaryWidth:norm,styledWidth:got});
  Deno.exitCode=1;
}
for(const rows of [ordinary,replaced]) {
  if (byId(rows,"submit-wrap")?.[6]!=="table-cell" || width(rows,"submit-wrap")<=0) {
    console.error("ordinary submit wrapper did not remain a table cell");
    Deno.exitCode=1;
  }
}
if (byId(replaced,"input")?.[6]!=="table-cell") {
  console.error("the computed display of the replaced input changed");
  Deno.exitCode=1;
}
