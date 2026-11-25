// Page requests of the desktop host (XMLHttpRequest and fetch of page scripts). The engine
// decides every request (formal/lean4/L4Factoidal/Net/PageFetch.lean: origin, CORS,
// redirects, what a page may reach, the address of a name); this file only moves bytes:
//
// - `resolve:true`: resolve the URL's host name (Deno.resolveDns: A and AAAA records from the
//   system's name servers; not the hosts file) and answer every address it gave
//   (`{id, addresses}`). Nothing is sent to the server.
// - `address` and `port`: connect to that address only. The name is not resolved again, so
//   a second DNS answer cannot move the request (DNS rebinding). `http`: Deno's client with a
//   TCP transport to the address. `https`: Deno's client through a one-connection tunnel to
//   the address; TLS still checks the certificate against the URL's name.
// - otherwise (an IP literal, a page loaded from a local address): a plain fetch.
//
// Every fetch: redirect "manual" (each hop goes back to the engine), no cookies (Deno's fetch
// has no cookie jar), a body of at most 64 MiB, 300 s at most.

export type NetWire={id:number;method:string;url:string;headers:[string,string][];bodyBase64?:string;
  resolve?:boolean;address?:string;port?:number};
export type NetAnswer={id:number;status?:number;statusText?:string;headers?:[string,string][];bodyBase64?:string;addresses?:string[]};

const MAX_BODY=67108864;

/** Extra trust roots (tests only: a local TLS server's certificate). */
export type NetOptions={caCerts?:string[];timeoutMs?:number};

/** A tunnel for one connection: accepts one CONNECT for `target` (`name:port`) with the
 *  random credential it gave the client, and joins it to `address:port`. It listens on the
 *  loopback interface only, for one connection, and stops when the client is closed. */
async function tunnelClient(target:string,address:string,port:number,opts:NetOptions):Promise<{client:Deno.HttpClient;done:()=>void}>{
  const secret=crypto.randomUUID();
  const expected="Basic "+btoa("p:"+secret);
  const listener=Deno.listen({hostname:"127.0.0.1",port:0});
  let open=true;
  const close=()=>{if(open){open=false;try{listener.close();}catch{/* closed */}}};
  const timer=setTimeout(close,opts.timeoutMs??300000);
  (async()=>{
    let conn:Deno.Conn|undefined,up:Deno.Conn|undefined;
    try{
      conn=await listener.accept();close();
      const buf=new Uint8Array(4096);let head="";
      while(!head.includes("\r\n\r\n")){
        const n=await conn.read(buf);if(n===null||head.length>8192)throw new Error("tunnel: no request");
        head+=new TextDecoder("latin1").decode(buf.subarray(0,n));
      }
      const lines=head.slice(0,head.indexOf("\r\n\r\n")).split("\r\n");
      const auth=lines.slice(1).find(l=>/^proxy-authorization:/i.test(l))?.replace(/^[^:]*:\s*/,"");
      if(lines[0]!==`CONNECT ${target} HTTP/1.1`||auth!==expected)throw new Error("tunnel: refused");
      up=await Deno.connect({hostname:address,port});
      await conn.write(new TextEncoder().encode("HTTP/1.1 200 Connection established\r\n\r\n"));
      await Promise.allSettled([conn.readable.pipeTo(up.writable),up.readable.pipeTo(conn.writable)]);
    }catch{
      try{conn?.close();}catch{/* closed */}
      try{up?.close();}catch{/* closed */}
    }finally{close();clearTimeout(timer);}
  })();
  const port0=(listener.addr as Deno.NetAddr).port;
  const client=Deno.createHttpClient({proxy:{transport:"http",url:`http://127.0.0.1:${port0}`,basicAuth:{username:"p",password:secret}},
    ...(opts.caCerts?{caCerts:opts.caCerts}:{})});
  return {client,done:()=>{close();clearTimeout(timer);}};
}

function b64(bytes:Uint8Array):string{
  let s="";for(let i=0;i<bytes.length;i+=32768)s+=String.fromCharCode(...bytes.subarray(i,i+32768));
  return btoa(s);
}

/** The host's answer to one wire of a turn (`netRequests` or `netSync`). */
export async function netAnswer(w:NetWire,opts:NetOptions={}):Promise<NetAnswer>{
  const failed={id:w.id,status:0};
  // a WebSocket connection's wires go to socketOpen / socketWrite / socketClose
  if(w.method.startsWith("WEBSOCKET"))return failed;
  if(w.resolve){
    try{
      const host=new URL(w.url).hostname;
      const found=await Promise.allSettled([Deno.resolveDns(host,"A"),Deno.resolveDns(host,"AAAA")]);
      return {id:w.id,addresses:found.flatMap(r=>r.status==="fulfilled"?r.value:[])};
    }catch{return {id:w.id,addresses:[]};}
  }
  let client:Deno.HttpClient|undefined,done=()=>{};
  try{
    if(w.address){
      const u=new URL(w.url);
      if(u.protocol==="https:"){
        ({client,done}=await tunnelClient(`${u.hostname}:${w.port}`,w.address,w.port??443,opts));
      }else{
        client=Deno.createHttpClient({proxy:{transport:"tcp",hostname:w.address,port:w.port??80}});
      }
    }else if(opts.caCerts){
      client=Deno.createHttpClient({caCerts:opts.caCerts});
    }
    const body=w.bodyBase64!==undefined?Uint8Array.from(atob(w.bodyBase64),c=>c.charCodeAt(0)):undefined;
    const r=await fetch(w.url,{method:w.method,headers:w.headers,body,redirect:"manual",
      signal:AbortSignal.timeout(opts.timeoutMs??300000),...(client?{client}:{})} as RequestInit);
    const reader=r.body?.getReader();let total=0;const parts:Uint8Array[]=[];
    for(;reader;){const {done:end,value}=await reader.read();if(end)break;total+=value.length;if(total>MAX_BODY){await reader.cancel();return failed;}parts.push(value);}
    const bytes=new Uint8Array(total);let at=0;for(const p of parts){bytes.set(p,at);at+=p.length;}
    return {id:w.id,status:r.status,statusText:r.statusText,headers:[...r.headers],bodyBase64:b64(bytes)};
  }catch{return failed;}
  finally{try{client?.close();}catch{/* closed */}done();}
}

// ---- WebSocket connections (formal/lean4/L4Factoidal/Net/WebSocket.lean) ----------------
// The engine writes the opening handshake's fields and every frame, and reads every byte that
// comes back; this host opens one TCP connection (TLS for `wss`, the certificate checked
// against the URL's name) to the address the engine chose (`address`, `port`; else the URL's
// host), writes in order and reads.

export type NetSocket={conn:Deno.Conn;writing:Promise<unknown>};

/** Open the connection of a `WEBSOCKET` wire and make the handshake: the answer is the
 *  response's status and fields and the bytes after them; `socket` when it is open. */
export async function socketOpen(w:NetWire,opts:NetOptions={}):Promise<{answer:NetAnswer;socket?:NetSocket}>{
  const failed={answer:{id:w.id,status:0}};
  let u:URL;try{u=new URL(w.url);}catch{return failed;}
  const secure=u.protocol==="wss:";
  if(!secure&&u.protocol!=="ws:")return failed;
  let conn:Deno.Conn;
  try{
    const tcp=await Deno.connect({hostname:w.address||u.hostname.replace(/^\[|\]$/g,""),port:w.port||Number(u.port||(secure?443:80))});
    conn=secure?await Deno.startTls(tcp,{hostname:u.hostname,...(opts.caCerts?{caCerts:opts.caCerts}:{})}):tcp;
  }catch{return failed;}
  try{
    let head=`GET ${u.pathname}${u.search} HTTP/1.1\r\n`;
    for(const [n,v] of w.headers)head+=`${n}: ${v}\r\n`;
    await conn.write(new TextEncoder().encode(head+"\r\n"));
    let got=new Uint8Array(0);const buf=new Uint8Array(65536);
    const timer=setTimeout(()=>{try{conn.close();}catch{/* closed */}},opts.timeoutMs??30000);
    try{
      for(;;){
        let at=-1;for(let i=0;i+3<got.length;i++)if(got[i]===13&&got[i+1]===10&&got[i+2]===13&&got[i+3]===10){at=i;break;}
        if(at>=0){
          const lines=new TextDecoder().decode(got.subarray(0,at)).split("\r\n");
          const m=/^HTTP\/1\.[01] (\d{3}) ?(.*)$/.exec(lines[0]??"");
          if(!m){conn.close();return failed;}
          const headers=lines.slice(1).map(l=>{const i=l.indexOf(":");return [l.slice(0,i).trim(),l.slice(i+1).trim()] as [string,string];}).filter(h=>h[0]);
          return {answer:{id:w.id,status:Number(m[1]),statusText:m[2],headers,bodyBase64:b64(got.subarray(at+4))},socket:{conn,writing:Promise.resolve()}};
        }
        if(got.length>65536){conn.close();return failed;}
        const n=await conn.read(buf);
        if(n===null){conn.close();return failed;}
        const next=new Uint8Array(got.length+n);next.set(got);next.set(buf.subarray(0,n),got.length);got=next;
      }
    }finally{clearTimeout(timer);}
  }catch{try{conn.close();}catch{/* closed */}return failed;}
}

/** The next bytes of an open connection (status 1), or its end (status 0). */
export async function socketRead(id:number,s:NetSocket):Promise<NetAnswer>{
  const buf=new Uint8Array(65536);
  try{const n=await s.conn.read(buf);return n===null?{id,status:0}:{id,status:1,bodyBase64:b64(buf.subarray(0,n))};}
  catch{return {id,status:0};}
}

/** A `WEBSOCKET-SEND` (the frame's bytes, in order) or `WEBSOCKET-CLOSE` wire. */
export function socketAct(s:NetSocket,w:NetWire):void{
  if(w.method==="WEBSOCKET-CLOSE"){s.writing=s.writing.then(()=>{try{s.conn.close();}catch{/* closed */}});return;}
  const bytes=w.bodyBase64!==undefined?Uint8Array.from(atob(w.bodyBase64),c=>c.charCodeAt(0)):new Uint8Array(0);
  s.writing=s.writing.then(async()=>{try{let at=0;while(at<bytes.length)at+=await s.conn.write(bytes.subarray(at));}catch{/* the read sees the end */}});
}
