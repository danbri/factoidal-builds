import {handle} from "./source/labs/demos/foafnaut/daily_use_server.ts";

const [role,presentation,engine,out]=Deno.args;
const actual=role==="candidate";
const host=new URL("source/labs/demos/foafnaut/run_html.ts",import.meta.url).pathname;
const server=Deno.serve({hostname:"127.0.0.1",port:0,onListen(){}},handle);
const home="http://127.0.0.1:"+server.addr.port;
const path=out+"/"+role+"-"+presentation;
const steps=path+".json";
try {
  const fieldRow=presentation==="single"?250:120;
  await Deno.writeTextFile(steps,JSON.stringify(["hold","tap:480,"+fieldRow,"hold","type:go",[5,36,0],"title=Results: go","addr=@url"]));
  const result=await new Deno.Command("timeout",{args:["145","deno","run","--no-check","--no-config","--no-npm","--node-modules-dir=none",
    "--unstable-webgpu","--unstable-ffi","-A",host,"--offscreen","--idle-checks-only","--no-spare-engine-worker","--no-state","--follow-links",
    "--native-engine",engine,"--url",home+"/search.html","--steps",steps,"--shot",path+".png","--shot-at-end",
    ...(presentation==="single"?["--single-frame"]:[])],stdout:"piped",stderr:"piped"}).output();
  const decode=new TextDecoder(), log=decode.decode(result.stdout)+decode.decode(result.stderr);
  await Deno.writeTextFile(path+".log",log);
  const events=log.split("\n").filter(line=>line.startsWith("{")).flatMap(line=>{
    try { return [JSON.parse(line)]; } catch { return []; }
  });
  const addr=events.find(event=>event.type==="native-html-test-edit"&&event.step==="addr=@url");
  const title=events.find(event=>event.type==="native-html-test-title"&&event.ok===true);
  const destination=home+"/results?q=go&r=";
  console.log(JSON.stringify({role,presentation,status:result.code,title,addr}));
  if(title?.url!==destination||addr?.address!==destination
      ||(actual? result.code!==0||!addr.ok||addr.presentedAddress!==destination
                 : result.code!==1||addr.ok||addr.presentedAddress!==home+"/search.html")) Deno.exitCode=1;
} finally {
  await server.shutdown();
}
