
type Icon = { category: string; icon: string; original: string; control: string };
const [baselinePath, candidatePath, fixture] = Deno.args;
const { url, nodes } = JSON.parse(await Deno.readTextFile(fixture)) as { url: string; nodes: Icon[] };
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
const baseline = openNative(baselinePath);
const candidate = openNative(candidatePath);
const width = 192;
const height = 80;
const request = JSON.stringify({
  op: "render", url, liberal: true, scripting: false, checks: false, partialNote: false, diagnostics: true, cpu: true,
});
async function render(engine: typeof baseline, markup: string) {
  const html = `<!doctype html><style>body{margin:8px;background:#aaa;color:#222}
    svg{width:112px;height:48px;display:block}</style>${markup}`;
  const buffer = engine(html, request, width, height);
  const { head, sections } = unpackAnswer(buffer);
  if (head.error) throw Error(String(head.error));
  const page = (head.page ?? head) as Record<string, unknown>;
  const diagnostics = (page.diagnostics ?? head.diagnostics ?? []) as { message?: string }[];
  const index = page.pixelsSection;
  if (typeof index !== "number") throw Error("Render returned no pixels");
  const [offset, size] = sections[index];
  if (size !== width * height * 4) throw Error("Unexpected raster size");
  const digest = await crypto.subtle.digest("SHA-256", new Uint8Array(buffer, offset, size));
  return {
    pixels: Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, "0")).join(""),
    labelSkip: diagnostics.some(({ message }) => /unsupported attribute on svg: (category|icon)$/.test(message ?? "")),
    messages: diagnostics.map(({ message }) => message),
  };
}
const blank = await render(candidate, "");
let visibleRecovered = 0;
let baselineSkips = 0;
for (const { category, icon, original, control } of nodes) {
  const old = await render(baseline, original);
  const fixed = await render(candidate, original);
  const expected = await render(candidate, control);
  const visible = fixed.pixels !== old.pixels && fixed.pixels !== blank.pixels;
  console.log(JSON.stringify({ category, icon, old, fixed, expected, visible }));
  if (old.labelSkip) baselineSkips++;
  if (fixed.labelSkip || fixed.pixels !== expected.pixels) {
    throw Error(`Unexpected result for ${category}/${icon}`);
  }
  if (visible) visibleRecovered++;
}
console.log(JSON.stringify({ compared: nodes.length, baselineSkips, visibleRecovered }));
if (!baselineSkips) throw Error("The baseline did not reproduce the SVG metadata rejection");
if (!visibleRecovered) throw Error("The change did not recover any visible icons");
