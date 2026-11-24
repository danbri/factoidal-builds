const [library, arm] = Deno.args;
const engine = Deno.dlopen(library, {
  web_document_call: { parameters: ["buffer", "buffer", "u32", "u32"], result: "pointer" },
  web_render_free: { parameters: ["pointer"], result: "void" },
} as const);
const encoder = new TextEncoder();
const bytes = (value: string) => encoder.encode(value + "\0");
const call = (html: string, request: Record<string, unknown>, width: number, height: number) => {
  const ptr = engine.symbols.web_document_call(bytes(html), bytes(JSON.stringify(request)), width, height);
  if (ptr === null) throw Error("native engine returned no answer");
  try {
    const result = JSON.parse(new Deno.UnsafePointerView(ptr).getCString());
    if (result.error) throw Error(result.error);
    return result;
  } finally { engine.symbols.web_render_free(ptr); }
};
const width = 1280, height = 800, url = "https://frogfind.com/";
const probe = `<script>
const sizing = document.querySelector("font[size]");
const colour = document.querySelector("font[color]");
console.log(JSON.stringify({outer: getComputedStyle(sizing).fontSize,
  inner: getComputedStyle(colour).fontSize, color: getComputedStyle(colour).color}));
</script>`;
const html = (await Deno.readTextFile("page.html")).replace(/<\/body>/i, probe + "</body>");
const turn = call(html, {op:"scriptSession",action:"start",engine:"bubblepop",url,width,height}, width, height);
try {
  if (turn.errors.length) throw Error(JSON.stringify(turn.errors));
  const [record] = turn.logs.map(JSON.parse);
  if (!record) throw Error("FrogFind heading measurement is missing");
  console.log(JSON.stringify(record));
  if (arm === "candidate" && (record.outer !== "48px" || record.inner !== "48px" ||
      record.color !== "rgb(0, 128, 0)")) {
    throw Error("The archived heading did not receive HTML legacy size and colour");
  }
} finally {
  call("", {op:"scriptSession",action:"close",session:turn.session}, width, height);
}
