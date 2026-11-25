const lib = Deno.args[0];
const ffi = Deno.dlopen(lib, {
  web_document_call_bin: { parameters:["buffer","buffer","u32","u32","buffer"], result:"pointer" },
  web_render_free: { parameters:["pointer"], result:"void" },
} as const);
const width = 160, height = 80;
const enc = new TextEncoder(), dec = new TextDecoder();
const bytes = (s: string) => enc.encode(s + "\0");
function raster(radius: string) {
  const img = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAIAAACRXR/mAAAAQ0lEQVR4nO3OMQ0AMAwDsPAnvRHonxyWDMDJy6L+QEtLS0tLa0N/oKWlpaWltaE/0NLS0tLS2tAfaGlpaWlpbegPLh/AWbrEDESjlAAAAABJRU5ErkJggg==";
  const html = `<!doctype html><style>html{background:#000}body{margin:0}
.sample{position:absolute;top:10px;width:50px;height:50px;padding:5px;border-radius:${radius}}
div.sample{left:10px;background:#fff}img.sample{left:85px;background:#fff}</style>
<div class="sample"></div><img class="sample" src="${img}">`;
  const size = new Uint32Array(1);
  const request = bytes(JSON.stringify({op:"render", cpu:true, checks:false, liberal:true, partialNote:false, images:[{key:img,base64:img.split(",")[1]}]}));
  const ptr = ffi.symbols.web_document_call_bin(bytes(html), request, width, height, size);
  if (!ptr) throw Error("native renderer returned nothing");
  try {
    const buffer = Deno.UnsafePointerView.getArrayBuffer(ptr, size[0]);
    const view = new DataView(buffer);
    const start = 12 + 4 * view.getUint32(8, true);
    const length = view.getUint32(4, true);
    const result = JSON.parse(dec.decode(new Uint8Array(buffer, start, length)));
    const section = result.pixelsSection;
    if (result.error || !Number.isInteger(section)) throw Error(JSON.stringify(result).slice(0, 500));
    let offset = start + length;
    for (let i = 0; i < section; i++) offset += (view.getUint32(12 + 4 * i, true) + 3) & ~3;
    const rgba = new Uint8Array(buffer, offset, width * height * 4).slice();
    const pixel = (x: number, y: number) => [...rgba.slice((y * width + x) * 4, (y * width + x) * 4 + 4)];
    return {radius, backgroundCorner:pixel(11,11), imageBackgroundCorner:pixel(86,11),
      imageContentCorner:pixel(91,16), imageCenter:pixel(115,40), rgba};
  } finally { ffi.symbols.web_render_free(ptr); }
}
const square = raster("0"), round = raster("50%");
for (const {rgba: _, ...samples} of [square, round]) console.log(JSON.stringify(samples));
const difference = square.rgba.reduce((n, channel, i) => n + Number(channel !== round.rgba[i]), 0);
if (round.imageCenter.join(",") !== "0,255,0,255") throw Error("image fixture did not render");
console.log(JSON.stringify({changedChannels:difference}));

const pixelIs = (value: number[], expected: string) => value.join(",") === expected;
const white = "255,255,255,255", black = "0,0,0,255", green = "0,255,0,255";
if (!pixelIs(square.backgroundCorner, white) || !pixelIs(square.imageBackgroundCorner, white) ||
    !pixelIs(square.imageContentCorner, green)) throw Error("zero-radius control changed");
if (Deno.args[1] === "candidate") {
  if (!pixelIs(round.backgroundCorner, black) || !pixelIs(round.imageBackgroundCorner, black) ||
      pixelIs(round.imageContentCorner, green)) throw Error("rounded paint did not clip all corners");
} else if (difference !== 0) throw Error("baseline radius unexpectedly changed paint");
