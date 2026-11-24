from pathlib import Path
import sys

lab = Path(sys.argv[1])

def add_marks(path, opening, marks):
    source = path.read_text()
    assert source.count(opening) == 1, opening
    trace = """
  let previous = performance.now();
  const mark = (phase:string, count?:number) => {
    const at = performance.now();
    console.error(JSON.stringify({type:"wiki-startup-phase", phase, ms:Math.round(at-previous), count}));
    previous = at;
  };"""
    source = source.replace(opening, opening + trace)
    for anchor, label, count in marks:
        assert source.count(anchor) == 1, anchor
        source = source.replace(anchor, f'  mark("{label}"{", "+count if count else ""});\n' + anchor)
    path.write_text(source)

doc = lab / "native_html_document.ts"
src = doc.read_text()
opening = src.split("export async function prepareHTML", 1)[1].split("\n", 1)[0]
opening = "export async function prepareHTML" + opening
assert opening.endswith("{"), opening
add_marks(doc, opening, [
    ("  // The page's console", "document-read", "document.bytes"),
    ("  const fonts=fontHost", "xml-stylesheet", None),
    ("  noteDiagnostics(page,inspection,false);", "inspect", "inspection.images?.length"),
    ("  const listedImages=new Set", "stylesheet-imports", "resources.length"),
    ("  // The tab icon that Lean chose", "joined-and-installed-images", "backgroundWanted.length"),
    ("  const webFonts=await loadWebFonts", "icon", None),
    ('  // `diagnostics:true` asks Lean', "web-fonts", "webFonts.length"),
    ("  if(scripted&&scriptHost) {", "font-host", None),
    ("    // Liberal mode: when the script engine refuses", "classic-script-join", "supplied.length"),
    ("    if(turn){\n      noteTurn(page,turn);", "script-start-and-sync", "turn?.commands?.length"),
    ("  // Elements that the page's scripts make", "start-finalize", "script?.turn.commandCount"),
])

text = lab / "textnaut" / "textnaut.ts"
src = text.read_text()
changes = [
    ("  const doc = await prepareHTML(engine, url, signal, inline, { liberal: options.liberal });",
     '  const doc = await prepareHTML(engine, url, signal, inline, { liberal: options.liberal });\n'
     '  const prepared = performance.now();\n'
     '  console.error(JSON.stringify({type:"wiki-startup-phase",phase:"prepare-total",ms:Math.round(prepared-t0)}));'),
    ("  const load = performance.now() - t0;",
     '  const load = performance.now() - t0;\n'
     '  console.error(JSON.stringify({type:"wiki-startup-phase",phase:"post-start-script-settle",ms:Math.round(performance.now()-prepared)}));'),
    ("    return { view, artifact: await doc.compile(view.width, view.height) as unknown as Frame };",
     '    const started = performance.now();\n'
     '    const artifact = await doc.compile(view.width, view.height) as unknown as Frame;\n'
     '    console.error(JSON.stringify({type:"wiki-startup-phase",phase:"layout-compile",ms:Math.round(performance.now()-started),width:view.width,height:view.height}));\n'
     '    return { view, artifact };'),
]
for old, new in changes:
    assert src.count(old) == 1, old
    src = src.replace(old, new)
text.write_text(src)
