from pathlib import Path

renderer = Path("core/tests/browser-wpt/reftest-render.ts")
source = renderer.read_text()
anchor = '  const scene=(head.page??head) as Record<string,unknown>;'
assert source.count(anchor) == 1
renderer.write_text(source.replace(anchor, anchor + '''
  const layout = scene.webRender as {boxes?: number[][]}|undefined;
  if (!Array.isArray(layout?.boxes)) throw new Error("native frame has no layout boxes");
  const inspected = await engine.inspect(source,{...options,url:page.url}) as {
    nodes:{id:number;tagName:string;attributes?:Record<string,string>;parent:number|null}[]
  };
  const byId = new Map(inspected.nodes.map(n=>[n.id,n]));
  const byBox = new Map<number,number[][]>();
  for (const [id,x,y,w,h] of layout.boxes) {
    const existing=byBox.get(id)??[];
    existing.push([x,y,w,h]);
    byBox.set(id,existing);
  }
  const needles=["paper in her kitchen","Amner Hall","Huang and Trump","returns to the office"];
  const cards=needles.map(needle=>({needle,instances:inspected.nodes
    .filter(n=>n.tagName.toLowerCase()==="img"&&n.attributes?.alt?.includes(needle))
    .slice(0,6).map(n=>{
      const chain=[];
      let node:typeof n|undefined=n;
      for(let depth=0;node&&depth<10;depth++){
        chain.push({tag:node.tagName,classes:node.attributes?.class,boxes:byBox.get(node.id)??[]});
        node=node.parent===null?undefined:byId.get(node.parent);
      }
      return {chain};
    })}));
  await Deno.writeTextFile(outDir+"/foafnaut-geometry.json",JSON.stringify({url:page.url,cards},null,2)+"\\n");
'''))
