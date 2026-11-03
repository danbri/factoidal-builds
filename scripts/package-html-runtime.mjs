#!/usr/bin/env node
// Package a checked local build. This is not a compiler or a GPU/conformance gate.
import {stripTypeScriptTypes} from 'node:module';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {readFile,writeFile,lstat,realpath,mkdir,mkdtemp,rename,rm} from 'node:fs/promises';
import {resolve,join,dirname,relative,isAbsolute,sep} from 'node:path';
import {pathToFileURL} from 'node:url';
export const HTML_RUNTIME_FILES=Object.freeze(['web-render.mjs','web-render.wasm',
  'render-plan.mjs','render-plan.wasm','gpu-transport.mjs','render-plan-host.mjs','source-witness.json']);
const LAB='labs/demos/foafnaut',BUILD=LAB+'/.build/web-render';
const hash=b=>createHash('sha256').update(b).digest('hex');
function safe(path){
 if(typeof path!=='string'||!path||isAbsolute(path)||path.includes('\\')||/[\u0000-\u001f]/u.test(path)||path.split('/').some(p=>!p||p==='.'||p==='..'))throw Error('Unsafe source path');
 return path;
}
async function bytes(root,path){
 safe(path);const name=join(root,path),info=await lstat(name);
 if(!info.isFile()||info.isSymbolicLink())throw Error(`Expected regular file: ${path}`);
 const actual=await realpath(name),rel=relative(root,actual);
 if(rel==='..'||rel.startsWith('..'+sep)||isAbsolute(rel))throw Error('Source escapes checkout');
 return readFile(name);
}
function git(core,args){return execFileSync('git',['-C',core,...args],{stdio:['ignore','pipe','pipe']});}
async function committed(core,path,head){
 const data=await bytes(core,path),row=git(core,['ls-tree',head,'--',safe(path)]).toString().trim();
 if(!/^100(?:644|755) blob [0-9a-f]+\t/u.test(row)||!data.equals(git(core,['show',`${head}:${path}`])))throw Error(`Uncommitted source input: ${path}`);
 return data;
}
export function stripHtmlBridge(source,name){
 const targets=name==='gpu_transport'?new Map([['./render_plan.ts','./render-plan-host.mjs']]):
  name==='render_plan'?new Map([['./.build/engines/render-plan.mjs','./render-plan.mjs']]):null;
 if(!targets)throw Error('Unknown HTML transport');
 let out=stripTypeScriptTypes(source,{mode:'strip',sourceUrl:`${name}.ts`}),seen=0;
 out=out.replace(/^([ \t]*import[ \t]+(?:[^'";\r\n]*?[ \t]+from[ \t]*)?)(["'])([^"'\r\n]+)\2/gmu,
  (_,prefix,quote,path)=>{if(!targets.has(path))throw Error(`Unexpected transport import: ${path}`);seen++;return prefix+quote+targets.get(path)+quote;});
 if(seen!==targets.size||[...out.matchAll(/^[ \t]*import\b/gmu)].length!==seen||/\bimport\s*\(/u.test(out))throw Error('Transport imports require review');
 return out;
}
async function closure(core){
 const files=new Set(),seen=new Set();
 async function visit(module){
  if(seen.has(module))return;seen.add(module);
  const path=module.startsWith('L4Factoidal.')?'formal/lean4/'+module.replaceAll('.','/')+'.lean':
   !module.includes('.')&&!['Init','Std','Lean'].includes(module)?LAB+'/'+module+'.lean':null;
  if(!path)return;
  const text=(await bytes(core,path)).toString();files.add(path);
  for(const match of text.matchAll(/^import\s+([^\r\n]+)/gmu))for(const name of match[1].split(/\s+/u)){
   if(name.startsWith('--'))break;await visit(name);
  }
 }
 const shim=(await bytes(core,LAB+'/web_render_shim.c')).toString();
 const initializers=[...shim.matchAll(/initialize_([A-Za-z][A-Za-z0-9_]*)\s*\(\s*1\s*\)/gu)].map(m=>m[1]);
 if(!initializers.length||initializers.some(name=>!['WebRender','WebRenderRDF','WebRenderFont','WebDocument'].includes(name)))throw Error('Renderer initializer requires review');
 for(const name of new Set(initializers))await visit(name);
 await visit('RenderPlan');return files;
}
export async function packageHtmlRuntime({coreDir,outDir,sourceCommit,kind='development'}){
 if(kind!=='development')throw Error('Only a trusted fresh-build publisher can finalize a release');
 if(!/^[0-9a-f]{40}$/u.test(sourceCommit??''))throw Error('Exact40-character source commit required');
 const core=await realpath(resolve(coreDir)),out=resolve(outDir),head=git(core,['rev-parse','HEAD']).toString().trim();
 if(head!==sourceCommit)throw Error('Requested source differs from checkout HEAD');
 const witnessBytes=await bytes(core,BUILD+'/source-witness.json');
 const witness=JSON.parse(witnessBytes.toString());
 if(witness.format!=='factoidal-web-render-source-witness-v1'||witness.commit!==head||!witness.files||!witness.generatedC||!witness.engines)throw Error('Missing or wrong-source renderer build witness');
 if(typeof witness.runtimeObjectWitness!=='string'||!/^wasm32-string-list-v1\n[0-9a-f]{64}\n[0-9a-f]{64}/u.test(witness.runtimeObjectWitness))throw Error('Verified wasm32 runtime witness required');
 for(const path of await closure(core))if(!Object.hasOwn(witness.files,path))throw Error(`Build witness omits source dependency: ${path}`);
 for(const path of [LAB+'/build-web-render.sh',LAB+'/web_render_shim.c',LAB+'/render_plan_shim.c',
   LAB+'/toolchain-versions.env','formal/lean4/lean-toolchain'])if(!Object.hasOwn(witness.files,path))throw Error(`Build witness omits required input: ${path}`);
 for(const [path,expected]of Object.entries(witness.files)){
  if(!/^[0-9a-f]{64}$/u.test(expected)||hash(await committed(core,path,head))!==expected)throw Error(`Stale source build witness: ${path}`);
 }
 // Generated C is validated locally; it is not included in the public package.
 for(const [path,expected]of Object.entries(witness.generatedC))if(hash(await bytes(core,path))!==expected)throw Error(`Stale generated C witness: ${path}`);
 const products=new Map(),sourceInputs=[];
 for(const name of ['web-render.mjs','web-render.wasm','render-plan.mjs','render-plan.wasm']){
  const path=BUILD+'/engines/'+name,data=await bytes(core,path);
  if(witness.engines[path]!==hash(data))throw Error(`Engine differs from build witness: ${name}`);
  if(name.endsWith('.wasm')&&!data.subarray(0,8).equals(Buffer.from([0,97,115,109,1,0,0,0])))throw Error('Invalid WASM module');
  products.set(name,data);
 }
 for(const [input,output]of [['gpu_transport','gpu-transport.mjs'],['render_plan','render-plan-host.mjs']]){
  const path=LAB+'/'+input+'.ts',data=await committed(core,path,head);
  products.set(output,Buffer.from(stripHtmlBridge(data.toString(),input)));
  sourceInputs.push({path,bytes:data.length,sha256:hash(data)});
 }
 products.set('source-witness.json',witnessBytes);
 const manifest={format:'factoidal-html-webgpu-runtime-v1',kind,sourceCommit:head,
  files:HTML_RUNTIME_FILES.map(path=>({path,bytes:products.get(path).length,sha256:hash(products.get(path))})),
  evidence:{qualification:'Development package: source/C/engine byte correspondence is recorded, not a compiler-correctness, browser-conformance or GPU proof.',
   sourceWitnessSha256:hash(witnessBytes),sourceInputs,packagingNode:process.version,
   leanToolchain:(await bytes(core,'formal/lean4/lean-toolchain')).toString().trim()}};
 try{await lstat(out);throw Error('Output already exists');}catch(error){if(error.code!=='ENOENT')throw error;}
 await mkdir(dirname(out),{recursive:true});const stage=await mkdtemp(join(dirname(out),'.html-runtime-'));
 try{
  for(const [path,data]of products)await writeFile(join(stage,path),data);
  await writeFile(join(stage,'manifest.json'),JSON.stringify(manifest,null,2)+'\n');await rename(stage,out);
 }catch(error){await rm(stage,{recursive:true,force:true});throw error;}
 return manifest;
}
async function main(args){
 const values={},names=new Map([['--core','coreDir'],['--out','outDir'],['--source-commit','sourceCommit'],['--kind','kind']]);
 while(args.length){const key=args.shift();if(!names.has(key)||!args.length||Object.hasOwn(values,names.get(key)))throw Error('Expected --core DIR --out NEW_DIR --source-commit SHA [--kind development]');values[names.get(key)]=args.shift();}
 if(!values.coreDir||!values.outDir)throw Error('--core and --out required');
 const manifest=await packageHtmlRuntime(values);console.log(`Packaged${manifest.files.length} HTML runtime files from${manifest.sourceCommit}; ${manifest.kind}`);
}
if(process.argv[1]&&import.meta.url===pathToFileURL(resolve(process.argv[1])).href)main(process.argv.slice(2)).catch(error=>{console.error(error.message);process.exitCode=1;});
