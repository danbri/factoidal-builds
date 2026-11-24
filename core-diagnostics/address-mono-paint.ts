const [library, fontPath, output] = Deno.args;
const ffi = Deno.dlopen(library, {
  web_document_call: { parameters: ["buffer", "buffer", "u32", "u32"], result: "pointer" },
  web_document_call_bin: { parameters: ["buffer", "buffer", "u32", "u32", "buffer"], result: "pointer" },
  web_document_font_call_bin: { parameters: ["buffer", "u32", "buffer", "buffer", "u32"], result: "pointer" },
  web_render_free: { parameters: ["pointer"], result: "void" },
} as const);
const encoder = new TextEncoder();
const decoder = new TextDecoder();
const cs = (s: string) => encoder.encode(s + "\0");
const width = 640;
const shell = {
  address: "https://example.org/Quick-fix?q=42", tabs: [{ title: "Example" }],
  theme: "light", scale: 1, focus: true, focused: true, cursor: 13, anchor: 4,
};
function getJSON(pointer: Deno.PointerValue) {
  if (!pointer) throw Error("The native engine returned a null pointer");
  try {
    const value = JSON.parse(new Deno.UnsafePointerView(pointer).getCString());
    if (value.error) throw Error(value.error);
    return value;
  } finally {
    ffi.symbols.web_render_free(pointer);
  }
}
function pixels() {
  const size = new Uint32Array(1);
  const request = cs(JSON.stringify({ op: "chromeLayer", shell, checks: false, cpu: true }));
  const ptr = ffi.symbols.web_document_call_bin(cs(""), request, width, 120, size);
  if (!ptr) throw Error("No native chrome response");
  try {
    const buffer = Deno.UnsafePointerView.getArrayBuffer(ptr, size[0]);
    const view = new DataView(buffer);
    if (view.getUint32(0, true) !== size[0]) throw Error("Unrecognised binary response");
    const jsonSize = view.getUint32(4, true);
    const count = view.getUint32(8, true);
    const start = 12 + 4 * count;
    const result = JSON.parse(decoder.decode(new Uint8Array(buffer, start, jsonSize)));
    const part = result.chrome?.pixelsSection;
    const height = result.top;
    if (result.error || !Number.isInteger(part) || !Number.isInteger(height)) throw Error(JSON.stringify(result));
    let offset = start + jsonSize;
    for (let i = 0; i < part; i++) offset += (view.getUint32(12 + 4 * i, true) + 3) & ~3;
    const length = view.getUint32(12 + 4 * part, true);
    if (length !== 4 * width * height) throw Error("Wrong native chrome pixel count");
    return { height, rgba: new Uint8Array(buffer, offset, length).slice() };
  } finally {
    ffi.symbols.web_render_free(ptr);
  }
}
function hits() {
  return [4, 45, 115, 157, 280, 560, 630].map((x) =>
    getJSON(ffi.symbols.web_document_call(cs(""), cs(JSON.stringify({
      op: "shellHit", shell, x, y: 43, width,
    })), width, 120)).control);
}
function ppm(height: number, rgba: Uint8Array, path: string) {
  const header = encoder.encode(`P6\n${width} ${height}\n255\n`);
  const file = new Uint8Array(header.length + 3 * width * height);
  file.set(header);
  for (let i = 0; i < width * height; i++) file.set(rgba.subarray(i * 4, i * 4 + 3), header.length + i * 3);
  Deno.writeFileSync(path, file);
}
const priorHits = hits();
const before = pixels();
const font = Deno.readFileSync(fontPath);
const hash = [...new Uint8Array(await crypto.subtle.digest("SHA-256", font))]
  .map((byte) => byte.toString(16).padStart(2, "0")).join("");
const held = getJSON(ffi.symbols.web_document_font_call_bin(font, font.length, cs("Liberation Mono"), cs(hash), 4));
if (held.mono !== "Liberation Mono") throw Error(`The mono face did not load: ${JSON.stringify(held)}`);
const after = pixels();
if (after.height !== before.height || JSON.stringify(hits()) !== JSON.stringify(priorHits)) {
  throw Error("Loading the font moved chrome interaction geometry");
}
let changed = 0;
for (let row = 0; row < before.height; row++) {
  for (let col = 0; col < width; col++) {
    const offset = (row * width + col) * 4;
    if (before.rgba.subarray(offset, offset + 4).every((byte, c) => after.rgba[offset + c] === byte)) continue;
    if (row < 26 || row >= 62) throw Error(`The address font changed a pixel outside the toolbar at ${col}, ${row}`);
    changed++;
  }
}
if (changed === 0) throw Error("Loading the mono face did not change any painted address pixels");
Deno.mkdirSync(output, { recursive: true });
ppm(before.height, before.rgba, output + "/address-bitmap.ppm");
ppm(after.height, after.rgba, output + "/address-liberation-mono.ppm");
console.log(JSON.stringify({ font: held.mono, sha256: hash, changed, hits: priorHits }));
