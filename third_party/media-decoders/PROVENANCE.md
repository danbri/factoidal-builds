# Media decoder modules: provenance

Owner, 2026-11-26, verbatim: "vendor them into factoidal-builds/ repo third_party/ with provenance
version and license info. Include wasm and build chain." Tracking:
https://github.com/danbri/factoidal-core/issues/1169 (audio in Foafnaut, stage A). Records in
factoidal-core: `docs/designissues/2026-11-08-media-wasmvm.md` (the decoders in WasmVM) and
`docs/designissues/2026-11-26-foafnaut-audio-plan.md` (the audio plan).

## What is here

| Path | What |
|---|---|
| `wasm/*.wasm`, `wasm/SHA256SUMS` | the four modules that Lean's WasmVM runs |
| `build/build-media.sh`, `build/setup-emsdk.sh`, `build/media/*.c` | the build chain: Emscripten setup, the build, the entry points |
| `src/minimp3/` | a copy of minimp3 (no upstream releases exist), checked by SHA-256 in the build |
| `licenses/` | the licence of each library, from its source |
| `tests/` | the checks of the section "Checks" |

## Built

2026-11-26, Linux x86_64 (Ubuntu 24.04 cloud container), Emscripten 6.0.8 (`emcc` commit
`aeb67926e7de656da38bc807d83050af93578758`, emscripten-releases build
`9d70dbe8860ccdd3595f6e6065d94bfb543ae955`), the version factoidal-builds uses in `build.yml`. Flags
and their reasons are in the header of `build/build-media.sh`.

## Sources

| Library | Version | Source | SHA-256 of the file | Licence | Used |
|---|---|---|---|---|---|
| libopus | 1.5.2 | https://downloads.xiph.org/releases/opus/opus-1.5.2.tar.gz | `65c1d2f78b9f2fb20082c38cbe47c951ad5839345876e46941612ee87f9a7ce1` | BSD 3-clause (`licenses/libopus-1.5.2-COPYING`) | the decoder, float build |
| libogg | 1.3.5 | https://downloads.xiph.org/releases/ogg/libogg-1.3.5.tar.gz | `0eb4b4b9420a0f51db142ba3f9c64b333f826532dc0f48c6410ae51f4799b664` | BSD 3-clause (`licenses/libogg-1.3.5-COPYING`) | `bitwise.c`, `framing.c` (for libvorbis) |
| libvorbis | 1.3.7 | https://downloads.xiph.org/releases/vorbis/libvorbis-1.3.7.tar.gz | `0e982409a9c3fc82ee06e08205b1355e5c6aa4c36bca58146ef399621b0ce5ab` | BSD 3-clause (`licenses/libvorbis-1.3.7-COPYING`) | the decoder files |
| libvpx | 1.15.2 | https://storage.googleapis.com/downloads.webmproject.org/releases/webm/libvpx-1.15.2.tar.gz | `79c99e7038c281e63f4540c51c264efd6ab1a8a005a9221d6e1f77109e6f57b5` | BSD 3-clause and Google's patent grant (`licenses/libvpx-1.15.2-LICENSE`, `-PATENTS`) | the VP8 decoder |
| minimp3 | `master` of https://github.com/lieff/minimp3, read 2026-11-26 | `src/minimp3/minimp3.h` | `eb4b44812cfe77a358aa1820462cc877473a8d97206009ebecd18b60a123875a` | CC0-1.0 (`licenses/minimp3-LICENSE`) | the MPEG audio layer I, II and III decoder |

The libvpx release tarball has the same 1,241 files as the tag `v1.15.2` of
https://chromium.googlesource.com/webm/libvpx (`diff -r`, 2026-11-26). The modules of 2026-11-08
were built from the GitHub tag archive (SHA-256
`26fcd3db88045dee380e581862a6ef106f49b74b6396ee95c2993a260b4636aa`), which this container could not
fetch. The other files of `src/minimp3/`: `minimp3_ex.h`
`ec1240ad4f29961ed83a9da160fcb190ce2253b618aaae36dfbd7bab4d5eedcf` (not compiled),
`LICENSE` `6a1ee543e5282cd9061881edf462e6fdab181f328da71fc2c9a6950a80e94d01`.

MP3: the patents on MPEG-1/2 audio layer III ended in 2017. libvpx's `PATENTS` file is Google's
grant for VP8. This is not legal advice.

## Modules

| Module | Bytes | SHA-256 | Imports | Interface |
|---|---|---|---|---|
| `opus-wasmvm.wasm` | 126,600 | `0397d9f0daf0f85034626f7ce7ac44455ded2d92a120cabb303ed433f9e87daa` | `env.emscripten_notify_memory_growth` | 2: `mw_opus_init`, `mw_opus_decode` (int16), `mw_opus_decode_f32` (float), `mw_pcm`, `mw_pcm_f32` |
| `vorbis-wasmvm.wasm` | 152,839 | `fcc4c90eaae4dbf44854a227d891ae7a5ae466c8d5c016c715cfac9296a9d367` | that, and `wasi_snapshot_preview1.proc_exit` | 2: `mw_vorbis_header`, `mw_vorbis_rate`, `mw_vorbis_channels`, `mw_vorbis_decode` (int16, first 2 channels), `mw_vorbis_decode_f32` (float, every channel, 8 at most) |
| `vp8-wasmvm.wasm` | 98,853 | `3a536c007f6e1dd446c74b46cc003860f51e9a59567aa98dd286f82666f9236b` | `env.emscripten_notify_memory_growth` | 2: `mw_vp8_init`, `mw_vp8_decode`, `mw_vp8_width`, `mw_vp8_height`, `mw_vp8_i420`, `mw_vp8_rgba` |
| `mp3-wasmvm.wasm` | 36,337 | `d27a97544d98d70ad1a3625f3d5b3db6a6271dd5ef96dc2a601afbd69f7f0efd` | `env.emscripten_notify_memory_growth` | 2: `mw_mp3_init`, `mw_mp3_decode` (one frame), `mw_mp3_info`, `mw_pcm`, `mw_pcm_f32` |

Every module also exports `mw_abi` (returns 2), `mw_alloc` and `mw_free`. Interface 1 (the modules of
2026-11-08) is interface 2 without `mw_abi` and the float exports; the MP3 module is new.

## Checks (2026-11-26)

1. Same bytes from a second build in another directory: all four SHA-256 equal.
2. `mp3-wasmvm.wasm`, run by Node's V8 (`tests/wasm_ref.mjs`), against minimp3 compiled natively with
   the same defines (`tests/ref.c`, `gcc -O2 -ffp-contract=off`): the floats are bit-identical on
   three clips made for this (CC0): 128 kbit/s CBR, VBR with a Xing header, mono 22.05 kHz MPEG-2.
   Against FFmpeg 6.1.1's MP3 decoder: SNR 124.7 and 122.0 dB, largest difference 1.1e-6.
3. Opus, Vorbis, VP8 in Lean's WasmVM (`lake exe media-bench` in factoidal-core, `main` `225aa179`), on
   the clips of core's `third_party/media`:
   - Opus (`arpeggio.opus`) against FFmpeg with libopus: 99.99% of samples identical, largest
     difference 1 of 32768, SNR 115 dB; 190 million WasmVM instructions, as on 2026-11-08.
   - Vorbis (`arpeggio.ogg`) against FFmpeg's own Vorbis decoder: largest difference 1 of 32768, SNR
     84 dB; 120 million instructions, as on 2026-11-08.
   - VP8 (`testsrc-320x180.webm`): all 48 frames byte-identical to FFmpeg with libvpx.
   - Lean container tests (`media-bench test`): 34 passed, 0 failed.
4. The float exports (`tests/f32check.mjs`): on every sample of `arpeggio.opus` (385,920) and
   `arpeggio.ogg` (354,304), the int16 export equals the float export converted the way the C does
   it (libopus: scale, clamp, round half to even; the Vorbis entry: `clip()`): 0 differ.

Not yet run: the Opus test vectors of RFC 8251 and MP3 compliance streams (their licence is to be
checked).

## Rebuild

```
build/setup-emsdk.sh /tmp/emsdk && source /tmp/emsdk/emsdk_env.sh
build/build-media.sh /tmp/media-work            # writes wasm/ and wasm/SHA256SUMS
git diff --stat wasm/                           # no change expected
```
