### Since the previous full run: +25 subtests (+0.0011 points)

Previous: `20261125T2338Z-wpt-linux-x86_64-gh45719673715a1`, core `edbd2752d`, 92.6461%. This run: core `2bf8a0f56`, 92.6471%; 19 commits between.
Tests that lost subtests: 1 (-1); that gained: 18 (+26). Page outcomes: CRASH -1, OK -1, STALL +2.

**Directories that rose** (5; the first 5)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| third_party/test262 | 53,838 | 46,342 | 46,352 | +10 |
| html-aam | 1,016 | 847 | 856 | +9 |
| css/css-sizing | 6,744 | 5,186 | 5,190 | +4 |
| html/semantics | 22,523 | 15,710 | 15,711 | +1 |
| preload | 956 | 242 | 243 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 1 directories, the first 1)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| third_party/test262 | 1 | 1 |

**Tests that lost most** (the first 1 of 1)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /third_party/test262/test/built-ins/Set/prototype/isSupersetOf/require-internal-slot.test262.html | 1 | 0 | 1 |

**Commits between** (19)

- `271805a2e` Restore WebDriver names for native elements without layout boxes
- `b61bd3ad2` Select area elements in the computed-label guards
- `054a5169f` Transfer height constraints to automatic block widths through aspect ratio
- `e42615c4a` Integrate #1106 with the validated browser size allowance
- `229d5d8aa` Package tested block aspect ratios and accessible names together
- `81a26d9d8` Foafnaut concurrency record: Lean's own threads and processes against what we built (2a)
- `ee388710b` Audit of worker, process and Emscripten paths against Lean native concurrency (inventory, no measurement)
- `3ff9222b1` Foafnaut Tor: keep Arti state in a sealed local LWS storage
- `213e2a483` BubblePopJS: String.prototype.normalize (NFC, NFD, NFKC, NFKD) from Unicode.Normalization
- `a5a6b9ac9` CLAUDE.md: Foafnaut is native first; the in-browser build is a curio (owner, 2026-11-25)
- `af32b113c` Honor maxlength for text-control insertion (#1101)
- `1553ce0b5` Foafnaut host: timer turn trace splits each animation frame into engine time, call beyond it, and wait before the next ask (issue 1098)
- `74d4c4f54` Foafnaut: keep the chrome layer and the no-layers answer in the engine state (issue 1124, stage A)
- `c28cc76f1` Canvas 2D: source-over without Px values; canvas store drawn in place (issue 1098)
- `59604442c` Report exact byte margins from the binary budget check (#1132)
- `802cde686` Correct block aspect-ratio sizing and WebDriver labels (#1119)
- `e67e88a0b` Foafnaut: boxes, glyph runs and links as binary sections in a layers answer (issue 1124, stage B)
- `b496fa983` Foafnaut tests: layout sections in the bytes test; spinal probe budget met (issue 1124)
- `2bf8a0f56` Supply Particle Rex's stylesheet to the strict offline demo check (#1133)

