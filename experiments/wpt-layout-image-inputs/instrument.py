"""Test the released renderer with the ordinary desktop image request fields."""
from pathlib import Path
import sys

path = Path(sys.argv[1])
source = path.read_text()

def replace(old, new):
    global source
    assert source.count(old) == 1, old
    source = source.replace(old, new)

replace(
    'import {loadImports} from "../../docs/web/hub/foafnaut/page-load.mjs";',
    '''import {loadImports} from "../../docs/web/hub/foafnaut/page-load.mjs";
import {imageOptions, MAX_IMAGE_BYTES, pageImageLimit} from "../../labs/demos/foafnaut/native_html_document.ts";''',
)
replace('const wptserveMode=args.includes("--wptserve");',
        'const wptserveMode=args.includes("--wptserve");\nconst withLayoutImages=args.includes("--diagnostic-layout-images");')
replace('stylesheets?:{nodeId:number;url:string}[]};',
        'stylesheets?:{nodeId:number;url:string}[];images?:{key:string;url:string}[]};')
old='''    const layout=sheetResources.length||sheetFailures.length||webFonts.length||imported.length?{layout:{url,resources:sheetResources,resourceFailures:sheetFailures,
      ...(webFonts.length?{webFonts}:{}),...(imported.length?{imported}:{})}}:{};'''
new='''    const layoutResources={url,resources:sheetResources,resourceFailures:sheetFailures,
      ...(webFonts.length?{webFonts}:{}),...(imported.length?{imported}:{})};
    let imageFields:Record<string,unknown>={};
    if(withLayoutImages){
      const wanted=(engine.inspect(html,layoutResources) as unknown as Facts).images??[];
      const fetched:{key:string;bytes:Uint8Array}[]=[];
      const keys=new Set<string>();
      let total=0;
      const limit=await pageImageLimit(engine);
      for(const {key,url:src} of wanted){
        if(keys.has(key)||!isWptHost(src))continue;
        const file=scriptFile(src);
        if(!http&&(!file||(await Deno.stat(file).catch(()=>undefined))?.size!>MAX_IMAGE_BYTES))continue;
        const bytes=await readBytes(src);
        if(!bytes||bytes.length>MAX_IMAGE_BYTES||total+bytes.length>limit)continue;
        total+=bytes.length;
        keys.add(key);
        fetched.push({key,bytes});
      }
      imageFields=await imageOptions(engine,fetched);
      console.log(JSON.stringify({type:"diagnostic-layout-images",file,listed:wanted.length,held:fetched.length,bytes:total}));
    }
    const layout=sheetResources.length||sheetFailures.length||webFonts.length||imported.length||Object.keys(imageFields).length
      ?{layout:{...layoutResources,...imageFields}}:{};'''
new=new.replace(
    'if(!http&&(!file||(await Deno.stat(file).catch(()=>undefined))?.size!>MAX_IMAGE_BYTES))continue;',
    '''if(!http){
          if(!file)continue;
          const stat=await Deno.stat(file).catch(()=>undefined);
          if(!stat?.isFile||stat.size>MAX_IMAGE_BYTES)continue;
        }''',
)
replace(old, new)
path.write_text(source)
