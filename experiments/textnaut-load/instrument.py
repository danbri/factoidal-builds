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
function scriptSession(engine: HTMLEngine, ...args: Parameters<HTMLEngine["scriptSession"]>) {
  const started = performance.now();
  try { return engine.scriptSession(...args); }
  finally { notePhase("engine." + args[1].action, started); }
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
      console.error(JSON.stringify({ type: "textnaut-load-phases", ...rendered.ms, phases }));''')
p.write_text(source)
