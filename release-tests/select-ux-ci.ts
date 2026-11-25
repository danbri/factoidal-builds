const [engine, guest, out] = Deno.args;
if (!engine || !guest || !out) throw new Error("usage: select-ux-ci.ts ENGINE QUICKJS_WASM OUTPUT");
const host = new URL("./source/labs/demos/foafnaut/run_html.ts", import.meta.url).pathname;
const chosenValue = "wrapped value";
const initialTitle = "Select submission fixture";
const resultTitle = "Select submission received";
const expectedFields = [["choice", chosenValue]];

type Variant = "wrapped" | "reference" | "different";
type Method = "GET" | "POST";
type Receipt = {
  method: string;
  endpoint: string;
  query: string;
  body: string;
  contentType: string | null;
  fields: string[][];
};
const receipts: Receipt[] = [];

const css = `
  body { margin: 0; background: white; }
  #panel { position: absolute; left: 32px; top: 24px; width: 300px; height: 74px;
    background: #e4139a; padding: 12px; }
  select { display: block; width: 242px; height: 36px; color: black; background: white;
    font: 20px sans-serif; }
  button { position: absolute; left: 32px; top: 145px; width: 128px; height: 42px; }
`;

const prepareSelect = `
const form = document.getElementById("form");
const select = document.getElementById("choice");
const wrapper = document.createElement("div");
const group = document.createElement("optgroup");
group.setAttribute("label", "Included group");
const wrapped = document.createElement("option");
wrapped.setAttribute("value", "wrapped value");
wrapped.textContent = "Wrapped office";
group.appendChild(wrapped);
wrapper.appendChild(group);
select.appendChild(wrapper);
select.value = "wrapped value";

const boundary = document.createElement("datalist");
const blocked = document.createElement("option");
blocked.setAttribute("value", "outside value");
blocked.textContent = "Outside office";
boundary.appendChild(blocked);
select.appendChild(boundary);
blocked.setAttribute("selected", "");
const valueAfterAttribute = select.value;
blocked.selected = true;

console.log("select-ux-dom " + JSON.stringify({
  valueAfterAttribute,
  value: select.value,
  options: Array.from(select.options, option => option.value),
  selected: Array.from(select.selectedOptions, option => option.value),
  index: select.selectedIndex,
  includedOwner: wrapped.form === form,
  excludedOwner: blocked.form === null,
  excludedSelected: blocked.selected,
  fields: Array.from(new FormData(form).entries())
}));
`;

function fixture(variant: Variant, method: Method): string {
  const direct = variant === "reference"
    ? '<option value="wrapped value" selected>Wrapped office</option>'
    : "";
  const originalSelected = variant === "reference" ? "" : " selected";
  const script = variant === "wrapped" ? `<script>${prepareSelect}</script>` : "";
  return `<!doctype html><meta charset="utf-8"><title>${initialTitle}</title><style>${css}</style>
<form id="form" action="/received/${method.toLowerCase()}" method="${method}">
  <div id="panel"><select id="choice" name="choice">
    <option value="original value"${originalSelected}>Original branch</option>${direct}
  </select></div>
  <button type="submit">Send choice</button>
</form>${script}`;
}

const htmlHeaders = { "content-type": "text/html; charset=UTF-8", "cache-control": "no-store" };
const server = Deno.serve({ hostname: "127.0.0.1", port: 0, onListen() {} }, async (request) => {
  const url = new URL(request.url);
  if (url.pathname === "/fixture") {
    const variant = url.searchParams.get("variant");
    if (variant !== "wrapped" && variant !== "reference" && variant !== "different") {
      return new Response("Unknown fixture", { status: 404 });
    }
    const method = url.searchParams.get("method") === "POST" ? "POST" : "GET";
    return new Response(fixture(variant, method), { headers: htmlHeaders });
  }
  if (url.pathname === "/received/get" || url.pathname === "/received/post") {
    const body = await request.text();
    const fields = Array.from(new URLSearchParams(request.method === "POST" ? body : url.search).entries());
    receipts.push({
      method: request.method,
      endpoint: url.pathname,
      query: url.search,
      body,
      contentType: request.headers.get("content-type"),
      fields,
    });
    return new Response(`<!doctype html><title>${resultTitle}</title><h1>${resultTitle}</h1>`, {
      headers: htmlHeaders,
    });
  }
  return new Response("Not found", { status: 404 });
});

const home = `http://127.0.0.1:${server.addr.port}`;
const cases: { name: string; variant: Variant; submit?: Method }[] = [
  { name: "wrapped", variant: "wrapped" },
  { name: "reference", variant: "reference" },
  { name: "different", variant: "different" },
  { name: "get", variant: "wrapped", submit: "GET" },
  { name: "post", variant: "wrapped", submit: "POST" },
];

function fromLog<T>(line: string): T[] {
  try {
    return [JSON.parse(line) as T];
  } catch {
    return [];
  }
}

const expectedDom = {
  valueAfterAttribute: chosenValue,
  value: chosenValue,
  options: ["original value", chosenValue],
  selected: [chosenValue],
  index: 1,
  includedOwner: true,
  excludedOwner: true,
  excludedSelected: true,
  fields: expectedFields,
};
const same = (a: unknown, b: unknown): boolean => JSON.stringify(a) === JSON.stringify(b);
type Event = {
  type?: string;
  url?: string;
  method?: string;
  ok?: boolean;
  title?: string;
  blocked?: boolean;
  cause?: string;
  engine?: string;
  state?: string;
  default?: string;
};
const rows: Record<string, unknown>[] = [];

try {
  for (const test of cases) {
    const path = `${out}/${test.name}`;
    const method = test.submit ?? "GET";
    const steps = [`title=${initialTitle}`, "hold"];
    if (test.submit) steps.push("tap:80,164", `title=${resultTitle}`);
    await Deno.writeTextFile(path + ".json", JSON.stringify(steps));
    const receiptStart = receipts.length;
    const url = `${home}/fixture?variant=${test.variant}&method=${method}`;
    const result = await new Deno.Command("timeout", {
      args: [
        "145", "deno", "run", "--no-check", "--no-config", "--no-npm", "--node-modules-dir=none",
        "--unstable-webgpu", "--unstable-ffi", "-A", host,
        "--offscreen", "--idle-checks-only", "--no-spare-engine-worker", "--no-state", "--follow-links",
        "--offscreen-size", "640x480@1", "--text-size", "100",
        "--native-engine", engine, "--quickjs-wasm", guest,
        "--url", url, "--steps", path + ".json", "--shot", path + ".png", "--shot-at-end",
      ],
      stdout: "piped",
      stderr: "piped",
    }).output();
    const decode = new TextDecoder();
    const log = decode.decode(result.stdout) + "\n" + decode.decode(result.stderr);
    await Deno.writeTextFile(path + ".log", log);
    const events = log.split("\n").filter((line) => line.startsWith("{")).flatMap(fromLog<Event>);
    const dom = log.split("\n").flatMap((line) => {
      const entry = /^page: .*?select-ux-dom (\{.*\})$/.exec(line);
      return entry ? fromLog<typeof expectedDom>(entry[1]) : [];
    });
    const opened = events.some((event) =>
      event.type === "native-html-test-title" && event.ok && event.title === initialTitle && event.url === url
    );
    const native = events.findLast((event) => event.type === "native-html-engine")?.engine === "native " + engine;
    const scriptsOn = events.some((event) =>
      event.type === "native-html-scripts" && event.state === "on" && event.default === "bubblepop"
    );
    const bubblepop = events.some((event) =>
      event.type === "native-html-script" && event.cause === "start" && event.engine === "bubblepop"
    );
    const visible = events.some((event) => event.type === "native-html-shot");
    const domOK = test.variant !== "wrapped" || bubblepop && dom.length === 1 && same(dom[0], expectedDom);
    const seen = receipts.slice(receiptStart);
    const endpoint = "/received/" + method.toLowerCase();
    const received = seen.length === 1 && seen.every((receipt) =>
      receipt.method === method && receipt.endpoint === endpoint && same(receipt.fields, expectedFields) &&
      (method === "POST"
        ? receipt.query === "" && /^application\/x-www-form-urlencoded\b/i.test(receipt.contentType ?? "")
        : receipt.body === "")
    );
    const navigated = events.some((event) => event.type === "native-html-form-navigate" &&
      event.url?.startsWith(home + endpoint) && event.method?.toUpperCase() === method && event.blocked === false);
    const receivedPage = events.some((event) => event.type === "native-html-test-title" &&
      event.ok && event.title === resultTitle && event.url?.startsWith(home + endpoint));
    const submitOK = test.submit ? received && navigated && receivedPage : seen.length === 0;
    const pass = result.code === 0 && native && scriptsOn && opened && visible && domOK && submitOK;
    const row = { case: test.name, pass, exit: result.code, native, scriptsOn, bubblepop, opened, visible, domOK, dom, submitOK, navigated, receivedPage, seen };
    rows.push(row);
    console.log(JSON.stringify(row));
  }
} finally {
  await server.shutdown();
  await Deno.writeTextFile(out + "/browser-results.json", JSON.stringify(rows, null, 2) + "\n");
}
if (rows.some((row) => !row.pass)) Deno.exitCode = 1;
