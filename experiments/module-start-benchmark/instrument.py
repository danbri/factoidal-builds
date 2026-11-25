from pathlib import Path
import sys

renderer = Path(sys.argv[1])
source = renderer.read_text()


def after(anchor, addition):
    global source
    assert source.count(anchor) == 1, anchor
    source = source.replace(anchor, anchor + addition)


before = 'const engine=await loadHTML(library);'
assert source.count(before) == 1
source = source.replace(before, '''const rawEngine=await loadHTML(library);
let phase="bootstrap";
const methods:Record<string,{calls:number;ms:number}>={};
const measured=new Set(["decodeDocument","inspect","xmlStylesheet","compile","imageInfo","imageLoad",
  "scriptSession","fontLoad","fontLoadBytes","fontFaces","webFontLoad","subresource"]);
const engine=new Proxy(rawEngine,{
  get(target,key){
    const value=Reflect.get(target,key);
    if(typeof key!=="string"||!measured.has(key)||typeof value!=="function")return value;
    return (...args:unknown[])=>{
      const scope=phase;
      const start=performance.now();
      try{return Reflect.apply(value,target,args);}
      finally{
        const row=methods[scope+"."+key]??={calls:0,ms:0};
        row.calls++;
        row.ms+=performance.now()-start;
      }
    };
  }
});''')
after('  size={width:job.width,height:job.height};', '''
  phase="read";
  const times:Record<string,number>={};
  let phaseStart=performance.now();
  const nextPhase=(next:string)=>{
    times[phase]=performance.now()-phaseStart;
    phase=next;
    phaseStart=performance.now();
  };''')
after('  const source0=withTestRendered(read.source);', '\n  nextPhase("prepare");')
after('  const page=await prepareHTML(engine,read.url,undefined,source0===read.source?undefined:source0,{liberal:true});', '\n  nextPhase("scriptFollowup");')
after('  const {source,options}=page.request(job.width,job.height,{textScalePercent:100,zoomUnit:100});', '\n  nextPhase("encodeRequest");')
before='  const request=JSON.stringify({...options,op:"render",checks:false,cpu:true,partialNote:false});'
assert source.count(before)==1
source=source.replace(before,
  '  const request=JSON.stringify({...options,op:"render",checks:false,partialNote:false});')
after('  const request=JSON.stringify({...options,op:"render",checks:false,partialNote:false});', '\n  nextPhase("scene");')
after('  let buffer=bytesBackend(source,request,job.width,job.height);', '\n  nextPhase("genericFontsAndRedraw");')
after('  if(script)try{engine.scriptSession("",{action:"close"});}catch{/* closed */}', '\n  nextPhase("frameOutput");')
after('  const scene=(head.page??head) as Record<string,unknown>;', '''
  nextPhase("done");
  if (typeof scene.pixelsSection==="number") throw new Error("scene-only call returned CPU pixels");
  if (typeof scene.wgsl!=="string"||typeof scene.dataSection!=="number")
    throw new Error("scene-only call returned no render plan");
  const sha=await crypto.subtle.digest("SHA-256",buffer);
  const digest=Array.from(new Uint8Array(sha),b=>b.toString(16).padStart(2,"0")).join("");
  console.log(JSON.stringify({type:"everyday-phase",url:job.url,file:job.file,
    requestChars:request.length,sourceChars:source.length,times,methods,
    nativeTimings:Object.fromEntries(Object.entries(scene)
      .filter(([key,value])=>/ms$|timing|duration/i.test(key)&&(typeof value==="number"||typeof value==="object")))}));
  return {status:timedOut?"timeout":"ok",sha:digest,waited,scripted:!!script,
    ...(script?{scriptCost:{...reads,wholeWhy}}:{})};''')
const_start=source.index('  const k=scene.pixelsSection;')
const_stop=source.index('\n}\n\nconst jobs=',const_start)
source=source[:const_start]+source[const_stop:]
renderer.write_text(source)
