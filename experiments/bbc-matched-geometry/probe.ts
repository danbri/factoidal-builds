import {readZip} from "./zip.ts";

type Entry = {
  url: string;
  status: number;
  headers: [string, string][];
  body?: string;
};

const [archive, output, binary] = Deno.args;
const zip = await readZip(await Deno.readFile(archive));
const manifest = JSON.parse(new TextDecoder().decode(zip.get("manifest.json"))) as {url:string;entries:Entry[]};
const key = (url: string) => {
  const u = new URL(url);
  u.hash = "";
  u.searchParams.sort();
  return u.href;
};
const records = new Map<string, Entry>();
for (const entry of manifest.entries) {
  const requestKey = key(entry.url);
  if (!records.has(requestKey)) records.set(requestKey, entry);
}
const stats = {hits: 0, misses: 0, errors: [] as string[]};
const profile = await Deno.makeTempDir({prefix:"bbc-chrome-offline-"});
const browser = new Deno.Command(binary, {args:[
  "--headless=new", "--no-sandbox", "--disable-gpu", "--disable-background-networking",
  "--disable-default-apps", "--disable-extensions", "--no-first-run",
  "--host-resolver-rules=MAP * ~NOTFOUND",
  "--remote-debugging-port=0", `--user-data-dir=${profile}`, "about:blank",
], stdout:"null", stderr:"null"}).spawn();
const wait = (ms:number) => new Promise<void>(r=>setTimeout(r,ms));
const encode = (data:Uint8Array) => {
  let text="";
  for(let i=0;i<data.length;i+=32768)text+=String.fromCharCode(...data.subarray(i,i+32768));
  return btoa(text);
};
let ws:WebSocket|undefined;
try {
  let port="";
  for(let i=0;i<100&&!port;i++){
    try{port=(await Deno.readTextFile(`${profile}/DevToolsActivePort`)).split("\n")[0];}
    catch{await wait(75);}
  }
  if(!port)throw new Error("Chrome did not start the local DevTools endpoint");
  const tabs=await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
  ws=new WebSocket(tabs.find((t:{type:string})=>t.type==="page").webSocketDebuggerUrl);
  await new Promise<void>((resolve,reject)=>{ws!.onopen=()=>resolve();ws!.onerror=reject;});
  let id=0;
  let loaded=false;
  let active=0;
  let lastRequest=performance.now();
  const pending=new Map<number,(m:any)=>void>();
  function send(method:string,params:Record<string,unknown>={}) {
    return new Promise<any>((resolve,reject)=>{
      const next=++id;
      pending.set(next,m=>m.error?reject(new Error(`${method}: ${m.error.message}`)):resolve(m.result));
      ws!.send(JSON.stringify({id:next,method,params}));
    });
  }
  ws.onmessage=event=>{
    const msg=JSON.parse(event.data);
    if(msg.id){pending.get(msg.id)?.(msg);pending.delete(msg.id);return;}
    if(msg.method==="Page.loadEventFired"){loaded=true;return;}
    if(msg.method!=="Fetch.requestPaused")return;
    const {requestId,request}=msg.params;
    const entry=records.get(key(request.url));
    const headers=(entry?.headers??[]).filter(([name,value])=>
      !/^(content-encoding|content-length|transfer-encoding|set-cookie2?)$/i.test(name) &&
      !/[\u0000\r\n]/.test(value)).map(([name,value])=>({name,value}));
    const data=entry?.body?zip.get(entry.body):undefined;
    if(entry)stats.hits++;else stats.misses++;
    active++;lastRequest=performance.now();
    send("Fetch.fulfillRequest", {requestId,responseCode:entry?.status??404,
      responseHeaders:headers,...(data?{body:encode(data)}:{})})
      .catch(e=>stats.errors.push(String(e))).finally(()=>{active--;lastRequest=performance.now();});
  };
  await send("Page.enable");
  await send("Emulation.setDeviceMetricsOverride",{width:1280,height:735,deviceScaleFactor:1,mobile:false});
  await send("Fetch.enable",{patterns:[{urlPattern:"http://*",requestStage:"Request"},{urlPattern:"https://*",requestStage:"Request"}]});
  await send("Page.navigate",{url:manifest.url});
  for(let i=0;i<160;i++){
    await wait(100);
    if(loaded&&!active&&performance.now()-lastRequest>800)break;
  }
  const extract=`(()=>{
    const needles=["paper in her kitchen","Amner Hall","Huang and Trump","returns to the office"];
    const boxes=needles.map(needle=>{
      const candidates=[...document.images].filter(image=>image.alt.includes(needle));
      const shown=candidates.find(image=>{const r=image.getBoundingClientRect();return r.width>0&&r.height>0&&r.top<innerHeight});
      if(!shown)return {needle,candidateCount:candidates.length};
      const chain=[];
      let node=shown;
      for(let i=0;i<10&&node;i++,node=node.parentElement){
        const b=node.getBoundingClientRect(),s=getComputedStyle(node);
        chain.push({tag:node.tagName,classes:node.className,box:[b.x,b.y,b.width,b.height],css:{
          display:s.display,position:s.position,height:s.height,minHeight:s.minHeight,
          aspectRatio:s.aspectRatio,paddingBottom:s.paddingBottom,alignItems:s.alignItems,
          flexDirection:s.flexDirection,gridTemplateRows:s.gridTemplateRows,boxSizing:s.boxSizing}});
      }
      return {needle,source:shown.currentSrc,decoded:[shown.naturalWidth,shown.naturalHeight],chain};
    });
    return {url:location.href,viewport:[innerWidth,innerHeight],ready:document.readyState,boxes};
  })()`;
  const result=await send("Runtime.evaluate",{expression:extract,returnByValue:true});
  if(result.exceptionDetails)throw new Error(JSON.stringify(result.exceptionDetails));
  const shot=await send("Page.captureScreenshot",{format:"png",captureBeyondViewport:false});
  await Deno.mkdir(output,{recursive:true});
  await Deno.writeFile(`${output}/chrome.png`,Uint8Array.from(atob(shot.data),c=>c.charCodeAt(0)));
  await Deno.writeTextFile(`${output}/chrome.json`,JSON.stringify({...result.result.value,stats},null,2)+"\n");
  console.log(JSON.stringify({stats,boxes:result.result.value.boxes.map((row:any)=>[row.needle,row.decoded,row.chain?.[0].box])}));
  if(result.result.value.url!==manifest.url||result.result.value.boxes.some((row:any)=>!row.decoded?.[0]))Deno.exitCode=1;
} finally {
  ws?.close();
  try{browser.kill("SIGTERM");}catch{/* exited already */}
  await browser.status;
  await Deno.remove(profile,{recursive:true}).catch(()=>{});
}
