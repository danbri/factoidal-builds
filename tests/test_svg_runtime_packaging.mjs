// Packaging controls with tiny FAKE engine/source files. These are not Lean,
// GPU, rendering, source/binary-equivalence or WASM execution evidence.
import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp,mkdir,writeFile,readFile,rm,access,symlink} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {pathToFileURL} from 'node:url';
import {packageSvgRuntime,stripBridge,REQUIRED_RUNTIME_FILES,REQUIRED_SOURCE_FILES} from '../scripts/package-svg-runtime.mjs';

const LAB='labs/demos/foafnaut';
const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
async function fixture(t){
  const root=await mkdtemp(join(tmpdir(),'svg-package-test-'));
  t.after(()=>rm(root,{recursive:true,force:true}));
  const core=join(root,'core'),out=join(root,'package');
  await mkdir(core);
  const put=async(path,body)=>{await mkdir(join(core,path,'..'),{recursive:true});await writeFile(join(core,path),body);};
  const git=args=>execFileSync('git',['-C',core,...args],{encoding:'utf8',stdio:['ignore','pipe','pipe']}).trim();
  const inputs=new Map(REQUIRED_SOURCE_FILES.map(path=>[path,`-- FAKE packaging fixture: ${path}\n`]));
  for(const [path,body] of inputs)await put(path,body);
  await put('.gitignore',`${LAB}/.build/\n`);
  for(const path of ['build-engines.sh','svg_shim.c','render_plan_shim.c','toolchain-versions.env'])
    await put(`${LAB}/${path}`,`FAKE packaging fixture ${path}\n`);
  await put('formal/lean4/lean-toolchain','FAKE packaging fixture toolchain\n');
  await put(`${LAB}/svg_engine.ts`,'import create from "./.build/engines/svg-engine.mjs";\nexport const value:number=3;\nexport {create};\n');
  await put(`${LAB}/gpu_transport.ts`,'import type {Removed} from "./not-packaged.ts";\nimport {value} from "./render_plan.ts";\nexport const data:number=value;\n');
  await put(`${LAB}/render_plan.ts`,'import create from "./.build/engines/render-plan.mjs";\nexport const value:number=4;\nexport {create};\n');
  git(['init','-q']);git(['add','.']);git(['-c','user.name=Packaging Test','-c','user.email=test@example.invalid','commit','-qm','Fake packaging fixtures']);
  const sha=git(['rev-parse','HEAD']);
  const manifest=[...inputs].map(([path,body])=>`${hash(body)}  ${path}`).join('\n')+'\n';
  await put(`${LAB}/.build/source-SHA256SUMS`,manifest);
  await put(`${LAB}/.build/native-artifact.json`,JSON.stringify({abi:'lean-graphics-v1',fixture:true}));
  await put(`${LAB}/.build/tool-versions.txt`,'FAKE packaging fixture versions\n');
  for(const name of ['svg-engine','render-plan']){
    await put(`${LAB}/.build/engines/${name}.mjs`,'// FAKE packaging fixture; no Lean or GPU\nexport default function(){return "fixture";}\n');
    await put(`${LAB}/.build/engines/${name}.wasm`,Buffer.from([0,97,115,109,1,0,0,0]));
  }
  return {core,out,sha,put,git,manifest,run:extra=>packageSvgRuntime({coreDir:core,outDir:out,sourceCommit:sha,...extra})};
}

test('development package strips actual TS syntax, relocates imports, and hashes every output',async t=>{
  const f=await fixture(t),manifest=await f.run();
  assert.equal(manifest.kind,'development');assert.equal(manifest.sourceCommit,f.sha);
  assert.deepEqual(manifest.files.map(row=>row.path),REQUIRED_RUNTIME_FILES);
  assert.deepEqual(JSON.parse(await readFile(join(f.out,'provenance.json'),'utf8')),manifest);
  for(const row of manifest.files){const bytes=await readFile(join(f.out,row.path));assert.equal(row.sha256,hash(bytes));assert.equal(row.bytes,bytes.length);}
  const bridge=await readFile(join(f.out,'svg_engine.mjs'),'utf8');
  assert.match(bridge,/from "\.\/engines\/svg-engine\.mjs"/);
  assert.doesNotMatch(bridge,/:number|\.build/);
  const transport=await readFile(join(f.out,'gpu_transport.mjs'),'utf8');
  assert.match(transport,/from "\.\/render_plan\.mjs"/);assert.doesNotMatch(transport,/not-packaged/);
  assert.equal((await import(pathToFileURL(join(f.out,'gpu_transport.mjs')).href)).data,4);
  assert.match(manifest.evidence.qualification,/not established/);
  assert.equal(manifest.evidence.sourceInventorySha256,hash(f.manifest));
});

test('release label cannot be assigned to existing or warm artifacts',async t=>{
  const f=await fixture(t);await assert.rejects(f.run({kind:'release'}),/trusted fresh-build wrapper/);
  await assert.rejects(access(f.out));
});
test('requested commit must equal actual checkout HEAD',async t=>{
  const f=await fixture(t);await assert.rejects(f.run({sourceCommit:'f'.repeat(40)}),/does not match actual checkout/);
});
test('dirty tracked source cannot be labelled with the old commit',async t=>{
  const f=await fixture(t);await f.put(`${LAB}/svg_engine.ts`,'export const modified=true;');
  await assert.rejects(f.run(),/Tracked checkout changes/);
});
test('stale source checksum fails without emitting a package',async t=>{
  const f=await fixture(t);await f.put(`${LAB}/.build/source-SHA256SUMS`,f.manifest.replace(/^[0-9a-f]{64}/u,'0'.repeat(64)));
  await assert.rejects(f.run(),/Stale source inventory/);await assert.rejects(access(f.out));
});
test('shortened, duplicate and traversing source manifests are refused',async t=>{
  const f=await fixture(t);
  await f.put(`${LAB}/.build/source-SHA256SUMS`,f.manifest.split('\n').slice(1).join('\n'));
  await assert.rejects(f.run(),/omits required dependency/);
  await f.put(`${LAB}/.build/source-SHA256SUMS`,f.manifest+f.manifest.split('\n')[0]+'\n');
  await assert.rejects(f.run(),/Duplicate source inventory/);
  await f.put(`${LAB}/.build/source-SHA256SUMS`,'0'.repeat(64)+'  ../outside\n');
  await assert.rejects(f.run(),/Unsafe source path/);
});
for(const module of ['SVGCSS','SVGDash','SVGDashUnits'])test(`omitting the ${module} producer dependency is refused`,async t=>{
  const f=await fixture(t);
  await f.put(`${LAB}/.build/source-SHA256SUMS`,f.manifest.split('\n').filter(line=>!line.endsWith('/'+module+'.lean')).join('\n'));
  await assert.rejects(f.run(),new RegExp('omits required dependency: .*'+module+'\\.lean'));
  await assert.rejects(access(f.out));
});
test('missing engines and non-WASM bytes fail instead of producing an incomplete runtime',async t=>{
  const f=await fixture(t);await rm(join(f.core,`${LAB}/.build/engines/svg-engine.wasm`));
  await assert.rejects(f.run(),/ENOENT/);
  await f.put(`${LAB}/.build/engines/svg-engine.wasm`,'this is not wasm');
  await assert.rejects(f.run(),/WASM v1 header/);await assert.rejects(access(f.out));
});
test('engine symlinks and unknown native scene markers are refused',async t=>{
  const f=await fixture(t),engine=join(f.core,`${LAB}/.build/engines/svg-engine.wasm`);
  await rm(engine);await symlink('render-plan.wasm',engine);
  await assert.rejects(f.run(),/non-symlink/);
  await rm(engine);await f.put(`${LAB}/.build/engines/svg-engine.wasm`,Buffer.from([0,97,115,109,1,0,0,0]));
  await f.put(`${LAB}/.build/native-artifact.json`,'{"abi":"wrong"}');
  await assert.rejects(f.run(),/compatibility marker/);
});
test('existing output is never overwritten',async t=>{
  const f=await fixture(t);await mkdir(f.out);await writeFile(join(f.out,'keep'),'keep');
  await assert.rejects(f.run(),/Output already exists/);assert.equal(await readFile(join(f.out,'keep'),'utf8'),'keep');
});
test('rewriting only touches static imports and refuses unreviewed runtime dependencies',()=>{
  const input='import {x} from "./render_plan.ts";\nexport const sample:string=\'from "./render_plan.ts"\';\n';
  const output=stripBridge(input,'test');
  assert.match(output,/from "\.\/render_plan\.mjs"/);assert.match(output,/\'from "\.\/render_plan\.ts"\'/);
  assert.throws(()=>stripBridge('import x from "node:fs";','test'),/Unexpected runtime import/);
  assert.throws(()=>stripBridge('const x=import("./render_plan.ts");','test'),/Dynamic import/);
});
