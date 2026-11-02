import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp,mkdir,writeFile,readFile,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {createHash} from 'node:crypto';
import {finalizeSvgRuntime} from '../scripts/finalize-svg-runtime.mjs';
import {REQUIRED_RUNTIME_FILES} from '../scripts/package-svg-runtime.mjs';

const sha=b=>createHash('sha256').update(b).digest('hex');
async function fixture(t){
  const root=await mkdtemp(join(tmpdir(),'svg-finalize-test-'));t.after(()=>rm(root,{recursive:true,force:true}));
  const files=[];
  for(const path of REQUIRED_RUNTIME_FILES){
    const body=path.endsWith('.wasm')?Buffer.from([0,97,115,109,1,0,0,0,1]):Buffer.from(`fixture ${path}`);
    await mkdir(join(root,path,'..'),{recursive:true});await writeFile(join(root,path),body);
    files.push({path,bytes:body.length,sha256:sha(body)});
  }
  const manifest={format:'factoidal-svg-webgpu-runtime-v1',kind:'development',sourceCommit:'a'.repeat(40),files,evidence:{qualification:'development only'}};
  await writeFile(join(root,'provenance.json'),JSON.stringify(manifest));return {root,manifest};
}
const run=({root,manifest},overrides={})=>finalizeSvgRuntime({runtimeDir:root,sourceCommit:manifest.sourceCommit,buildRun:'https://github.com/danbri/factoidal-builds/actions/runs/41270048119',...overrides});

test('same-source complete development package finalizes with explicit build scope',async t=>{
  const f=await fixture(t),result=await run(f);
  assert.equal(result.kind,'release');assert.equal(result.evidence.releaseBuildRun,'https://github.com/danbri/factoidal-builds/actions/runs/41270048119');
  assert.match(result.evidence.qualification,/not SVG conformance/);
  assert.deepEqual(JSON.parse(await readFile(join(f.root,'provenance.json'),'utf8')),result);
});
test('wrong source, non-development packages and invalid run URL are refused',async t=>{
  const f=await fixture(t);await assert.rejects(run(f,{sourceCommit:'b'.repeat(40)}),/same-source/);
  const g=await fixture(t);g.manifest.kind='release';await writeFile(join(g.root,'provenance.json'),JSON.stringify(g.manifest));
  await assert.rejects(run(g),/same-source/);
  const h=await fixture(t);await assert.rejects(run(h,{buildRun:'https://example.com/attestation'}),/workflow run URL/);
});
test('missing, unexpected, tampered and malformed WASM inventory entries fail closed',async t=>{
  const f=await fixture(t);await writeFile(join(f.root,REQUIRED_RUNTIME_FILES[0]),'tampered');await assert.rejects(run(f),/integrity/);
  const g=await fixture(t);g.manifest.files.pop();await writeFile(join(g.root,'provenance.json'),JSON.stringify(g.manifest));await assert.rejects(run(g),/incomplete/);
  const h=await fixture(t);h.manifest.files[0].path='../outside';await writeFile(join(h.root,'provenance.json'),JSON.stringify(h.manifest));await assert.rejects(run(h),/unexpected path/);
  const k=await fixture(t);await writeFile(join(k.root,'engines/svg-engine.wasm'),'not wasm');
  const idx=k.manifest.files.findIndex(x=>x.path==='engines/svg-engine.wasm');k.manifest.files[idx]={path:'engines/svg-engine.wasm',bytes:8,sha256:sha(Buffer.from('not wasm'))};await writeFile(join(k.root,'provenance.json'),JSON.stringify(k.manifest));await assert.rejects(run(k),/WASM v1/);
});
