### Since the previous full run: -41 subtests (-0.0018 points)

Previous: `20261126T0933Z-wpt-linux-x86_64-gh45793078070a1`, core `547af47fc`, 92.6645%. This run: core `c434aaa9d`, 92.6627%; 18 commits between.
Tests that lost subtests: 2 (-42); that gained: 1 (+1). Page outcomes: OK -3, STALL +4, TIMEOUT -1.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/dom | 72,476 | 69,936 | 69,895 | -41 |
| third_party/test262 | 53,838 | 46,356 | 46,355 | -1 |

**Directories that rose** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| preload | 956 | 242 | 243 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| html/dom | 41 | 1 |
| third_party/test262 | 1 | 1 |

**Tests that lost most** (the first 2 of 2)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /html/dom/aria-attribute-reflection.html | 41 | 0 | 41 |
| /third_party/test262/test/built-ins/Temporal/PlainTime/prototype/until/largestunit-undefined.test262.html | 1 | 0 | 1 |

**Commits between** (18)

- `48ab38d35` Foafnaut: perf samples cut to trace windows; WebGPU sharing check (issue 1031)
- `ae56565a9` Foafnaut: --engine-mode pooled, a prototype: task sessions served by one or two host workers (issue 1031)
- `ae7ec7e83` zones: map labs/demos/foafnaut/WebSession.lean (engine sessions on Lean tasks) to lab-browser
- `c19bea129` perf_window_report.py: name frames of the engine copies (--engine-mode copies) from the original library
- `17a575910` engine_sessions_report.py: lines for the steady scenarios; only the scenarios in the result (issue 1031)
- `43ead4550` skills/foafnaut: pooled mode, hidden tabs, steady scenarios, perf windows; three traps of 2026-11-26 (issue 1031)
- `80ac0a848` Foafnaut: --warming-spare take|new for task sessions (issue 1031)
- `070e7a849` webgpu_share_check.ts: no claim about the WebGPU specification that was not checked
- `727da3600` engine_sessions_bench.py: steady scenarios run with --idle-checks-only (issue 1031)
- `6b021ac15` Foafnaut: frames of --steps runs carry CPU probes; trap, CLAUDE.md note (issue 1031)
- `8029d7430` engine_sessions_report.py --markdown: a table per steady scenario (issue 1031)
- `361381921` Engine sessions record, section 7 (interim): what was built, per-frame probes, profile of tab B's first frame, WebGPU check (issue 1031)
- `907ac61fa` engine_sessions_bench.py: count spares taken and spares passed over while warming (issue 1031)
- `eca268850` Textnaut 0.1.5: pin the Wasm and native Linux engine of 023a9ce12 (the 0.38.0 release commit)
- `651c1ce6c` Textnaut e2e test: the engine size comes from engine-pin.json, not a fixed 11.7 MB
- `40110e8c6` engine_sessions_test.ts: expected failure, ten library copies in one process on Linux (issue 1160)
- `589ee1d71` Engine sessions record, section 7: steady state with 5, 20 and 50 tabs; the default as a question for the owner (issue 1031)
- `c434aaa9d` skills/foafnaut: tasks mode numbers without per-frame probes; the default is a question for the owner (issue 1031)

