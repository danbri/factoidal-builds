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
import re
line, = re.findall(r'^ +const \{bytes\}=await readSubresource\(engine as SubresourceEngine,"font".*;$',s,re.M)
inner=" "*(len(line)-len(line.lstrip()))
outer=inner[:-2]
replace(outer+'try {\n'+line,
        outer+'const start=performance.now();\n'+outer+'let readMs:number|null=null;\n'+
        outer+'try {\n'+line+'\n'+inner+'readMs=performance.now()-start;')
saved=inner+'total+=bytes.length;loaded.set(src,sha256);webFonts.push({url:src,sha256});'
replace(saved,saved+'\n'+inner+'noteFont("loaded",{readMs,ms:performance.now()-start,bytes:bytes.length,sha256});')
refused=inner+'loaded.set(src,"");'
replace(refused,refused+'\n'+inner+'noteFont("refused",{readMs,ms:performance.now()-start});')
path.write_text(s)
