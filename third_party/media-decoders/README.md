# Media decoder modules

Audio and video decoders compiled to standalone WebAssembly, run by the WebAssembly engine
written in Lean (WasmVM) in factoidal-core's Foafnaut browser. Lean reads the containers (Ogg,
WebM, MP3 frames and tags) and gives a module one packet or frame per call; the module returns
samples or a picture, and Lean checks them.

- Modules: `wasm/` (Opus, Vorbis, VP8, MP3), with `wasm/SHA256SUMS`.
- Where each came from, the licences, the checks made, and how to rebuild: `PROVENANCE.md`.
- Build chain: `build/` (Emscripten 6.0.8 setup, the build script, the entry points).

factoidal-core pins the SHA-256 of each module it loads; a rebuilt module with other bytes is a
change that core must take on purpose.
