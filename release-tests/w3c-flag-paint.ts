const [library, fixture, mode] = Deno.args;
const ffi = Deno.dlopen(library, {
  web_document_call: { parameters:["buffer","buffer","u32","u32"], result:"pointer" },
  web_document_call_bin: { parameters:["buffer","buffer","u32","u32","buffer"], result:"pointer" },
  web_render_free: { parameters:["pointer"], result:"void" },
} as const);
const enc = new TextEncoder(), dec = new TextDecoder();
const cstr = (s: string) => enc.encode(s + "\0");
const base = "https://www.w3.org/StyleSheets/TR/2021/";
const badge = base + "logos/CRD.svg";
const doc = JSON.parse(await Deno.readTextFile(fixture));
const archived = mode !== "reduce";
const width = archived ? 1280 : 180, height = archived ? 735 : 100;
const finish = (opts: Record<string, unknown>) => cstr(JSON.stringify({url:"https://www.w3.org/TR/css-flexbox-1/",liberal:true,cpu:true,checks:false,partialNote:false,...opts}));
const example = (rule: string) => `<!doctype html><style>
body{margin:0;background:#000}
#outer{height:70px;background:#fff url(${badge}) top left no-repeat;background-size:25px auto}
#inner{margin-left:60px;height:70px;${rule};background-color:#fff}
</style><div id="outer"><div id="inner"></div></div>`;
const variants = archived ? [
  ["authored",""],
  ["explicit",`#toc{background-image:url(${badge})!important;background-repeat:no-repeat!important;background-size:25px auto!important}`],
  ["hidden-sidebar","#toc{display:none!important}"],
] : [
  ["reference",`background-image:url(${badge});background-repeat:no-repeat;background-size:25px auto`],
  ["shorthand","background:inherit"],
  ["longhands","background-image:inherit;background-repeat:inherit;background-size:inherit"],
];
for (const [name, rule] of variants) {
  const source = cstr(archived ? doc.page.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, "").replace(/<body\b/i,`<style>${rule}</style><body`) : example(rule));
  function inspect(extra: Record<string,unknown> = {}) {
    const p = ffi.symbols.web_document_call(source,finish({op:"inspect",...extra}),width,height);
    if (!p) throw Error("No inspect response");
    try {
      const result = JSON.parse(new Deno.UnsafePointerView(p).getCString());
      if (result.error) throw Error(result.error);
      return result;
    } finally { ffi.symbols.web_render_free(p); }
  }
  const initial = inspect();
  const resources = initial.stylesheets.flatMap((sheet: {url:string}) => doc.css[sheet.url] ? [{...sheet,source:doc.css[sheet.url]}] : []);
  const imported = [{url:base+"base.css",source:doc.css[base+"base.css"]}];
  const listed = inspect({resources,imported}).backgroundImages?.map((image: {url:string})=>image.url) ?? [];
  const images = Object.entries(doc.images).map(([key,base64])=>({key,base64}));
  const size = new Uint32Array(1);
  const q = ffi.symbols.web_document_call_bin(source,finish({op:"render",resources,imported,images}),width,height,size);
  if (!q) throw Error("No render response");
  try {
    const buffer = Deno.UnsafePointerView.getArrayBuffer(q,size[0]);
    const view = new DataView(buffer);
    const start = 12+4*view.getUint32(8,true), length = view.getUint32(4,true);
    const meta = JSON.parse(dec.decode(new Uint8Array(buffer,start,length)));
    const section = meta.pixelsSection;
    if (meta.error || !Number.isInteger(section)) throw Error(JSON.stringify(meta).slice(0,500));
    let offset = start + length;
    for (let i=0;i<section;i++) offset += (view.getUint32(12+4*i,true)+3)&~3;
    const rgba = new Uint8Array(buffer,offset,width*height*4);
    const pixel=(x:number,y:number)=>[...rgba.slice((y*width+x)*4,(y*width+x)*4+3)];
    const cols = archived ? [2,10,20,27] : [2,10,62,70,90];
    console.log(JSON.stringify({name, listed:listed.includes(badge), resources:resources.length,
      samples:cols.map(x=>[x, [2,10,25,46].map(y=>pixel(x,y))])}));
  } finally { ffi.symbols.web_render_free(q); }
}
