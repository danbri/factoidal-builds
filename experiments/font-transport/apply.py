from pathlib import Path
import sys

lab=Path(sys.argv[1])
doc=lab/'native_html_document.ts'
net=lab/'native_net.ts'
source=doc.read_text()

def replace(before,after):
    global source
    assert source.count(before)==1,before
    source=source.replace(before,after)

replace('import {netAnswer,type NetWire}', 'import {netAnswer,pinnedHTTPSBatch,type NetWire}')
replace('  limit:number,signal?:AbortSignal,before?:()=>Promise<{url:string;bytes:Uint8Array;contentType:string}>):Promise<{url:string;bytes:Uint8Array;contentType:string}> {',
        '''  limit:number,signal?:AbortSignal,before?:()=>Promise<{url:string;bytes:Uint8Array;contentType:string}>,
  transport?:ReturnType<typeof pinnedHTTPSBatch>):Promise<{url:string;bytes:Uint8Array;contentType:string}> {''')
replace('netAnswer(wire,{timeoutMs:10000})','netAnswer(wire,{timeoutMs:10000},transport)')
start=source.index('  for(const face of answer?.faces??[])')
end=source.index('  return webFonts;',start)
before=source[start:end]
assert before.count('MAX_FONT_BYTES,signal);')==1
after=before.replace('MAX_FONT_BYTES,signal);','MAX_FONT_BYTES,signal,undefined,transport);')
source=source[:start]+'''  const transport=pinnedHTTPSBatch({timeoutMs:10000});
  try{
'''+''.join('  '+line for line in after.splitlines(keepends=True))+'''  }finally{transport.close();}
'''+source[end:]
doc.write_text(source)

source=net.read_text()
replace('const timer=setTimeout(stopListening,opts.timeoutMs??300000);',
        'const timer=reusable?undefined:setTimeout(stopListening,opts.timeoutMs??300000);')
net.write_text(source)
