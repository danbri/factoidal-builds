// The float exports of interface version 2 against the 16-bit exports of version 1, on the same
// packets: libopus's 16-bit output is its float output rounded (FLOAT2INT16), and the Vorbis entry's
// 16-bit output is clip() of the float output, so each 16-bit sample must equal the float sample
// converted that way.
import fs from "node:fs";
const W = "/home/user/media-build/chain/wasm/";
function oggPackets(buf) { // minimal Ogg reader: packets in page order (one logical stream)
  const out = []; let cur = []; let p = 0;
  while (p + 27 <= buf.length && buf.toString("latin1", p, p + 4) === "OggS") {
    const nseg = buf[p + 26]; const table = buf.subarray(p + 27, p + 27 + nseg); let q = p + 27 + nseg;
    for (const len of table) { cur.push(buf.subarray(q, q + len)); q += len; if (len < 255) { out.push(Buffer.concat(cur)); cur = []; } }
    p = q;
  }
  return out;
}
function inst(name) {
  const mod = new WebAssembly.Module(fs.readFileSync(W + name));
  const stubs = {}; for (const i of WebAssembly.Module.imports(mod)) (stubs[i.module] ??= {})[i.name] = () => 0;
  const x = new WebAssembly.Instance(mod, stubs).exports; if (x._initialize) x._initialize(); return x;
}
function put(x, pkt) { const p = x.mw_alloc(pkt.length); new Uint8Array(x.memory.buffer, p, pkt.length).set(pkt); return p; }
// libopus FLOAT2INT16: scale, clamp to [-32768, 32767], then lrintf (round half to even)
const lrintf = x => { const r = Math.round(x); return (Math.abs(x % 1) === 0.5) ? 2 * Math.round(x / 2) : r; };
const f2i_opus = f => lrintf(Math.max(-32768, Math.min(32767, Math.fround(f * 32768))));
const f2i_vorbis = f => { let v = Math.trunc(Math.fround(Math.fround(f * 32767) + (f < 0 ? -0.5 : 0.5))); return Math.max(-32768, Math.min(32767, v)); };
// Opus: two instances, one per path
{ const pk = oggPackets(fs.readFileSync("/home/user/factoidal-core/third_party/media/arpeggio.opus"));
  const ch = pk[0][9]; const a = inst("opus-wasmvm.wasm"), b = inst("opus-wasmvm.wasm");
  a.mw_opus_init(ch); b.mw_opus_init(ch); let n16 = 0, bad = 0;
  for (const pkt of pk.slice(2)) {
    const na = a.mw_opus_decode(put(a, pkt), pkt.length), nb = b.mw_opus_decode_f32(put(b, pkt), pkt.length);
    if (na !== nb) { bad++; continue; }
    const s = new Int16Array(a.memory.buffer, a.mw_pcm(), na * ch), f = new Float32Array(b.memory.buffer, b.mw_pcm_f32(), nb * ch);
    for (let i = 0; i < na * ch; i++) { n16++; if (s[i] !== f2i_opus(f[i])) bad++; }
  }
  console.log(`Opus: abi ${a.mw_abi()}; ${n16} samples; ${bad} differ between the 16-bit and the float export`); }
// Vorbis
{ const pk = oggPackets(fs.readFileSync("/home/user/factoidal-core/third_party/media/arpeggio.ogg"));
  const a = inst("vorbis-wasmvm.wasm"), b = inst("vorbis-wasmvm.wasm");
  for (let i = 0; i < 3; i++) { a.mw_vorbis_header(put(a, pk[i]), pk[i].length, i); b.mw_vorbis_header(put(b, pk[i]), pk[i].length, i); }
  const ch = a.mw_vorbis_channels(); let n16 = 0, bad = 0;
  for (const pkt of pk.slice(3)) {
    const na = a.mw_vorbis_decode(put(a, pkt), pkt.length), nb = b.mw_vorbis_decode_f32(put(b, pkt), pkt.length);
    if (na !== nb) { bad++; continue; }
    const s = new Int16Array(a.memory.buffer, a.mw_pcm(), na * ch), f = new Float32Array(b.memory.buffer, b.mw_pcm_f32(), nb * ch);
    for (let i = 0; i < na * ch; i++) { n16++; if (s[i] !== f2i_vorbis(f[i])) bad++; }
  }
  console.log(`Vorbis: abi ${a.mw_abi()}; ${ch} channels, rate ${a.mw_vorbis_rate()}; ${n16} samples; ${bad} differ between the 16-bit and the float export`); }
console.log(`VP8: abi ${inst("vp8-wasmvm.wasm").mw_abi()}; MP3: abi ${inst("mp3-wasmvm.wasm").mw_abi()}`);
