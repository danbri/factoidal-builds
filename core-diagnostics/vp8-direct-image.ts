const [library, webpPath, pngPath] = Deno.args;
const ffi = Deno.dlopen(library, {
  web_document_call: { parameters: ["buffer", "buffer", "u32", "u32"], result: "pointer" },
  web_document_call_bin: { parameters: ["buffer", "buffer", "u32", "u32", "buffer"], result: "pointer" },
  web_render_free: { parameters: ["pointer"], result: "void" },
} as const);
const encoder = new TextEncoder();
const decoder = new TextDecoder();
const asCString = (s: string) => encoder.encode(s + "\0");
const base64 = async (file: string) => btoa(String.fromCharCode(...await Deno.readFile(file)));
const webp = await base64(webpPath);
const png = await base64(pngPath);
function icon(bytes: string) {
  const pointer = ffi.symbols.web_document_call(asCString(""), asCString(JSON.stringify({
    op: "iconPrepare", base64: bytes, scale: 1,
  })), 64, 64);
  if (!pointer) throw Error("No tab icon response");
  try {
    const output = JSON.parse(new Deno.UnsafePointerView(pointer).getCString());
    if (output.kind !== "bitmap") throw Error(JSON.stringify(output));
    return {width: output.width, height: output.height, rgba: output.rgba};
  } finally {
    ffi.symbols.web_render_free(pointer);
  }
}
const gotIcon = icon(webp);
const pngIcon = icon(png);
if (JSON.stringify(gotIcon) !== JSON.stringify(pngIcon)) throw Error("WebP icon did not match PNG");
console.log(JSON.stringify({kind: "icon", width: gotIcon.width, height: gotIcon.height, equalToPng: true}));

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
const blank = pixels("");
for (const [kind, image] of [
  ["html-image", (uri: string) => `<img src="${uri}" width="32" height="32" alt="WEBPALT">`],
  ["picture-source", (uri: string) => `<picture><source srcset="${uri}"><img width="32" height="32" alt="WEBPALT"></picture>`],
  ["html-object", (uri: string) => `<object data="${uri}" width="32" height="32"></object>`],
  ["svg-image", (uri: string) => `<svg width="32" height="32"><image href="${uri}" width="32" height="32"/></svg>`],
  ["css-background", (uri: string) => `<div style="width:32px;height:32px;background-image:url(${uri});background-size:32px 32px"></div>`],
] as const) {
  const native = pixels(image("data:image/webp;base64," + webp));
  const reference = pixels(image("data:image/png;base64," + png));
  if (equal(native, blank) || !equal(native, reference)) throw Error(`WebP did not match a visibly rendered PNG for ${kind}`);
  console.log(JSON.stringify({kind, equalToPng: true}));
}
