#!/usr/bin/env node
// Package existing Lean-generated engines and existing TS host bridges.
// This command does NOT build, render, prove or publish anything. A matching
// source inventory detects stale source inputs; it does not prove that existing
// engine bytes were compiled from them. Therefore this path is DEVELOPMENT ONLY.
import {stripTypeScriptTypes} from 'node:module';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {readFile,writeFile,lstat,realpath,mkdir,mkdtemp,rename,rm} from 'node:fs/promises';
import {resolve,dirname,join,relative,isAbsolute,sep} from 'node:path';
import {pathToFileURL} from 'node:url';

const LAB='labs/demos/foafnaut';
export const REQUIRED_RUNTIME_FILES=Object.freeze([
  'svg_engine.mjs','gpu_transport.mjs','render_plan.mjs',
  'engines/svg-engine.mjs','engines/svg-engine.wasm',
  'engines/render-plan.mjs','engines/render-plan.wasm',
]);
// The minimum closure of build-engines.sh's current SVG/render-plan link inputs.
// Every additional manifest entry is also verified; missing required entries
// fail rather than turn a shortened manifest into successful validation.
export const REQUIRED_SOURCE_FILES=Object.freeze([
  ...['Document','Parser','Wellformedness','Namespaces','NamespaceView']
    .map(name=>`formal/lean4/L4Factoidal/XML/${name}.lean`),
  ...['Graphics','SVGPath','SVGCSS','SVGDash','SVG','RenderPlan'].map(name=>`${LAB}/${name}.lean`),
  'formal/lean4/L4Factoidal/Math/Affine.lean',
  'formal/lean4/L4Factoidal/Tdb2/Format.lean',
]);
const BRIDGES=['svg_engine','gpu_transport','render_plan'];
const BUILD_INPUTS=[`${LAB}/build-engines.sh`,`${LAB}/svg_shim.c`,`${LAB}/render_plan_shim.c`,
  `${LAB}/toolchain-versions.env`,'formal/lean4/lean-toolchain'];
const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
function git(core,args,encoding='utf8'){
  return execFileSync('git',['-C',core,...args],{encoding,stdio:['ignore','pipe','pipe']});
}
function safeRelative(path){
  if(typeof path!=='string'||!path||isAbsolute(path)||path.includes('\\')||
    path.split('/').some(part=>part===''||part==='.'||part==='..')||/[\u0000-\u001f]/u.test(path))
    throw Error(`Unsafe source path: ${JSON.stringify(path)}`);
  return path;
}
async function readRegular(core,path){
  safeRelative(path);
  const target=join(core,path),info=await lstat(target);
  if(!info.isFile()||info.isSymbolicLink())throw Error(`Expected a regular non-symlink file: ${path}`);
  const actual=await realpath(target),rel=relative(core,actual);
  if(rel==='..'||rel.startsWith('..'+sep)||isAbsolute(rel))throw Error(`File escapes source checkout: ${path}`);
  const bytes=await readFile(target);
  if(bytes.length===0)throw Error(`Empty input: ${path}`);
  return bytes;
}
async function committedBytes(core,path,head){
  const bytes=await readRegular(core,path);
  const tracked=git(core,['ls-tree',head,'--',path]).trim();
  if(!/^100(?:644|755) blob [0-9a-f]+\t/u.test(tracked))throw Error(`Source is not a committed regular file: ${path}`);
  const committed=git(core,['show',`${head}:${path}`],null);
  if(!bytes.equals(committed))throw Error(`Source differs from ${head}: ${path}`);
  return bytes;
}

export function stripBridge(source,name){
  if(typeof stripTypeScriptTypes!=='function')throw Error('Node 22.13 or later with stripTypeScriptTypes is required.');
  let output=stripTypeScriptTypes(source,{mode:'strip',sourceUrl:`${name}.ts`});
  // Only module specifiers are changed. Ordinary strings and shader contents
  // remain byte-for-byte as produced by Node's type stripper.
  let imports=0;
  output=output.replace(/^([ \t]*import[ \t]+(?:[^'";\r\n]*?[ \t]+from[ \t]*)?)(["'])([^"'\r\n]+)\2/gmu,
    (_all,prefix,quote,path)=>{
      imports++;
      const target=path.replace(/^\.\/\.build\/engines\//u,'./engines/').replace(/\.ts$/u,'.mjs');
      if(!['./render_plan.mjs','./engines/svg-engine.mjs','./engines/render-plan.mjs'].includes(target))
        throw Error(`Unexpected runtime import in ${name}: ${path}`);
      return prefix+quote+target+quote;
    });
  if([...output.matchAll(/^[ \t]*import\b/gmu)].length!==imports)
    throw Error(`Unsupported import syntax requires packaging review: ${name}`);
  // No dynamic imports exist in these bridges. Refuse a newly introduced one
  // until its packaging path and browser dependencies have been reviewed.
  if(/\bimport\s*\(/u.test(output))throw Error(`Dynamic import requires packaging review: ${name}`);
  return output;
}

export async function packageSvgRuntime({coreDir,outDir,sourceCommit,kind='development'}){
  if(kind!=='development')throw Error('Release packaging requires a trusted fresh-build wrapper and receipt; this packager only emits development packages.');
  if(typeof sourceCommit!=='string'||!/^[0-9a-f]{40}$/u.test(sourceCommit))throw Error('An exact 40-character source commit is required.');
  const core=await realpath(resolve(coreDir)),out=resolve(outDir);
  const head=git(core,['rev-parse','HEAD']).trim();
  if(head!==sourceCommit)throw Error(`Requested source commit ${sourceCommit} does not match actual checkout ${head}.`);
  if(git(core,['status','--porcelain','--untracked-files=no']).trim())
    throw Error('Tracked checkout changes must be committed before assigning source provenance.');
  const inventoryBytes=await readRegular(core,`${LAB}/.build/source-SHA256SUMS`);
  const inventory=new Map();
  for(const line of inventoryBytes.toString('utf8').trimEnd().split('\n')){
    const match=/^([0-9a-f]{64}) [ *](.+)$/u.exec(line);
    if(!match)throw Error('Malformed source-SHA256SUMS entry.');
    const path=safeRelative(match[2]);
    if(inventory.has(path))throw Error(`Duplicate source inventory entry: ${path}`);
    if(hash(await committedBytes(core,path,head))!==match[1])throw Error(`Stale source inventory: ${path}`);
    inventory.set(path,match[1]);
  }
  for(const path of REQUIRED_SOURCE_FILES)if(!inventory.has(path))throw Error(`Source inventory omits required dependency: ${path}`);

  const sourceInputs=[];
  for(const path of [...BUILD_INPUTS,...BRIDGES.map(name=>`${LAB}/${name}.ts`)]){
    const bytes=await committedBytes(core,path,head);
    sourceInputs.push({path,bytes:bytes.length,sha256:hash(bytes)});
  }
  // This scene is a compatibility marker ONLY. It has no source-commit field
  // and must never be interpreted as engine build provenance.
  const nativeBytes=await readRegular(core,`${LAB}/.build/native-artifact.json`);
  let native;
  try{native=JSON.parse(nativeBytes.toString('utf8'));}catch{throw Error('native-artifact.json is not valid JSON.');}
  if(native.abi!=='lean-graphics-v1')throw Error('Unrecognized native scene compatibility marker.');
  const tools=await readRegular(core,`${LAB}/.build/tool-versions.txt`);

  const products=new Map();
  for(const name of BRIDGES){
    const source=await committedBytes(core,`${LAB}/${name}.ts`,head);
    products.set(`${name}.mjs`,Buffer.from(stripBridge(source.toString('utf8'),name)));
  }
  for(const name of ['svg-engine','render-plan'])for(const extension of ['mjs','wasm']){
    const path=`engines/${name}.${extension}`;
    const bytes=await readRegular(core,`${LAB}/.build/${path}`);
    if(extension==='wasm'&&!bytes.subarray(0,8).equals(Buffer.from([0,97,115,109,1,0,0,0])))
      throw Error(`Missing WASM v1 header: ${path}`);
    products.set(path,bytes);
  }
  const manifest={format:'factoidal-svg-webgpu-runtime-v1',kind,sourceCommit:head,
    files:REQUIRED_RUNTIME_FILES.map(path=>({path,bytes:products.get(path).length,sha256:hash(products.get(path))})),
    evidence:{qualification:'Development package: engine/source correspondence and GPU behavior are not established by packaging.',
      sourceInventorySha256:hash(inventoryBytes),sourceInventoryEntries:inventory.size,
      sourceInputs,toolVersions:tools.toString('utf8'),packagingNode:process.version,
      nativeScene:{role:'compatibility marker, not build provenance',sha256:hash(nativeBytes)}}};
  // Refuse replacement of an existing package. Publish the complete directory
  // only after every validation/read succeeds; never leave a half package.
  try{await lstat(out);throw Error(`Output already exists: ${out}`);}catch(error){if(error.code!=='ENOENT')throw error;}
  await mkdir(dirname(out),{recursive:true});
  const stage=await mkdtemp(join(dirname(out),'.svg-runtime-'));
  try{
    for(const [path,bytes] of products){await mkdir(dirname(join(stage,path)),{recursive:true});await writeFile(join(stage,path),bytes);}
    await writeFile(join(stage,'provenance.json'),JSON.stringify(manifest,null,2)+'\n');
    await rename(stage,out);
  }catch(error){await rm(stage,{recursive:true,force:true});throw error;}
  return manifest;
}

async function main(args){
  const options={};
  const names=new Map([['--core','coreDir'],['--out','outDir'],['--source-commit','sourceCommit'],['--kind','kind']]);
  while(args.length){const key=args.shift();if(!names.has(key)||!args.length||Object.hasOwn(options,names.get(key)))throw Error('Usage: node scripts/package-svg-runtime.mjs --core CHECKOUT --out NEW_DIRECTORY --source-commit SHA [--kind development]');options[names.get(key)]=args.shift();}
  if(!options.coreDir||!options.outDir)throw Error('--core and --out are required.');
  const result=await packageSvgRuntime(options);
  console.log(`Packaged ${result.files.length} SVG runtime files (${result.kind}) from ${result.sourceCommit}; no rendering/build verification claimed.`);
}
if(process.argv[1]&&import.meta.url===pathToFileURL(resolve(process.argv[1])).href)
  main(process.argv.slice(2)).catch(error=>{console.error(error.message);process.exitCode=1;});
