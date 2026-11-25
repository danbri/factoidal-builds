from pathlib import Path
import sys

path = Path(sys.argv[1])
arm = sys.argv[2]
s = path.read_text()

def replace(before, after):
    global s
    assert s.count(before) == 1, before
    s = s.replace(before, after)

replace('    let i=0,fetchMs=0,engineMs=0;',
        '    let i=0,fetchMs=0,engineMs=0;\n    const routes=new Map<string,number>();')
replace('      console.log(JSON.stringify({type:"startup-sync-wire",t:t0,index:i,host,',
        '''      const key=wire.address?JSON.stringify([host,wire.port,wire.address]):"";
      if(key&&!routes.has(key))routes.set(key,routes.size);
      const bodyDigest=a.bodyBase64===undefined?null:[...new Uint8Array(await crypto.subtle.digest(
        "SHA-256",new TextEncoder().encode(a.bodyBase64)))].map(n=>n.toString(16).padStart(2,"0")).join("");
      console.log(JSON.stringify({type:"startup-sync-wire",t:t0,index:i,host,bodyDigest,route:routes.get(key)??null,''')
if arm == "candidate":
    replace('import {netAnswer,socketAct', 'import {netAnswer,pinnedHTTPSBatch,socketAct')
    replace('    const routes=new Map<string,number>();','''    const routes=new Map<string,number>();
    const transport=pinnedHTTPSBatch();
    try{''')
    replace('      const a=await netFetch(wire);','      const a=await netFetch(wire,transport);')
    replace('    // The requests a turn waited for (module graphs, sync XMLHttpRequest):',
            '    }finally{transport.close();}\n    // The requests a turn waited for (module graphs, sync XMLHttpRequest):')
    replace('  const netFetch=(w:NonNullable<ScriptTurn["netRequests"]>[number])=>{netInFlight++;return Promise.resolve(netAnswer(w)).finally(()=>{netInFlight--;});};',
            '''  const netFetch=(w:NonNullable<ScriptTurn["netRequests"]>[number],transport?:ReturnType<typeof pinnedHTTPSBatch>)=>{
    netInFlight++;
    return netAnswer(w,undefined,transport).finally(()=>{netInFlight--;});
  };''')
elif arm != "baseline":
    raise ValueError(arm)
path.write_text(s)
