import {startCompileWorker} from "./native_html_compile.ts";
import {loadHTML} from "./native_html_engine.ts";

const [mode, library, font] = Deno.args;
const native = library === "wasm" ? undefined : library;
const source = '<!doctype html><style>body{margin:0}</style><p><a href="/next">Next</a></p>';
const now = performance.now();
if (mode === "worker") {
  const worker = await startCompileWorker({path:font,family:"Noto Sans"}, native);
  try {
    const ready = performance.now() - now;
    const {artifact} = await worker.compile(source,800,500,{liberal:true});
    if (artifact.webRender.links.length !== 1 || !artifact.data.length) throw Error("worker fixture did not render");
    console.log(JSON.stringify({mode, ready, total:performance.now()-now,rss:Deno.memoryUsage().rss,
      primitiveCount:artifact.primitiveCount,links:artifact.webRender.links}));
  } finally { worker.terminate(); }
} else if (mode === "hit") {
  const engine = await loadHTML(native);
  const artifact = engine.compile(source,800,500,{liberal:true});
  const [id, href, x, y, w, h] = artifact.webRender.links[0] as [number,string,number,number,number,number];
  const hit = engine.hit(artifact,x+w/2+0.125,y+h/2-0.125);
  const miss = engine.hit(artifact,799,499);
  if (!hit || hit.sourceNode !== id || hit.href !== href || miss !== null) throw Error(JSON.stringify({hit,miss,href,id}));
  console.log(JSON.stringify({mode,hit,miss}));
} else throw Error("unknown probe mode");
