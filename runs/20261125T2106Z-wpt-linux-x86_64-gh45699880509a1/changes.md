### Since the previous full run: +92 subtests (+0.0040 points)

Previous: `20261125T1904Z-wpt-linux-x86_64-gh45680725780a1`, core `3f499a901`, 92.6361%. This run: core `dc102cae4`, 92.6402%; 17 commits between.
Tests that lost subtests: 4 (-46); that gained: 32 (+138). Page outcomes: ERROR -1, OK -1, STALL +2.

**Directories that fell** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/dom | 72,476 | 69,929 | 69,895 | -34 |
| preload | 956 | 243 | 242 | -1 |
| third_party/test262 | 53,838 | 46,343 | 46,342 | -1 |

**Directories that rose** (8; the first 8)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/semantics | 22,523 | 15,616 | 15,709 | +93 |
| css/selectors | 6,266 | 5,720 | 5,737 | +17 |
| webcodecs | 4,138 | 2,725 | 2,737 | +12 |
| html/infrastructure | 1,664 | 983 | 985 | +2 |
| IndexedDB | 5,853 | 5,503 | 5,504 | +1 |
| css/css-values | 10,473 | 6,257 | 6,258 | +1 |
| dom/nodes | 16,229 | 15,487 | 15,488 | +1 |
| fetch | 13,314 | 8,823 | 8,824 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 4 directories, the first 4)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| html/dom | 41 | 1 |
| html/semantics | 3 | 1 |
| preload | 1 | 1 |
| third_party/test262 | 1 | 1 |

**Tests that lost most** (the first 4 of 4)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /html/dom/aria-attribute-reflection.html | 41 | 0 | 41 |
| /html/semantics/embedded-content/the-img-element/naturalWidth-naturalHeight-width-height.html | 18 | 15 | 258 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |
| /third_party/test262/test/built-ins/String/prototype/trim/15.5.4.20-4-50.test262.html | 1 | 0 | 1 |

**Commits between** (17)

- `bfdf8c654` Foafnaut: new tab page, Settings page repaired, console with level colours and counts (issue 1031)
- `38cd7746b` Foafnaut new tab: one shared document and square corners, measured on the Linux rig (issue 1031)
- `3b09d84d1` fallback_fonts_test: the new tab page may fetch one emoji slice, for its dinosaur (issue 1031)
- `a580a2c92` WebRoute: nameAndArgument, with types, for foafnaut:NAME?QUERY (the build of 38cd7746b stopped at WebRoute)
- `bf2aaa40d` Foafnaut pages: Particle Rex, the owner's one-button canvas game, as supplied (issue 1031)
- `f31c9b761` Particle Rex: W, A, S, D and arrow keys mapped to the existing tap; offline Liberation Mono face; manifest entry (issue 1031)
- `02f74e98c` Particle Rex: still sprites from two cached bitmaps per size; original kept as particle-rex-original.html; --page-console json trace (issue 
- `fd71e7778` Canvas 2D prelude: send a batch as binary numbers when one is fractional (issue 1031)
- `5d8afbee0` Foafnaut: particle_rex_test.ts, canvas fraction-batch cost ratchet and expected failures of issues 1074 and 1075 (issue 1031)
- `c67ec6886` Particle Rex: number keys for the cell-texture cache, no number printed per draw (issue 1031)
- `d3cc94ea3` Canvas 2D raster: no decimal parse per pixel; typed arrays: no 2^53 parse per access (issue 1031)
- `7b5f58719` Keep a dropdown's selected value tied to its own options (#1087)
- `660ea09ff` Style: read the style-independent table part of each declaration once per sheet (issue 871)
- `89c167167` WebConsole: long messages wrap (no pre-wrap; line breaks as <br>), counts say 1 error, 2 errors
- `d3150f9ad` Read dimension attributes for unrendered HTML images (#1090)
- `ac8961ffc` Apply :valid and :invalid to controls and their containers (#1081)
- `dc102cae4` Merge remote-tracking branch 'origin/wip/1031-new-tab-page'

