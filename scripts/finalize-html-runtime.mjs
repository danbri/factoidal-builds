#!/usr/bin/env node
// publish.sh calls this only after its main-ancestry check and fresh-build gates.
import {readFile,writeFile,rename,lstat,rm} from 'node:fs/promises';
import {resolve,join} from 'node:path';
import {pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
import {HTML_RUNTIME_FILES} from './package-html-runtime.mjs';
const hash=b=>createHash('sha256').update(b).digest('hex');
export async function finalizeHtmlRuntime({runtimeDir,sourceCommit,buildRun}){
 if(!/^[0-9a-f]{40}$/u.test(sourceCommit??''))throw Error('Exact source commit required');
 if(!/^https:\/\/github\.com\/danbri\/factoidal-builds\/actions\/runs\/[0-9]+$/u.test(buildRun??''))throw Error('Exact Builds workflow run URL required');
 const root=resolve(runtimeDir),path=join(root,'manifest.json');
 const manifest=JSON.parse(await readFile(path,'utf8'));
 if(manifest.format!=='factoidal-html-webgpu-runtime-v1'||manifest.kind!=='development'||manifest.sourceCommit!==sourceCommit)throw Error('Same-source development package required');
 if(!Array.isArray(manifest.files)||manifest.files.length!==HTML_RUNTIME_FILES.length)throw Error('Incomplete HTML runtime inventory');
 const seen=new Set();
 for(const row of manifest.files){
  if(!row||!HTML_RUNTIME_FILES.includes(row.path)||seen.has(row.path))throw Error('Unexpected or duplicate runtime path');seen.add(row.path);
  const file=join(root,row.path),info=await lstat(file);
  if(!info.isFile()||info.isSymbolicLink())throw Error('Runtime file must be regular');
  const data=await readFile(file);
  if(row.bytes!==data.length||row.sha256!==hash(data))throw Error('HTML runtime integrity mismatch');
  if(row.path.endsWith('.wasm')&&!data.subarray(0,8).equals(Buffer.from([0,97,115,109,1,0,0,0])))throw Error('Invalid WASM module');
 }
 manifest.kind='release';manifest.evidence={...manifest.evidence,releaseBuildRun:buildRun,
  qualification:'Fresh targeted Lean/WASM build and named source/ABI checks passed in the recorded workflow; this is build identity, not full HTML/SVG conformance or GPU/compiler correctness.'};
 const tmp=path+'.tmp';
 try{await writeFile(tmp,JSON.stringify(manifest,null,2)+'\n',{flag:'wx'});await rename(tmp,path);}
 catch(error){await rm(tmp,{force:true});throw error;}
 return manifest;
}
async function main(args){
 const values={},names=new Map([['--runtime','runtimeDir'],['--source-commit','sourceCommit'],['--build-run','buildRun']]);
 while(args.length){const key=args.shift();if(!names.has(key)||!args.length||Object.hasOwn(values,names.get(key)))throw Error('Expected --runtime DIR --source-commit SHA --build-run URL');values[names.get(key)]=args.shift();}
 if(!values.runtimeDir)throw Error('Runtime directory required');
 const result=await finalizeHtmlRuntime(values);console.log(`Finalized${result.files.length} HTML runtime files`);
}
if(process.argv[1]&&import.meta.url===pathToFileURL(resolve(process.argv[1])).href)main(process.argv.slice(2)).catch(e=>{console.error(e.message);process.exitCode=1;});
