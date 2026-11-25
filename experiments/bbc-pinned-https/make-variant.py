from pathlib import Path
import sys

path = Path(sys.argv[1])
source = path.read_text()
start = source.index('/** A tunnel for one connection:')
end = source.index('function b64', start)
tunnel = '''type Tunnel = {client:Deno.HttpClient; close:()=>void};

/** Keep transport pinned to one authority and one Lean-approved address.
 * The inner TLS session still verifies the URL hostname. */
function tunnelClient(target:string,address:string,port:number,opts:NetOptions,reusable=false):Tunnel{
  const secret=crypto.randomUUID();
  const expected="Basic "+btoa("p:"+secret);
  const listener=Deno.listen({hostname:"127.0.0.1",port:0});
  let listening=true,closed=false;
  const connections=new Set<Deno.Conn>();
  const closeConnection=(conn:Deno.Conn)=>{
    connections.delete(conn);
    try{conn.close();}catch{/* closed */}
  };
  const stopListening=()=>{if(listening){listening=false;listener.close();}};
  const bridge=async(conn:Deno.Conn)=>{
    let upstream:Deno.Conn|undefined;
    connections.add(conn);
    const timer=setTimeout(()=>closeConnection(conn),opts.timeoutMs??300000);
    try{
      const buf=new Uint8Array(4096);let head="";
      while(!head.includes("\\r\\n\\r\\n")){
        const n=await conn.read(buf);if(n===null||head.length>8192)throw new Error("tunnel: no request");
        head+=new TextDecoder("latin1").decode(buf.subarray(0,n));
      }
      const lines=head.slice(0,head.indexOf("\\r\\n\\r\\n")).split("\\r\\n");
      const auth=lines.slice(1).find(line=>/^proxy-authorization:/i.test(line))?.replace(/^[^:]*:\\s*/,"");
      if(lines[0]!==`CONNECT ${target} HTTP/1.1`||auth!==expected)throw new Error("tunnel: refused");
      const connected=await Deno.connect({hostname:address,port});
      upstream=connected;
      if(closed)return;
      connections.add(upstream);
      await conn.write(new TextEncoder().encode("HTTP/1.1 200 Connection established\\r\\n\\r\\n"));
      clearTimeout(timer);
      await Promise.allSettled([conn.readable.pipeTo(upstream.writable),upstream.readable.pipeTo(conn.writable)]);
    }catch{/* the client sees a closed tunnel */}
    finally{
      clearTimeout(timer);
      closeConnection(conn);
      if(upstream)closeConnection(upstream);
    }
  };
  const timer=setTimeout(stopListening,opts.timeoutMs??300000);
  let client:Deno.HttpClient;
  try{
    client=Deno.createHttpClient({proxy:{transport:"http",url:`http://127.0.0.1:${listener.addr.port}`,
      basicAuth:{username:"p",password:secret}},...(opts.caCerts?{caCerts:opts.caCerts}:{}),
      ...(reusable?{poolMaxIdlePerHost:1,poolIdleTimeout:10000}:{})});
  }catch(error){clearTimeout(timer);stopListening();throw error;}
  void (async()=>{
    while(listening){
      let conn:Deno.Conn;
      try{conn=await listener.accept();}catch{break;}
      if(!reusable){stopListening();clearTimeout(timer);}
      if(closed||connections.size>=8)closeConnection(conn);
      else void bridge(conn);
    }
  })();
  return {client,close:()=>{
    if(closed)return;
    closed=true;
    clearTimeout(timer);
    stopListening();
    try{client.close();}finally{for(const conn of connections)closeConnection(conn);}
  }};
}

type PinnedHTTPSBatch = {get:(host:string,address:string,port:number)=>Deno.HttpClient; close:()=>void};

/** Reuse connections only within the caller's synchronous answer sequence. */
export function pinnedHTTPSBatch(opts:NetOptions={}):PinnedHTTPSBatch{
  const tunnels=new Map<string,Tunnel>();
  return {
    get(host,address,port){
      const key=JSON.stringify([host,address,port]);
      let tunnel=tunnels.get(key);
      if(tunnel)tunnels.delete(key);
      else{
        if(tunnels.size>=4){
          const oldest=tunnels.keys().next().value!;
          tunnels.get(oldest)!.close();
          tunnels.delete(oldest);
        }
        tunnel=tunnelClient(`${host}:${port}`,address,port,opts,true);
      }
      tunnels.set(key,tunnel);
      return tunnel.client;
    },
    close(){
      for(const tunnel of tunnels.values())tunnel.close();
      tunnels.clear();
    },
  };
}

'''
source = source[:start] + tunnel + source[end:]
def swap(before, after):
    global source
    assert source.count(before) == 1, before
    source = source.replace(before, after)
swap('export async function netAnswer(w:NetWire,opts:NetOptions={}):Promise<NetAnswer>{',
     'export async function netAnswer(w:NetWire,opts:NetOptions={},batch?:PinnedHTTPSBatch):Promise<NetAnswer>{')
swap('  let client:Deno.HttpClient|undefined,done=()=>{};',
     '  let client:Deno.HttpClient|undefined,pooled=false,done:()=>void=()=>{};')
swap('        ({client,done}=await tunnelClient(`${u.hostname}:${w.port}`,w.address,w.port??443,opts));',
     '''        const port=w.port??443;
        if(batch&&w.method==="GET"&&w.bodyBase64===undefined){
          client=batch.get(u.hostname,w.address,port);
          pooled=true;
        }else{
          ({client,close:done}=tunnelClient(`${u.hostname}:${port}`,w.address,port,opts));
        }''')
swap('  finally{try{client?.close();}catch{/* closed */}done();}',
     '  finally{if(!pooled)try{client?.close();}catch{/* closed */}done();}')
path.write_text(source)
