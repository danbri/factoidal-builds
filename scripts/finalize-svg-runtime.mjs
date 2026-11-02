#!/usr/bin/env node
// Called only by publish.sh, after it verifies the core commit is on main.
// This converts a fresh, tested same-run development package into the durable
// release-set form. It does not claim SVG conformance or GPU correctness.
import {createHash} from 'node:crypto';
import {readFile,writeFile,rename,lstat,rm} from 'node:fs/promises';
import {resolve,join} from 'node:path';
import {pathToFileURL} from 'node:url';
import {REQUIRED_RUNTIME_FILES} from './package-svg-runtime.mjs';

const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
const RUN_URL=/^https:\/\/github\.com\/danbri\/factoidal-builds\/actions\/runs\/[0-9]+$/u;

export async function finalizeSvgRuntime({runtimeDir,sourceCommit,buildRun}){
  if(typeof sourceCommit!=='string'||!/^[0-9a-f]{40}$/u.test(sourceCommit))throw Error('An exact core source commit is required.');
  if(typeof buildRun!=='string'||!RUN_URL.test(buildRun))throw Error('Expected the exact Factoidal Builds workflow run URL.');
  const root=resolve(runtimeDir),manifestPath=join(root,'provenance.json');
  let manifest;try{manifest=JSON.parse(await readFile(manifestPath,'utf8'));}catch{throw Error('SVG runtime provenance is missing or invalid JSON.');}
  if(manifest.format!=='factoidal-svg-webgpu-runtime-v1'||manifest.kind!=='development'||manifest.sourceCommit!==sourceCommit)
    throw Error('Only a same-source development package can be finalized for a release.');
  if(!Array.isArray(manifest.files)||manifest.files.length!==REQUIRED_RUNTIME_FILES.length)throw Error('SVG runtime inventory is incomplete.');
  const byPath=new Map();
  for(const row of manifest.files){
    if(!row||typeof row.path!=='string'||byPath.has(row.path))throw Error('SVG runtime inventory has an invalid or duplicate path.');
    if(!REQUIRED_RUNTIME_FILES.includes(row.path))throw Error(`SVG runtime inventory contains an unexpected path: ${row.path}.`);
    byPath.set(row.path,row);
  }
  for(const path of REQUIRED_RUNTIME_FILES){
    const row=byPath.get(path);if(!row)throw Error(`SVG runtime inventory omits ${path}.`);
    const info=await lstat(join(root,path));
    if(!info.isFile()||info.isSymbolicLink())throw Error(`SVG runtime file is not a regular file: ${path}.`);
    const bytes=await readFile(join(root,path));
    if(!Number.isSafeInteger(row.bytes)||row.bytes!==bytes.length||row.sha256!==hash(bytes))throw Error(`SVG runtime integrity check failed: ${path}.`);
    if(path.endsWith('.wasm')&&!bytes.subarray(0,8).equals(Buffer.from([0,97,115,109,1,0,0,0])))throw Error(`Invalid WASM v1 module: ${path}.`);
  }
  manifest.kind='release';
  manifest.evidence={...manifest.evidence,
    qualification:'Fresh Lean/WASM build and named source tests passed in the recorded workflow run; this records build/source identity, not SVG conformance or GPU correctness.',
    releaseBuildRun:buildRun};
  const temp=manifestPath+'.tmp';
  try{
    await writeFile(temp,JSON.stringify(manifest,null,2)+'\n',{flag:'wx'});
    await rename(temp,manifestPath);
  }catch(error){await rm(temp,{force:true});throw error;}
  return manifest;
}

async function main(args){
  const values={};const names=new Map([['--runtime','runtimeDir'],['--source-commit','sourceCommit'],['--build-run','buildRun']]);
  while(args.length){const key=args.shift();if(!names.has(key)||!args.length||Object.hasOwn(values,names.get(key)))throw Error('Usage: node scripts/finalize-svg-runtime.mjs --runtime DIR --source-commit SHA --build-run URL');values[names.get(key)]=args.shift();}
  if(!values.runtimeDir||!values.sourceCommit||!values.buildRun)throw Error('All finalization arguments are required.');
  const result=await finalizeSvgRuntime(values);console.log(`Finalized ${result.files.length} checked SVG runtime assets for ${result.sourceCommit}.`);
}
if(process.argv[1]&&import.meta.url===pathToFileURL(resolve(process.argv[1])).href)
  main(process.argv.slice(2)).catch(error=>{console.error(error.message);process.exitCode=1;});
