import {netAnswer as baseline} from "./native_net.base.ts";
import {netAnswer as candidate,pinnedHTTPSBatch,type NetWire} from "./native_net.ts";

const cert=await Deno.readTextFile("cert.pem");
const key=await Deno.readTextFile("key.pem");
const caCerts=[cert],timeoutMs=3000;
const opts={caCerts,timeoutMs};
const names=new Map<string,Set<number>>();
const order:string[]=[];
function handler(tag:string){
  return (req:Request,info:Deno.ServeHandlerInfo)=>{
    let sockets=names.get(tag);
    if(!sockets){sockets=new Set();names.set(tag,sockets);}
    sockets.add((info.remoteAddr as Deno.NetAddr).port);
    const path=new URL(req.url).pathname;
    order.push(`${tag}:${path}`);
    if(path==="/manual")return Response.redirect("https://unserved.invalid/followed",302);
    return new Response(`${tag}:${path}`);
  };
}
const first=Deno.serve({hostname:"127.0.0.1",port:0,cert,key,onListen(){}},handler("A"));
const port=first.addr.port;
const second=Deno.serve({hostname:"127.0.0.2",port,cert,key,onListen(){}},handler("B"));

function wire(id:number,path:string,address="127.0.0.1",hostname="fixture.invalid"):NetWire{
  return {id,method:"GET",url:`https://${hostname}:${port}${path}`,headers:[],address,port};
}
function verify(test:boolean,detail:unknown){
  if(!test)throw new Error(JSON.stringify(detail));
}
try{
  const reports=[];
  for(const [index,pooled] of [false,true,true,false].entries()){
    names.clear();
    order.length=0;
    const batch=pinnedHTTPSBatch(opts);
    const receive=pooled?(w:NetWire)=>candidate(w,opts,batch):(w:NetWire)=>baseline(w,opts);
    const started=performance.now();
    try{
      for(let n=0;n<64;n++){
        const isFirst=n%3!==0;
        const w=wire(n,`/module${n}`,isFirst?"127.0.0.1":"127.0.0.2");
        const answer=await receive(w);
        verify(answer.id===n&&answer.status===200&&
          atob(answer.bodyBase64??"")===`${isFirst?"A":"B"}:/module${n}`,{index,n,answer});
      }
      const elapsedMs=performance.now()-started;
      const sockets=[names.get("A")?.size,names.get("B")?.size];
      verify(sockets[0]===(pooled?1:42)&&sockets[1]===(pooled?1:22),{index,sockets});
      const redirect=await receive(wire(70,"/manual"));
      verify(redirect.status===302&&redirect.headers?.some(([n,v])=>
        n==="location"&&v==="https://unserved.invalid/followed")===true,redirect);
      const bad=await receive(wire(71,"/wrong-name","127.0.0.1","wrong.invalid"));
      verify(bad.id===71&&bad.status===0&&!order.some(path=>path.includes("/wrong-name")),bad);
      reports.push({index,pooled,transfers:64,sockets,elapsedMs});
    } finally {batch.close();}
  }
  const before=names.get("A")?.size??0;
  for(let n=0;n<2;n++){
    const batch=pinnedHTTPSBatch(opts);
    try{
      const a=await candidate(wire(0,"/fresh"),opts,batch);
      verify(a.status===200,a);
    } finally{batch.close();}
  }
  verify(names.get("A")?.size===before+2,{before});
  console.log(JSON.stringify(reports,null,2));
} finally {
  await Promise.all([first.shutdown(),second.shutdown()]);
}
