const [library] = Deno.args;
const ffi = Deno.dlopen(library, {
  web_document_call: { parameters: ["buffer", "buffer", "u32", "u32"], result: "pointer" },
  web_document_call_bin: { parameters: ["buffer", "buffer", "u32", "u32", "buffer"], result: "pointer" },
  web_render_free: { parameters: ["pointer"], result: "void" },
} as const);
const encoder = new TextEncoder();
const decoder = new TextDecoder();
const asCString = (s: string) => encoder.encode(s + "\0");
function pixels(body: string) {
  const source = "<!doctype html><style>body{margin:0;background:white}</style>" + body;
  const request = JSON.stringify({ op: "render", url: "https://fixture.test/", checks: false,
    liberal: true, diagnostics: true, cpu: true, partialNote: false });
  const size = new Uint32Array(1);
  const ptr = ffi.symbols.web_document_call_bin(asCString(source), asCString(request), 64, 64, size);
  if (!ptr) throw Error("No native scene response");
  try {
    const buffer = Deno.UnsafePointerView.getArrayBuffer(ptr, size[0]);
    const view = new DataView(buffer);
    if (view.getUint32(0, true) !== size[0]) throw Error("Unrecognized binary scene");
    const jsonLength = view.getUint32(4, true);
    const count = view.getUint32(8, true);
    const start = 12 + 4*count;
    const head = JSON.parse(decoder.decode(new Uint8Array(buffer, start, jsonLength)));
    const page = head.page ?? head;
    if (head.error || typeof page.pixelsSection !== "number") throw Error(JSON.stringify(head));
    let offset = start + jsonLength;
    for (let i = 0; i < page.pixelsSection; i++) offset += (view.getUint32(12 + 4*i, true) + 3) & ~3;
    const length = view.getUint32(12 + 4*page.pixelsSection, true);
    if (length !== 64 * 64 * 4) throw Error("Unexpected RGBA size");
    return new Uint8Array(buffer, offset, length).slice();
  } finally {
    ffi.symbols.web_render_free(ptr);
  }
}
const equal = (a: Uint8Array, b: Uint8Array) => a.every((byte, i) => byte === b[i]);

for (const kind of ["block","inline-block","pseudo-element","govuk-menu"]) {
  function fixture(transform: string) {
    if (kind === "govuk-menu") {
      return pixels(`<style>
        body{background:#1d70b8}
        .toggle{margin:20px;color:white}
        .toggle .inner::before{border-bottom:2px solid #fff;border-right:2px solid #fff;
          content:"";display:inline-block;height:8px;margin:0 10px 0 2px;
          vertical-align:middle;width:8px;${transform}}
        </style><div class="toggle"><span class="inner">Menu</span></div>`);
    }
    const selector = kind === "pseudo-element" ? "#owner::before" : "#mark";
    const display = kind === "block" ? "block" : "inline-block";
    const style = `${selector}{content:"";display:${display};width:8px;height:8px;
      border-right:2px solid black;border-bottom:2px solid black;
      ${transform}}`;
    const markup = kind === "pseudo-element"
      ? '<div id="owner" style="margin:20px">Menu</div>'
      : kind === "block" ? '<div id="mark" style="margin:20px;background:red">X</div>' : '<div style="margin:20px"><span id="mark"></span>Menu</div>';
    return pixels("<style>"+style+"</style>"+markup);
  }

  const plain = fixture("");
  for(const trial of ["translate(10px,3px)", "rotate(45deg)", "translateY(-35%) rotate(45deg) scale(1)"]) {
    if (kind === "govuk-menu" && !trial.startsWith("translateY")) continue;
    const turned = fixture("transform:" + trial);
    const changed = plain.reduce((sum,c,i) => sum + Number(i%4===0 && c!==turned[i]),0);
    const ink=(b:Uint8Array)=>b.reduce((sum,c,i) => sum + Number(i%4===0 && c<100),0);
    console.log(JSON.stringify({kind, trial, changed, inkBefore:ink(plain), inkAfter:ink(turned), byteIdentical:equal(plain,turned)}));
  }
}
