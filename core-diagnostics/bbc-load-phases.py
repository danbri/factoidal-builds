from pathlib import Path
import sys

def insert(s: str, anchor: str, addition: str, after: bool = False) -> str:
    assert s.count(anchor) == 1, anchor
    return s.replace(anchor, anchor + addition if after else addition + anchor)

host = Path(sys.argv[1])
document = host / "native_html_document.ts" if host.is_dir() else host
textnaut = host / "textnaut/textnaut.ts" if host.is_dir() else Path(sys.argv[2])
s = document.read_text()
s = insert(s, "  const decode:PageDecoder|undefined", """  let phaseAt = performance.now();
  const phase = (name: string, count?: number) => {
    const now = performance.now();
    console.error(JSON.stringify({type:"bbc-load-probe",phase:name,ms:Math.round(now-phaseAt),count}));
    phaseAt = now;
  };
""")
for anchor, line in [
    ("  // The page's console", '  phase("document");\n'),
    ("  const scriptElements=", '  phase("inspect");\n'),
    ("  // Lean lists the images", '  phase("styles-and-imports", resources.length);\n'),
    ("  // The tab icon", '  phase("initial-image-join", (inspection.images??[]).length);\n'),
    ("  // `diagnostics:true` asks", '  phase("icon-and-fonts", webFonts.length);\n'),
    ("    // Liberal mode: when the script engine refuses", '    phase("classic-script-join", supplied.length);\n'),
    ("    if(turn){", '    phase("script-session-start");\n'),
    ("  const startMore=script?.turn.startMore===true;", '  phase("startup-response-bookkeeping");\n'),
    ("  // Later turns: one check", '  phase("first-turn-resources");\n'),
]:
    s = insert(s, anchor, line)
document.write_text(s)

s = textnaut.read_text()
old = """  for (let i = 0; turn.netSync && i < 4096; i++)
    turn = engine.scriptSession("", { action: "syncAnswer", session: turn.session, answer: await netAnswer(turn.netSync) });"""
new = """  let waits = 0, readMs = 0, engineMs = 0;
  for (let i = 0; turn.netSync && i < 4096; i++) {
    const before = performance.now();
    const answer = await netAnswer(turn.netSync);
    const fetched = performance.now();
    turn = engine.scriptSession("", { action: "syncAnswer", session: turn.session, answer });
    readMs += fetched - before;
    const duration = performance.now() - fetched;
    engineMs += duration;
    console.error(JSON.stringify({type:"bbc-sync-answer",index:i+1,ms:Math.round(duration),continues:!!turn.netSync}));
    waits++;
  }
  if (waits) console.error(JSON.stringify({type:"bbc-sync-probe",waits,readMs:Math.round(readMs),engineMs:Math.round(engineMs)}));"""
assert s.count(old) == 1
s = s.replace(old,new)
s = insert(s, "  await settle(engine, doc, options);\n", "  const prepared = performance.now();\n")
s = insert(s, "  const load = performance.now() - t0;", '  console.error(JSON.stringify({type:"bbc-settle-probe",prepareMs:Math.round(prepared - t0),settleMs:Math.round(performance.now()-prepared)}));\n')
textnaut.write_text(s)
