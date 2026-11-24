import { nativeBackends, unpackAnswer } from "../core/labs/demos/foafnaut/native_html_engine.ts";

type Icon = { category: string; icon: string; original: string; control: string };
const [baselinePath, candidatePath, fixture] = Deno.args;
const { url, nodes } = JSON.parse(await Deno.readTextFile(fixture)) as { url: string; nodes: Icon[] };
const baseline = nativeBackends(baselinePath).bytes;
const candidate = nativeBackends(candidatePath).bytes;
const width = 192;
const height = 80;
const request = JSON.stringify({
  op: "render", url, liberal: true, scripting: false, checks: false, partialNote: false, cpu: true,
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
    categorySkip: diagnostics.some(({ message }) => message?.includes("unsupported attribute on svg: category")),
    messages: diagnostics.map(({ message }) => message),
  };
}
const blank = await render(candidate, "");
let visibleRecovered = 0;
for (const { category, icon, original, control } of nodes) {
  const old = await render(baseline, original);
  const fixed = await render(candidate, original);
  const expected = await render(candidate, control);
  const visible = fixed.pixels !== old.pixels && fixed.pixels !== blank.pixels;
  console.log(JSON.stringify({ category, icon, old, fixed, expected, visible }));
  if (!old.categorySkip || fixed.categorySkip || fixed.pixels !== expected.pixels) {
    throw Error(`Unexpected result for ${category}/${icon}`);
  }
  if (visible) visibleRecovered++;
}
console.log(JSON.stringify({ compared: nodes.length, visibleRecovered }));
if (!visibleRecovered) throw Error("The change did not recover any visible icons");
