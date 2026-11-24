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
const clearRule = '.row::after { content: ""; display: block; clear: both }';
const unrelatedHas = ".unrelated:has(> :not([hidden])) { margin-bottom: 12px }";
const checks = `<script>
const row = document.querySelector(".row");
const column = document.querySelector(".column");
const next = document.querySelector(".next");
const rb = row.getBoundingClientRect(), cb = column.getBoundingClientRect(), nb = next.getBoundingClientRect();
const after = getComputedStyle(row, "::after");
console.log(JSON.stringify({rowHeight:rb.height,columnHeight:cb.height,nextOffset:nb.top-rb.top,display:after.display,clear:after.clear}));
</script>`;
function measure(name: string, rule: string, explicit = false) {
  const html = `<!doctype html><style>body {margin:0}.column {float:left;width:50%;height:90px}
    ${rule}</style><div class=row><div class=column></div>${explicit ? '<div style="clear:both"></div>' : ""}
    </div><div class=next>Following section</div>${checks}`;
  const start = call(html, {op:"scriptSession",action:"start",engine:"bubblepop",url,width:1280,height:736});
  try {
    if (start.errors.length !== 0 || start.logs.length !== 1) throw Error(JSON.stringify(start.errors));
    const record = JSON.parse(start.logs[0]);
    console.log(JSON.stringify({name, ...record}));
    return record;
  } finally {
    call("", {op:"scriptSession",action:"close",session:start.session});
  }
}
const plain = measure("generated-only", clearRule);
const withHas = measure("generated-with-unrelated-has", clearRule + unrelatedHas);
const explicit = measure("ordinary-clear-with-has", unrelatedHas, true);
const open = measure("float-without-clear", unrelatedHas);
if (plain.rowHeight !== 90 || explicit.rowHeight !== 90 || open.rowHeight !== 0 ||
    withHas.rowHeight !== explicit.rowHeight || withHas.nextOffset !== explicit.nextOffset ||
    withHas.columnHeight !== 90 || withHas.display !== "block" || withHas.clear !== "both") {
  Deno.exit(1);
}
