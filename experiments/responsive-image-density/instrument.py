from pathlib import Path
import sys
file = Path(sys.argv[1]); s = file.read_text()
marker='  const scene=(head.page??head) as Record<string,unknown>;'
assert s.count(marker)==1
file.write_text(s.replace(marker,marker+'''
  const layout=scene.webRender as {boxes?:number[][]}|undefined;
  if(!Array.isArray(layout?.boxes))throw new Error("Missing layout boxes");
  const nodes=(await engine.inspect(source,{...options,url:page.url}) as {nodes:{id:number;tagName:string;attributes?:Record<string,string>}[]}).nodes;
  const images=nodes.filter(n=>n.tagName?.toLowerCase()==="img").map(n=>({id:n.attributes?.id,
    boxes:layout.boxes!.filter(b=>b[0]===n.id).map(b=>b.slice(1,5))}));
  await Deno.writeTextFile(outDir+"/"+job.file+".json",JSON.stringify(images));
'''))
