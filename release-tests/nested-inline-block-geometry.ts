const [library] = Deno.args;
const native = Deno.dlopen(library, {
  web_document_call: { parameters: ["buffer", "buffer", "u32", "u32"], result: "pointer" },
  web_render_free: { parameters: ["pointer"], result: "void" },
} as const);
const encode = (s: string) => new TextEncoder().encode(s+"\0");
const viewport = 640;
function call(html: string, request: Record<string, unknown>) {
  const options = {url:"https://example.test/",liberal:true,engine:"bubblepop",...request};
  const pointer = native.symbols.web_document_call(encode(html), encode(JSON.stringify(options)), viewport, 400);
  if (!pointer) throw Error("missing native response");
  try {
    const result = JSON.parse(new Deno.UnsafePointerView(pointer).getCString());
    if (result.error) throw Error(result.error);
    return result;
  } finally {
    native.symbols.web_render_free(pointer);
  }
}
const style = `<style>
  html,body{margin:0}
  nav{text-align:center;white-space:nowrap}
  ul{display:inline-block;list-style:none;margin:0;padding:0}
  li{position:relative;display:inline-block;border-left:1px solid transparent}
  a{position:relative;display:block;color:black;padding:8px;font-size:12px;line-height:16px}
</style>`;
const markup = `<nav><ul id="list"><li id="item1"><div id="inner1"><a id="link1" href="/one">Alpha</a></div></li><li id="item2"><div id="inner2"><a id="link2" href="/two">Bravo</a></div></li></ul></nav>`;
const measure = `<script>
const ids=["list","item1","inner1","link1","item2","inner2","link2"];
const boxes=ids.map((id)=>{
  const element=document.getElementById(id);
  const box=element.getBoundingClientRect();
  const style=getComputedStyle(element);
  return [id,box.x,box.y,box.width,box.height,style.paddingLeft,style.paddingRight];
});
console.log(JSON.stringify(boxes));
</script>`;
for (const [name, adjust] of [
  ["archived", ""],
  ["no-padding", "a{padding:0}"],
  ["anchor-inline-block", "a{display:inline-block}"],
  ["outer-block", "ul{display:block}"],
  ["outer-block-no-padding", "ul{display:block}a{padding:0}"],
  ["no-nowrap", "nav{white-space:normal}"],
  ["padding-on-items", "a{padding:0}li{padding:8px}"],
]) {
  const html="<!doctype html>"+style+"<style>"+adjust+"</style>"+markup+measure;
  if (["archived", "no-padding", "outer-block", "outer-block-no-padding"].includes(name)) {
    const browserHTML = html.replace("console.log(JSON.stringify(boxes));", "document.body.dataset.boxes = JSON.stringify(boxes);");
    await Deno.writeTextFile(`out/${name}.html`, browserHTML);
  }
  const result=call(html,{op:"scriptSession",action:"start"});
  try {
    console.log(JSON.stringify({name,boxes:result.logs.map(JSON.parse),errors:result.errors}));
  } finally {
    call("",{op:"scriptSession", action:"close",session:result.session});
  }
}
