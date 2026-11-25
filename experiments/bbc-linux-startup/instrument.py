from pathlib import Path
import sys

lab = Path(sys.argv[1])

def edit(file, edits):
    path = lab / file
    source = path.read_text()
    for before, after in edits:
        assert source.count(before) == 1, (file, before)
        source = source.replace(before, after)
    path.write_text(source)

def mark(phase):
    return f'  firstPhase("{phase}");\n'

lines = [
    ("  const xml=await engine.xmlStylesheet(", "source-ready"),
    ("  const inspection=await engine.inspect(", "metadata-ready"),
    ("  const scriptElements=inspection.scripts.some(", "inspection-ready"),
    ("  for(const read of sheetsRead)", "linked-sheets-ready"),
    ("  const listedImages=new Set(", "imports-ready"),
    ("  let iconBase64:string|undefined;", "first-frame-images-ready"),
    ("  const webFonts=await loadWebFonts(", "icon-ready"),
    ("  // `diagnostics:true` asks Lean", "web-fonts-ready"),
    ("  if(scripted&&scriptHost) {", "fallback-fonts-ready"),
    ("    const turn=await Promise.resolve(scriptHost.start(document.source,document.url,supplied,", "script-start"),
    ("    if(turn){\n      noteTurn(page,turn);", "script-ready"),
    ("  let againTimer:ReturnType<typeof setTimeout>|undefined", "script-resources-ready"),
]
edit("native_html_document.ts", [
    ("  const isLocalEpub=inline", """  const firstLoad = performance.now();
  const firstPhase=(phase:string)=>console.log(JSON.stringify({type:"startup-document-phase",
    phase,t:performance.now(),since:performance.now()-firstLoad}));
  firstPhase("prepare-enter");
  const isLocalEpub=inline"""),
    *[(needle, mark(phase)+needle) for needle, phase in lines],
    ("  const images:Record<string,unknown>=later?{}:await imageOptions(engine,await pageImageBytes);",
     """  firstPhase("images-wait-start");
  const firstBytes=later?undefined:await pageImageBytes;
  firstPhase("images-bytes-ready");
  const images:Record<string,unknown>=firstBytes?await imageOptions(engine,firstBytes):{};"""),
])
edit("run_html.ts", [
    ("      const a=await netFetch((t as ScriptTurn).netSync!);",
     """      const wire=(t as ScriptTurn).netSync!;
      const a=await netFetch(wire);"""),
    ("      fetchMs+=t1-t0;engineMs+=performance.now()-t1;",
     """      const done=performance.now();
      fetchMs+=t1-t0;engineMs+=done-t1;
      const host=(()=>{try{return new URL(wire.url).hostname;}catch{return "";}})();
      console.log(JSON.stringify({type:"startup-sync-wire",t:t0,index:i,host,
        transfer:wire.resolve?"dns":wire.address?"pinned":"direct",method:wire.method,
        status:a.status??null,addressCount:a.addresses?.length??null,base64Length:a.bodyBase64?.length??0,
        fetchMs:t1-t0,engineMs:done-t1}));"""),
    ("  const adapter=await navigator.gpu?.requestAdapter();",
     """  console.log(JSON.stringify({type:"startup-host-phase",phase:"document-ready",t:performance.now()}));
  const adapter=await navigator.gpu?.requestAdapter();"""),
    ("    device=await adapter.requestDevice();native=early??await nativePreflight(()=>loadNativeWindow());",
     """    device=await adapter.requestDevice();native=early??await nativePreflight(()=>loadNativeWindow());
    console.log(JSON.stringify({type:"startup-host-phase",phase:"device-ready",t:performance.now()}));"""),
])
