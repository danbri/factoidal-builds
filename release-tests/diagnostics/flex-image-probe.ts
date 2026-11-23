const engine = Deno.dlopen(Deno.args[0], {
  web_document_call: { parameters: ["buffer", "buffer", "u32", "u32"], result: "pointer" },
  web_render_free: { parameters: ["pointer"], result: "void" },
} as const);
const encoder = new TextEncoder();
const c = (s: string) => encoder.encode(s + "\0");
const bytes = await Deno.readFile(Deno.args[1]);
const png = btoa(String.fromCharCode(...bytes));
const root = "http://flex-image.test/css/css-flexbox/";
const image = new URL("support/solidblue.png", root).href;
const key = "flex-img-probe-16x16";
const call = (html: string, request: Record<string, unknown>) => {
  const ptr = engine.symbols.web_document_call(c(html), c(JSON.stringify(request)), 400, 300);
  if (!ptr) throw Error("native allocation refused");
  try {
    const result = JSON.parse(new Deno.UnsafePointerView(ptr).getCString());
    if (result.error) throw Error(result.error);
    return result;
  } finally {
    engine.symbols.web_render_free(ptr);
  }
};
const stylesheet = '<style>.flex{display:flex;width:40px;height:40px;align-items:flex-start}.flex img{min-width:0;min-height:0}</style>';
const observer = `<script>
window.readImages = label => {
  const records = [...document.querySelectorAll("img")].map(i => {
    const box = i.getBoundingClientRect();
    return [i.parentElement.className, i.complete, i.currentSrc, i.naturalWidth, i.naturalHeight, box.width, box.height];
  });
  console.log(JSON.stringify({label, records}));
};
window.addEventListener('load',()=>readImages("window-load"));
</script>`;
const art = (src: string) => `<img src="${src}">`;
const flex = (src: string) => `<div class="flex">${art(src)}</div>`;
const run = (name: string, fragment: string, held = false) => {
  const url = new URL(name+".html", root).href;
  const results: unknown[] = [];
  const requests: unknown[] = [];
  let session: number | undefined;
  try {
    if (held) call("", {op:"imageLoad",key:image,sha256:key,imageBase64:png});
    const start = call("<!doctype html>"+stylesheet+'<body onload="readImages(\'body-load\')">'+
      fragment+observer, {op:"scriptSession",action:"start",engine:"bubblepop",url,
      resources:[],network:true,pageAddress:"127.0.0.1",width:400,height:300,
      layout:{url, ...(held ? {heldImages:[{key:image,sha256:key}]} : {})}});
    session = start.session;
    let turn = start;
    const seen = new Set<number>();
    let idle = 0;
    for (let n=0; n<60; n++) {
      if (n===0 || turn.logs?.length || turn.errors?.length)
        results.push({turn:n,logs:turn.logs,errors:turn.errors});
      const pending=(turn.netRequests??[]).filter((r:{id:number})=>!seen.has(r.id));
      if (pending.length) {
        idle = 0;
        const answers = [];
        for (const req of pending) {
          seen.add(req.id);
          const ok=req.url===image;
          requests.push({id:req.id,url:req.url,reply:ok?200:404});
          answers.push({id:req.id,status:ok?200:404,statusText:ok?"OK":"Not Found",
            headers:[["content-type",ok?"image/png":"text/plain"]],bodyBase64:ok?png:""});
        }
        turn = call("", {op:"scriptSession",action:"net",session,results:answers,elapsedMs:1});
      } else if (n===0 || (!turn.quiet && idle++<4)) {
        turn = call("", {op:"scriptSession",action:"settle",session,budgetMs:1000});
      } else break;
    }
  } catch (error) {
    results.push({failure:String(error)});
    Deno.exitCode = 1;
  } finally {
    if (session !== undefined) call("", {op:"scriptSession",action:"close",session});
  }
  console.log(JSON.stringify({name,requests,results}));
};

run("static-network",art("support/solidblue.png")+flex("support/solidblue.png"));
run("many-static-network",Array.from({length:18},()=>flex("support/solidblue.png")).join(""));
run("cloned-network",`<template id="source">${flex("support/solidblue.png")}</template>
<script>document.body.appendChild(document.getElementById("source").content.cloneNode(true));</script>`);
run("static-data",art("data:image/png;base64,"+png)+flex("data:image/png;base64,"+png));
run("static-held",art("support/solidblue.png")+flex("support/solidblue.png"),true);
