// Measure the same script-visible node with and without the ordinary static image bytes.
import { loadHTML } from "../../labs/demos/foafnaut/native_html_engine.ts";
import { imageOptions } from "../../labs/demos/foafnaut/native_html_document.ts";

const [library, png] = Deno.args;
const engine = await loadHTML(library);
const url = "http://web-platform.test/controlled-image.html";
const key = "/images/green-256x256.png";
const html = `<!doctype html><div><img id="plain" src="${key}"></div>
<div><img id="empty" alt="" src="/absent.png"></div><div><span id="label">[image]</span></div>
<script>onload=function(){
  function box(id){var r=document.getElementById(id).getBoundingClientRect();return [r.width,r.height]}
  var i=document.getElementById("plain");console.log("__size "+JSON.stringify({width:i.width,height:i.height,
    box:box("plain"),empty:box("empty"),label:box("label")}));
}</script>`;
const images = (engine.inspect(html, { url }) as unknown as {
  images: { url: string; key: string }[];
}).images;
const first = images.find((i) => new URL(i.url, url).pathname === key);
if (!first) throw new Error("inspection omitted the static PNG");
const results = [];
for (const withImage of [false, true]) {
  const fields = withImage
    ? await imageOptions(engine, [{
      key: first.key,
      bytes: await Deno.readFile(png),
    }])
    : {};
  const turn = engine.scriptSession(html, {
    action: "start",
    engine: "bubblepop",
    url,
    resources: [],
    ...(withImage ? { layout: { url, ...fields } } : {}),
  });
  const after = engine.scriptSession("", {
    action: "settle",
    session: turn.session,
    budgetMs: 1000,
  });
  engine.scriptSession("", { action: "close" });
  const line = [...turn.logs, ...after.logs].find((x) =>
    x.startsWith("__size ")
  );
  if (!line) {
    throw new Error(
      "script produced no metrics: " +
        JSON.stringify([...turn.errors, ...after.errors]),
    );
  }
  results.push({ withImage, ...JSON.parse(line.slice(7)) });
}
console.log(JSON.stringify({ url, pngKey: first.key, results }));
if (
  results[0].width === 256 || results[1].width !== 256 ||
  results[1].height !== 256
) {
  throw new Error(
    "supplying the exact loaded PNG did not distinguish the two measurements",
  );
}
