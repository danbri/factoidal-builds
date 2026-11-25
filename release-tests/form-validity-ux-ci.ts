const [engine, guest, out] = Deno.args;
if (!engine || !guest || !out) throw new Error("usage: form-validity-ux-ci.ts ENGINE QUICKJS_WASM OUTPUT");

const host = new URL("./source/labs/demos/foafnaut/run_html.ts", import.meta.url).pathname;
const title = "Required name fixture";
const fixture = `<!doctype html>
<meta charset="utf-8"><title>${title}</title>
<style>
  body { margin: 0; background: white; }
  #panel { position: absolute; left: 32px; top: 24px; width: 336px; height: 140px;
    background: #e4139a; }
  label { position: absolute; left: 16px; top: 12px; font: 20px sans-serif; }
  input { position: absolute; left: 16px; top: 44px; width: 252px; height: 40px;
    border: 6px solid #444444; background: white; color: black; font: 20px sans-serif; }
  input:invalid { border-color: #d52b35; }
  input:valid { border-color: #117742; }
  p { position: absolute; left: 16px; top: 95px; font: 14px sans-serif; }
</style>
<form id="panel">
  <label for="name">Name (required)</label>
  <input id="name" name="name" type="text" required>
  <p>Red means required. Green means complete.</p>
</form>
<script>
  const field = document.getElementById("name");
  function report(phase) {
    const validity = field.validity;
    console.log("validity-ux-dom " + JSON.stringify({
      phase, value: field.value, willValidate: field.willValidate, customError: validity.customError,
      valueMissing: validity.valueMissing, valid: validity.valid,
      matchesInvalid: field.matches(":invalid"), matchesValid: field.matches(":valid")
    }));
  }
  report("initial");
  field.addEventListener("input", () => {
    const tooShort = field.value.length === 1;
    field.setCustomValidity(tooShort ? "Name needs two letters" : "");
    report(tooShort ? "customError" : "cleared");
  });
</script>`;

const server = Deno.serve({ hostname: "127.0.0.1", port: 0, onListen() {} }, (request) =>
  new URL(request.url).pathname === "/fixture"
    ? new Response(fixture, { headers: { "content-type": "text/html; charset=UTF-8", "cache-control": "no-store" } })
    : new Response("Not found", { status: 404 })
);
const url = `http://127.0.0.1:${server.addr.port}/fixture`;

const initial = {
  phase: "initial", value: "", willValidate: true, customError: false, valueMissing: true, valid: false,
  matchesInvalid: true, matchesValid: false,
};
const customError = {
  phase: "customError", value: "a", willValidate: true, customError: true, valueMissing: false,
  valid: false, matchesInvalid: true, matchesValid: false,
};
const cleared = {
  phase: "cleared", value: "ab", willValidate: true, customError: false, valueMissing: false,
  valid: true, matchesInvalid: false, matchesValid: true,
};
type Event = {
  type?: string;
  title?: string;
  url?: string;
  ok?: boolean;
  engine?: string;
  state?: string;
  default?: string;
  cause?: string;
};
function parse<T>(line: string): T[] {
  try { return [JSON.parse(line) as T]; } catch { return []; }
}
const rows: { pass: boolean }[] = [];
try {
  await Deno.writeTextFile(`${out}/fixture.html`, fixture);
  for (const [name, type] of [["before", false], ["after", true]] as const) {
    const path = `${out}/${name}`;
    const steps = [`title=${title}`, "hold", "tap:100,90", "hold", "type:a", "hold"];
    if (type) steps.push("type:b", "hold");
    await Deno.writeTextFile(path + ".json", JSON.stringify(steps));
    const result = await new Deno.Command("timeout", {
      args: [
        "145", "deno", "run", "--no-check", "--no-config", "--no-npm", "--node-modules-dir=none",
        "--unstable-webgpu", "--unstable-ffi", "-A", host, "--offscreen", "--idle-checks-only",
        "--no-spare-engine-worker", "--no-state", "--follow-links", "--offscreen-size", "640x480@1",
        "--text-size", "100", "--native-engine", engine, "--quickjs-wasm", guest, "--url", url,
        "--steps", path + ".json", "--shot", path + ".png", "--shot-at-end",
      ],
      stdout: "piped",
      stderr: "piped",
    }).output();
    const decode = new TextDecoder();
    const log = decode.decode(result.stdout) + "\n" + decode.decode(result.stderr);
    await Deno.writeTextFile(path + ".log", log);
    const lines = log.split("\n");
    const events = lines.filter((line) => line.startsWith("{")).flatMap(parse<Event>);
    const dom = lines.flatMap((line) => {
      const entry = /^page: .*?validity-ux-dom (\{.*\})$/.exec(line);
      return entry ? parse<typeof initial>(entry[1]) : [];
    });
    const browser = events.findLast((event) => event.type === "native-html-engine")?.engine === "native " + engine;
    const scripts = events.some((event) => event.type === "native-html-scripts" &&
      event.state === "on" && event.default === "bubblepop") &&
      events.some((event) => event.type === "native-html-script" && event.cause === "start" && event.engine === "bubblepop");
    const opened = events.some((event) => event.type === "native-html-test-title" &&
      event.ok && event.title === title && event.url === url);
    const shot = events.some((event) => event.type === "native-html-shot");
    const stateMatches = JSON.stringify(dom) === JSON.stringify(type ? [initial, customError, cleared] : [initial, customError]);
    const pass = result.code === 0 && browser && scripts && opened && shot && stateMatches;
    const row = { name, pass, exit: result.code, browser, scripts, opened, shot, stateMatches, dom };
    rows.push(row);
    console.log(JSON.stringify(row));
  }
} finally {
  await server.shutdown();
  await Deno.writeTextFile(`${out}/browser-results.json`, JSON.stringify(rows, null, 2) + "\n");
}
if (rows.some((row) => !row.pass)) Deno.exitCode = 1;
