const [host, engine, out] = Deno.args;
if (!host || !engine || !out) throw Error("Expected host directory, engine and output directory");
await Deno.mkdir(out, { recursive: true });

const form = `<!doctype html><title>Search fixture</title>
<style>
body { margin: 0 }
.row::after { content: ""; display: block; clear: both }
.unrelated:has(> :not([hidden])) { margin-bottom: 12px }
.column { float: left; width: 630px; height: 90px }
.table { display: table; width: 100% }
.cell { display: table-cell }
.submit { width: 1% }
input { box-sizing: border-box; width: 100%; height: 50px }
button { width: 50px; height: 50px }
.next { position: relative; background: white; height: 90px }
</style>
<div class="row">
  <form class="column" action="/results" method="get">
    <label for="keyword">Search</label>
    <div class="table">
      <div><input type="search" class="cell" id="keyword" name="keywords"></div>
      <div class="cell submit"><button type="submit">Go</button></div>
    </div>
  </form>
</div>
<div class="next">Following section</div>`;

const query = "public services";
const received: string[] = [];
const server = Deno.serve({hostname: "127.0.0.1", port: 0, onListen() {}}, (request) => {
  const url = new URL(request.url);
  if (url.pathname === "/search") return new Response(form, {headers: {"content-type": "text/html; charset=utf-8"}});
  if (url.pathname !== "/results") return new Response("Not found", {status: 404});
  const keyword = url.searchParams.get("keywords") ?? "";
  const valid = request.method === "GET" && keyword === query;
  if (valid) received.push(keyword);
  const title = valid ? "Results: public services" : "Unexpected request";
  return new Response(`<!doctype html><title>${title}</title><h1>${title}</h1>`, {
    headers: {"content-type": "text/html; charset=utf-8"},
  });
});

try {
  const cases = [
    {name: "enter", submit: [5, 36, 0]},
    {name: "button", submit: "tap:598,45"},
  ];
  let failed = 0;
  for (const {name, submit} of cases) {
    const steps = `${out}/${name}-steps.json`;
    const before = received.length;
    await Deno.writeTextFile(steps, JSON.stringify([
      "title=Search fixture", "hold", "tap:240,45", "hold", `type:${query}`, submit,
      "title=Results: public services",
    ]));
    const browser = [Deno.execPath(), "run", "--no-check",
      "--no-config", "--no-npm", "--node-modules-dir=none", "--unstable-webgpu", "--unstable-ffi", "-A",
      `${host}/run_html.ts`];
    const child = await new Deno.Command("perl", {args: [
      "-e", "alarm shift; exec @ARGV", "90", ...browser, "--offscreen", "--offscreen-size", "1280x800@1", "--no-state",
      "--no-scripts", "--follow-links", "--native-engine", engine, "--url",
      `http://127.0.0.1:${server.addr.port}/search`, "--steps", steps,
      "--shot", `${out}/${name}.png`, "--shot-at-end",
    ]}).output();
    await Deno.writeFile(`${out}/${name}.stdout.log`, child.stdout);
    await Deno.writeFile(`${out}/${name}.stderr.log`, child.stderr);
    const passed = child.success && received.length === before + 1;
    console.log(JSON.stringify({case: name, passed, exit: child.code, matchingRequests: received.length - before}));
    if (!passed) failed++;
  }
  if (failed) Deno.exitCode = 1;
} finally {
  await server.shutdown();
}
