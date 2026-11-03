// Tiny FAKE sources/WASM headers exercise packaging controls, not a renderer.
import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp,mkdir,writeFile,readFile,rm,access,symlink} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {packageHtmlRuntime,stripHtmlBridge,HTML_RUNTIME_FILES} from '../scripts/package-html-runtime.mjs';
import {finalizeHtmlRuntime} from '../scripts/finalize-html-runtime.mjs';
const LAB='labs/demos/foafnaut',BUILD=LAB+'/.build/web-render',hash=b=>createHash('sha256').update(b).digest('hex');
async function fixture(t,{rdf=false,font=false,document=false,initializer}={}){
 const root=await mkdtemp(join(tmpdir(),'html-runtime-test-'));t.after(()=>rm(root,{recursive:true,force:true}));
 const core=join(root,'core'),out=join(root,'runtime');await mkdir(core);
 const put=async(p,b)=>{await mkdir(join(core,p,'..'),{recursive:true});await writeFile(join(core,p),b);};
 const sources={
  [LAB+'/WebRender.lean']:'import L4Factoidal.Rendering.Fixture\n',
  ['formal/lean4/L4Factoidal/Rendering/Fixture.lean']:'-- fake source dependency\n',
  [LAB+'/RenderPlan.lean']:'-- fake render plan\n',
  [LAB+'/build-web-render.sh']:'fake build input\n',[LAB+'/web_render_shim.c']:'initialize_WebRender(1);\n',
  [LAB+'/render_plan_shim.c']:'fake C shim\n',[LAB+'/toolchain-versions.env']:'fake toolchain\n',
  ['formal/lean4/lean-toolchain']:'fake Lean version\n'};
 if(rdf||font){sources[LAB+'/WebRenderRDF.lean']='import WebRender\nimport L4Factoidal.Rendering.RdfFixture\n';sources['formal/lean4/L4Factoidal/Rendering/RdfFixture.lean']='-- fake RDF parser dependency\n';sources[LAB+'/web_render_shim.c']='initialize_WebRenderRDF(1);\n';}
 if(font){sources[LAB+'/WebRenderFont.lean']='import WebRender\nimport L4Factoidal.Rendering.FontFixture\n';sources['formal/lean4/L4Factoidal/Rendering/FontFixture.lean']='-- fake supplied font dependency\n';sources[LAB+'/web_render_shim.c']+='initialize_WebRenderFont(1);\n';}
 if(document){
  sources[LAB+'/WebDocument.lean']='import WebRenderScript\nimport WebRenderFontRequests\n';
  sources[LAB+'/WebRenderScript.lean']='import WebRender\nimport L4Factoidal.DOM.ScriptFixture\n';
  sources[LAB+'/WebRenderFontRequests.lean']='import WebRender\nimport L4Factoidal.Rendering.FontRequestsFixture\n';
  sources['formal/lean4/L4Factoidal/DOM/ScriptFixture.lean']='-- fake DOM mutation dependency\n';
  sources['formal/lean4/L4Factoidal/Rendering/FontRequestsFixture.lean']='-- fake computed font request dependency\n';
  sources[LAB+'/web_render_shim.c']+='initialize_WebDocument(1);\n';
 }
 if(initializer)sources[LAB+'/web_render_shim.c']=`initialize_${initializer}(1);\n`;
 for(const[p,b]of Object.entries(sources))await put(p,b);
 await put(LAB+'/gpu_transport.ts','import {x} from "./render_plan.ts";\nexport const y:number=x;\n');
 await put(LAB+'/render_plan.ts','import create from "./.build/engines/render-plan.mjs";\nexport const x:number=1;\nexport {create};\n');
 await put('.gitignore',LAB+'/.build/\n');
 const git=a=>execFileSync('git',['-C',core,...a],{encoding:'utf8',stdio:['ignore','pipe','pipe']}).trim();
 git(['init','-q']);git(['add','.']);git(['-c','user.name=Packaging Test','-c','user.email=test@example.invalid','commit','-qm','Fake HTML packaging inputs']);
 const sha=git(['rev-parse','HEAD']);
 const witness={format:'factoidal-web-render-source-witness-v1',commit:sha,
  files:Object.fromEntries(Object.entries(sources).map(([p,b])=>[p,hash(b)])),
  generatedC:{[BUILD+'/fixture.c']:hash('fake generated C')},engines:{},
  runtimeObjectWitness:'wasm32-string-list-v1\n'+'a'.repeat(64)+'\n'+'b'.repeat(64)+'\n'};
 await put(BUILD+'/fixture.c','fake generated C');
 for(const name of ['web-render.mjs','web-render.wasm','render-plan.mjs','render-plan.wasm']){
  const p=BUILD+'/engines/'+name,b=name.endsWith('.wasm')?Buffer.from([0,97,115,109,1,0,0,0]):Buffer.from('export default ()=>1;');
  await put(p,b);witness.engines[p]=hash(b);
 }
 const save=()=>put(BUILD+'/source-witness.json',JSON.stringify(witness));await save();
 return {core,out,sha,put,witness,save,run:extra=>packageHtmlRuntime({coreDir:core,outDir:out,sourceCommit:sha,...extra})};
}
test('exact complete package relocates canonical hosts and validates source closure',async t=>{
 const f=await fixture(t),m=await f.run();assert.deepEqual(m.files.map(x=>x.path),HTML_RUNTIME_FILES);
 for(const row of m.files){const b=await readFile(join(f.out,row.path));assert.equal(hash(b),row.sha256);assert.equal(b.length,row.bytes);}
 assert.match(await readFile(join(f.out,'gpu-transport.mjs'),'utf8'),/render-plan-host\.mjs/);
 assert.match(await readFile(join(f.out,'render-plan-host.mjs'),'utf8'),/from "\.\/render-plan\.mjs"/);
 assert.equal(m.kind,'development');assert.match(m.evidence.qualification,/not a compiler/);
});
test('RDF shim entry requires the entire additional Lean import closure',async t=>{
 const f=await fixture(t,{rdf:true});await f.run();
 const g=await fixture(t,{rdf:true});delete g.witness.files['formal/lean4/L4Factoidal/Rendering/RdfFixture.lean'];await g.save();
 await assert.rejects(g.run(),/omits source dependency/);
 const h=await fixture(t,{rdf:true});delete h.witness.files[LAB+'/WebRenderRDF.lean'];await h.save();
 await assert.rejects(h.run(),/omits source dependency/);
});
test('multiple initializers require both RDF and supplied-font source closures',async t=>{
 const f=await fixture(t,{font:true});await f.run();
 for(const path of [LAB+'/WebRenderRDF.lean',LAB+'/WebRenderFont.lean','formal/lean4/L4Factoidal/Rendering/FontFixture.lean']){
  const g=await fixture(t,{font:true});delete g.witness.files[path];await g.save();await assert.rejects(g.run(),/omits source dependency/);
 }
 const h=await fixture(t,{initializer:'Unreviewed'});await assert.rejects(h.run(),/initializer requires review/);
});
test('document initializer requires script and font-request transitive source witnesses',async t=>{
 const f=await fixture(t,{font:true,document:true});
 const manifest=await f.run();assert.deepEqual(manifest.files.map(row=>row.path),HTML_RUNTIME_FILES);
 for(const path of [LAB+'/WebDocument.lean',LAB+'/WebRenderScript.lean',LAB+'/WebRenderFontRequests.lean',
   'formal/lean4/L4Factoidal/DOM/ScriptFixture.lean','formal/lean4/L4Factoidal/Rendering/FontRequestsFixture.lean']){
  const g=await fixture(t,{font:true,document:true});delete g.witness.files[path];await g.save();
  await assert.rejects(g.run(),/omits source dependency/);await assert.rejects(access(g.out));
 }
 const h=await fixture(t,{document:true});await h.put(LAB+'/WebRenderScript.lean','-- changed mutation implementation\n');
 await assert.rejects(h.run(),/Uncommitted source/);
});
test('wrong revision, dirty source and direct release labels fail',async t=>{
 const f=await fixture(t);await assert.rejects(f.run({sourceCommit:'f'.repeat(40)}),/source differs/);
 await assert.rejects(f.run({kind:'release'}),/trusted fresh-build/);
 await f.put(LAB+'/WebRender.lean','changed');await assert.rejects(f.run(),/Uncommitted source/);await assert.rejects(access(f.out));
});
test('removed transitive source and required shim entries fail loudly',async t=>{
 const f=await fixture(t);delete f.witness.files['formal/lean4/L4Factoidal/Rendering/Fixture.lean'];await f.save();
 await assert.rejects(f.run(),/omits source dependency/);
 const g=await fixture(t);delete g.witness.files[LAB+'/web_render_shim.c'];await g.save();await assert.rejects(g.run(),/omits required input/);
});
test('tampered C, engines and absent runtime patch receipts fail',async t=>{
 const f=await fixture(t);await f.put(BUILD+'/fixture.c','changed');await assert.rejects(f.run(),/Stale generated C/);
 const g=await fixture(t);await g.put(BUILD+'/engines/web-render.wasm','changed');await assert.rejects(g.run(),/Engine differs/);
 const h=await fixture(t);delete h.witness.runtimeObjectWitness;await h.save();await assert.rejects(h.run(),/runtime witness/);
});
test('unsafe source names, symlinked engines and output replacement fail',async t=>{
 const f=await fixture(t);f.witness.files['../escape']='0'.repeat(64);await f.save();await assert.rejects(f.run(),/Unsafe source path/);
 const g=await fixture(t);await rm(join(g.core,BUILD+'/engines/web-render.wasm'));await symlink('render-plan.wasm',join(g.core,BUILD+'/engines/web-render.wasm'));await assert.rejects(g.run(),/regular file/);
 const h=await fixture(t);await mkdir(h.out);await writeFile(join(h.out,'keep'),'keep');await assert.rejects(h.run(),/already exists/);assert.equal(await readFile(join(h.out,'keep'),'utf8'),'keep');
});
test('unreviewed transport imports and dynamic imports are rejected',()=>{
 assert.throws(()=>stripHtmlBridge('import x from "node:fs";','gpu_transport'),/Unexpected transport/);
 assert.throws(()=>stripHtmlBridge('import x from "./render_plan.ts";\nconst y=import("x");','gpu_transport'),/require review/);
});
test('finalization records exact trusted workflow and refuses tampering or revision changes',async t=>{
 const f=await fixture(t);await f.run();const options={runtimeDir:f.out,sourceCommit:f.sha,buildRun:'https://github.com/danbri/factoidal-builds/actions/runs/123'};
 await assert.rejects(finalizeHtmlRuntime({...options,sourceCommit:'f'.repeat(40)}),/Same-source/);
 await assert.rejects(finalizeHtmlRuntime({...options,buildRun:'https://example.invalid/run'}),/workflow run/);
 const m=await finalizeHtmlRuntime(options);assert.equal(m.kind,'release');assert.match(m.evidence.qualification,/not full HTML/);
 await assert.rejects(finalizeHtmlRuntime(options),/Same-source/);
 const g=await fixture(t);await g.run();await writeFile(join(g.out,'web-render.wasm'),'changed');
 await assert.rejects(finalizeHtmlRuntime({...options,runtimeDir:g.out,sourceCommit:g.sha}),/integrity mismatch/);
});
