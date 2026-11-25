from pathlib import Path
import sys

path, role = Path(sys.argv[1]), sys.argv[2]
s = path.read_text()

def replace(before, after):
    global s
    assert s.count(before) == 1, before
    s = s.replace(before, after)

replace('  const hasRule=(text:string)=>/@font-face/i.test(text);',
        '''  const noteFont=(phase:string,fields:Record<string,unknown>)=>console.log(JSON.stringify({
    type:"startup-web-font",phase,t:performance.now(),...fields}));
  const hasRule=(text:string)=>/@font-face/i.test(text);''')
replace('  let answer;\n  try{answer=await engine.fontFaces',
        '  const discoveryStart=performance.now();\n  let answer;\n  try{answer=await engine.fontFaces')
replace('  const loaded=new Map<string,string>();let total=0;',
        '''  noteFont("discover",{ms:performance.now()-discoveryStart,faceCount:answer?.faces?.length??0});
  const loaded=new Map<string,string>();let total=0;''')
replace('      try {\n        const {bytes}=await readSubresource(engine as SubresourceEngine,"font",src,url,MAX_FONT_BYTES,signal);',
        '''      const start=performance.now();
      let readMs:number|null=null;
      try {
        const {bytes}=await readSubresource(engine as SubresourceEngine,"font",src,url,MAX_FONT_BYTES,signal);
        readMs=performance.now()-start;''')
replace('        total+=bytes.length;loaded.set(src,sha256);webFonts.push({url:src,sha256});',
        '''        total+=bytes.length;loaded.set(src,sha256);webFonts.push({url:src,sha256});
        noteFont("loaded",{readMs,ms:performance.now()-start,bytes:bytes.length,sha256});''')
replace('        loaded.set(src,"");',
        '''        loaded.set(src,"");
        noteFont("refused",{readMs,ms:performance.now()-start});''')
if role == "candidate":
    replace('  pageImageBytes.catch(()=>{});',
        '''  pageImageBytes.catch(()=>{});
  const webFontsReading=loadWebFonts(engine as WebFontEngine,document.url,document.source,resources,signal,imported);
  webFontsReading.catch(()=>{});''')
    replace('  const webFonts=await loadWebFonts(engine as WebFontEngine,document.url,document.source,resources,signal,imported);',
            '  const webFonts=await webFontsReading;')
elif role != "baseline":
    raise ValueError(role)
path.write_text(s)
