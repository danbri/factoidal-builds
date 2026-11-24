const [library, directory, mode] = Deno.args;
const encoder = new TextEncoder();
const decoder = new TextDecoder();
function openNative(path: string) {
  const ffi = Deno.dlopen(path, {
    web_document_call_bin: { parameters: ["buffer", "buffer", "u32", "u32", "buffer"], result: "pointer" },
    web_render_free: { parameters: ["pointer"], result: "void" },
  } as const);
  const size = new Uint32Array(1);
  return (html: string, options: string, width: number, height: number) => {
    const pointer = ffi.symbols.web_document_call_bin(encoder.encode(html + "\0"),
      encoder.encode(options + "\0"), width, height, size);
    if (!pointer) throw Error("Native renderer returned no buffer");
    try { return Deno.UnsafePointerView.getArrayBuffer(pointer, size[0]).slice(0); }
    finally { ffi.symbols.web_render_free(pointer); }
  };
}
function unpackAnswer(buffer: ArrayBuffer) {
  const view = new DataView(buffer);
  if (view.getUint32(0, true) !== buffer.byteLength) throw Error("Invalid renderer answer");
  const headLength = view.getUint32(4, true);
  const sectionCount = view.getUint32(8, true);
  let offset = 12 + 4 * sectionCount;
  const head = JSON.parse(decoder.decode(new Uint8Array(buffer, offset, headLength)));
  offset += headLength;
  const sections: [number, number][] = [];
  for (let index = 0; index < sectionCount; index++) {
    const length = view.getUint32(12 + 4 * index, true);
    sections.push([offset, length]);
    offset += (length + 3) & ~3;
  }
  return { head, sections };
}
const render = openNative(library);
const viewport = { width: 100, height: 80 };
const request = JSON.stringify({
  op: "render", url: "https://fixture.test/cascade", liberal: true, scripting: false,
  checks: false, partialNote: false, diagnostics: true, cpu: true,
});
const cases = JSON.parse(await Deno.readTextFile(directory + "/cases.json")) as { id: string; want: string }[];
let passed = 0;
for (const { id, want } of cases) {
  const source = await Deno.readTextFile(directory + "/" + id + ".html");
  const buffer = render(source, request, viewport.width, viewport.height);
  const { head, sections } = unpackAnswer(buffer);
  const page = head.page ?? head;
  if (head.error || typeof page.pixelsSection !== "number") throw Error(String(head.error ?? "No pixels"));
  const [offset, size] = sections[page.pixelsSection];
  if (size !== viewport.width * viewport.height * 4) throw Error("Unexpected raster size");
  const rgba = new Uint8Array(buffer, offset + (32 * viewport.width + 32) * 4, 4);
  const pixel = "#" + Array.from(rgba.subarray(0, 3), b => b.toString(16).padStart(2, "0")).join("");
  const pass = pixel === want && rgba[3] === 255;
  if (pass) passed++;
  console.log(JSON.stringify({ id, pixel, alpha: rgba[3], want, pass, diagnostics: page.diagnostics ?? head.diagnostics ?? [] }));
}
console.log(JSON.stringify({ passed, total: cases.length }));
if (mode === "require-pass" && passed !== cases.length) Deno.exit(1);
