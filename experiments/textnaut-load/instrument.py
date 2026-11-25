"""Measure existing Textnaut phases without changing the load or script order."""
from pathlib import Path
import sys

p = Path(sys.argv[1])
source = p.read_text()

def replace(old, new, count=1):
    global source
    assert source.count(old) == count, old
    source = source.replace(old, new)

replace('import { netAnswer, type NetWire }', 'import { netAnswer as rawNetAnswer, type NetWire }')
marker = 'const decoder = new TextDecoder(), encoder = new TextEncoder();'
replace(marker, marker + '''
const phases: Record<string, { calls: number; ms: number }> = {};
function notePhase(name: string, started: number) {
  const phase = phases[name] ??= { calls: 0, ms: 0 };
  phase.calls++;
  phase.ms += performance.now() - started;
}
async function timed<T>(name: string, action: () => Promise<T>): Promise<T> {
  const started = performance.now();
  try { return await action(); }
  finally { notePhase(name, started); }
}
const nativeClock = Deno.dlopen("libc.so.6", { clock_gettime: { parameters: ["i32", "buffer"], result: "i32" } });
const timespec = new BigInt64Array(2);
function monotonicTimestamp() {
  if (nativeClock.symbols.clock_gettime(1, timespec) !== 0) throw new Error("clock_gettime failed");
  return `${timespec[0]}.${String(timespec[1]).padStart(9, "0")}`;
}
const startupAnswers: { from: string; to: string; ms: number; pending: boolean; status?: number; wireBytes: number; addresses: number }[] = [];
function scriptSession(engine: HTMLEngine, ...args: Parameters<HTMLEngine["scriptSession"]>) {
  const started = performance.now();
  const isAnswer = args[1].action === "syncAnswer";
  const from = isAnswer ? monotonicTimestamp() : "";
  const result = engine.scriptSession(...args);
  const to = isAnswer ? monotonicTimestamp() : "";
  notePhase("engine." + args[1].action, started);
  if (isAnswer) {
    const answer = args[1].answer as Awaited<ReturnType<typeof rawNetAnswer>>;
    startupAnswers.push({
      from, to, ms: performance.now() - started, pending: !!result.netSync,
      status: answer.status, wireBytes: answer.bodyBase64?.length ?? 0, addresses: answer.addresses?.length ?? 0,
    });
  }
  return result;
}
const netAnswer = (request: Parameters<typeof rawNetAnswer>[0]) =>
  timed("network." + networkPhase, () => rawNetAnswer(request));
let networkPhase = "start";
''')
for action in ('syncAnswer', 'net', 'fetched', 'advance'):
    replace(f'engine.scriptSession("", {{ action: "{action}"', f'scriptSession(engine, "", {{ action: "{action}"')
replace('engine.scriptSession(source, {\n        action: "start"', 'scriptSession(engine, source, {\n        action: "start"')
replace('const results = await Promise.all(wanted.map', 'const results = await timed("network.worker-batch", () => Promise.all(wanted.map')
replace('      })));\n      take(', '      }))));\n      take(')
replace(
    'const doc = await prepareHTML(engine, url, signal, inline, { liberal: options.liberal });\n  await settle(engine, doc, options);',
    '''const doc = await timed("load.prepare", () =>
    prepareHTML(engine, url, signal, inline, { liberal: options.liberal }));
  networkPhase = "settle";
  await timed("load.settle", () => settle(engine, doc, options));'''
)
replace('if (parsed.timing) {', '''if (parsed.timing) {
      console.error(JSON.stringify({ type: "textnaut-load-phases", ...rendered.ms, phases, startupAnswers }));''')
p.write_text(source)

# Deno adds Node timer types through the survey imports. Keep the same timer at runtime.
input_file = p.with_name("input.ts")
input_source = input_file.read_text()
timer = "let timer: number | undefined;"
assert input_source.count(timer) == 1, timer
input_file.write_text(input_source.replace(timer, "let timer: ReturnType<typeof setTimeout> | undefined;"))
