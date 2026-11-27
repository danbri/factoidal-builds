// The Wasm module, run by Node's V8: the same loop as ref.c (the decoder finds each frame in the
// rest of the file). Checks that the module computes what the same C computes natively.
import fs from "node:fs";
const [wasmPath, mp3Path, outPath] = process.argv.slice(2);
const mod = new WebAssembly.Module(fs.readFileSync(wasmPath));
console.log("imports:", JSON.stringify(WebAssembly.Module.imports(mod)));
const stubs = {};
for (const i of WebAssembly.Module.imports(mod)) (stubs[i.module] ??= {})[i.name] = () => 0;
const inst = new WebAssembly.Instance(mod, stubs);
const x = inst.exports;
if (x._initialize) x._initialize();
console.log("abi", x.mw_abi());
const file = fs.readFileSync(mp3Path);
const ptr = x.mw_alloc(file.length);
new Uint8Array(x.memory.buffer, ptr, file.length).set(file);
x.mw_mp3_init();
const out = []; let off = 0, frames = 0, samples = 0;
while (off < file.length) {
  const s = x.mw_mp3_decode(ptr + off, file.length - off);
  const used = x.mw_mp3_info(0);
  if (used === 0) break;
  off += used;
  if (s > 0) {
    const ch = x.mw_mp3_info(1);
    out.push(Buffer.from(new Float32Array(x.memory.buffer, x.mw_pcm_f32(), s * ch).slice().buffer));
    frames++; samples += s;
  }
}
fs.writeFileSync(outPath, Buffer.concat(out));
console.log(`${mp3Path}: ${frames} frames, ${samples} samples per channel, ${x.mw_mp3_info(1)} channels, ${x.mw_mp3_info(2)} Hz`);
