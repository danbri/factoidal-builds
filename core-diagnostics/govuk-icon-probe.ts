const [library, input] = Deno.args;
const ffi = Deno.dlopen(library, {
  web_document_call: {parameters:["buffer","buffer","u32","u32"],result:"pointer"},
  web_document_call_bin: {parameters:["buffer","buffer","u32","u32","buffer"],result:"pointer"},
  web_render_free: {parameters:["pointer"],result:"void"},
} as const);
const encoder = new TextEncoder();
const decoder = new TextDecoder();
const width = 100;
const height = 80;
const documentURL = "https://www.gov.uk/";
const pageCSS = "body{margin:8px;background:white}svg{width:54px;height:54px;display:block}";
const icons = {
  plain: "",
  descendant: ".gem-c-action-link__svg .gem-c-action-link__icon__circle{fill:#d2e2f1}",
  direct: ".gem-c-action-link__icon__circle{fill:#d2e2f1}",
};
const html = await Deno.readTextFile(input);
const svg = html.match(/<svg\b[^>]*class="gem-c-action-link__svg"[^>]*>[\s\S]*?<\/svg>/i)?.[0];
if (!svg) throw Error("GOV.UK icon missing");
const size = new Uint32Array(1);
for (const [label, sheet, node, resources] of [
  ["no-css", icons.plain, svg, []],
  ["html-descendant", icons.descendant, svg, []],
  ["html-direct", icons.direct, svg, []],
  ["svg-direct", "", svg.replace(">", `><style>${icons.direct}</style>`), []],
  ["presentation-attribute", "", svg.replace("<circle ", '<circle fill="#d2e2f1" '), []],
  ["external-descendant", '<link rel="stylesheet" href="/test.css">', svg,
    [{url:"https://www.gov.uk/test.css",source:icons.descendant}]],
] as const) {
  const source = `<!doctype html><style>${pageCSS}${sheet.startsWith("<") ? "" : sheet}</style>
    ${sheet.startsWith("<") ? sheet : ""}${node}`;
  const cstring = (s: string) => encoder.encode(s + "\0");
  const inspect = ffi.symbols.web_document_call(cstring(source), cstring(JSON.stringify({op:"inspect",url:documentURL,liberal:true})), width, height);
  if (!inspect) throw Error("No native inspector result");
  const listed = JSON.parse(new Deno.UnsafePointerView(inspect).getCString()).stylesheets;
  ffi.symbols.web_render_free(inspect);
  const matched = listed.flatMap((entry: {url:string}) => resources.filter(r=>r.url === entry.url).map(r=>({...entry,...r})));
  if (resources.length !== matched.length) throw Error("External stylesheet fixture missing");
  const request = {op:"render",url:documentURL,liberal:true,scripting:false,checks:false,partialNote:false,cpu:true,resources:matched};
  const ptr = ffi.symbols.web_document_call_bin(encoder.encode(source + "\0"),encoder.encode(JSON.stringify(request) + "\0"),width,height,size);
  if (!ptr) throw Error("No native renderer result");
  try {
    const answer = Deno.UnsafePointerView.getArrayBuffer(ptr,size[0]);
    const view = new DataView(answer);
    if (view.getUint32(0,true) !== size[0]) throw Error("Invalid native renderer buffer");
    const headLength = view.getUint32(4,true);
    const sectionCount = view.getUint32(8,true);
    const headEnd = 12 + 4 * sectionCount + headLength;
    const head = JSON.parse(decoder.decode(new Uint8Array(answer,headEnd - headLength,headLength)));
    const page = head.page ?? head;
    if (head.error || typeof page.pixelsSection !== "number") throw Error(JSON.stringify(head.error ?? head));
    let offset = headEnd;
    for (let i = 0; i < page.pixelsSection; i++) offset += (view.getUint32(12 + 4*i,true) + 3) & ~3;
    const pixels = new Uint8Array(answer,offset,width*height*4);
    let sky = 0, black = 0;
    for (let i = 0; i < pixels.length; i += 4) {
      if (pixels[i] === 210 && pixels[i+1] === 226 && pixels[i+2] === 241 && pixels[i+3] === 255) sky++;
      if (pixels[i] === 0 && pixels[i+1] === 0 && pixels[i+2] === 0 && pixels[i+3] === 255) black++;
    }
    console.log(JSON.stringify({label,sky,black,diagnostics:page.diagnostics ?? head.diagnostics ?? []}));
  } finally {
    ffi.symbols.web_render_free(ptr);
  }
}
