const [library, mode] = Deno.args;
const style = mode === "balance" ? "text-wrap:balance" : "text-wrap:wrap";
const words = ["AAAA","BBBB","CCCC","DDDD","EEEE","FFFF"];
const html = `<!doctype html><style>body{margin:0}h1{margin:0;width:540px;font:32px/40px monospace;${style}}</style>
<h1>${words.map(w=>`<span>${w}</span>`).join(" ")}</h1>`;
if (!library) throw Error("Supply libweb-render and wrap or balance");
const ffi = Deno.dlopen(library, {
  web_document_call:{parameters:["buffer","buffer","u32","u32"],result:"pointer"},
  web_render_free:{parameters:["pointer"],result:"void"},
} as const);
const measure = `<script>
const h = document.querySelector("h1");
const style = getComputedStyle(h);
const boxes = Array.from(h.children, e => { const b=e.getBoundingClientRect(); return [e.textContent,b.x,b.y,b.width]; });
console.log(JSON.stringify({style:style.getPropertyValue("text-wrap-style"),mode:style.getPropertyValue("text-wrap-mode"),boxes}));
</script>`;
const cstr=(value:string)=>new TextEncoder().encode(value+"\0");
const ptr=ffi.symbols.web_document_call(cstr(html+measure),cstr(JSON.stringify({
  op:"scriptSession",action:"start",url:"https://example.test/",engine:"bubblepop",liberal:true,
})),640,250);
if(!ptr)throw Error("No native answer");
try {
  const answer=JSON.parse(new Deno.UnsafePointerView(ptr).getCString());
  if(answer.error || answer.errors?.length)throw Error(JSON.stringify(answer.error??answer.errors));
  console.log(answer.logs[0]);
} finally {
  ffi.symbols.web_render_free(ptr);
}
if (Deno.env.get("REFERENCE_OUT")) {
  const ref=measure.replace("console.log(JSON.stringify(", "document.body.dataset.layout=JSON.stringify(").replace("}));","});");
  await Deno.writeTextFile(Deno.env.get("REFERENCE_OUT")!, html+ref);
}
