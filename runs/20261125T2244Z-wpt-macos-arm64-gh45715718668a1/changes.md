### Since the previous full run: +198 subtests (+0.0087 points)

Previous: `20261125T1959Z-wpt-macos-arm64-gh45690398076a1`, core `41789954b`, 92.6363%. This run: core `acfa63c86`, 92.6450%; 26 commits between.
Tests that lost subtests: 6 (-77); that gained: 47 (+275). Page outcomes: CRASH -1, NO_RESULT -2, STALL +3.

**Directories that fell** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| performance-timeline | 352 | 302 | 244 | -58 |
| page-lifecycle | 23 | 13 | 0 | -13 |
| preload | 956 | 243 | 242 | -1 |
| xhr | 2,344 | 1,833 | 1,832 | -1 |

**Directories that rose** (12; the first 12)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/css-borders | 4,906 | 4,374 | 4,497 | +123 |
| html/semantics | 22,523 | 15,616 | 15,709 | +93 |
| css/selectors | 6,266 | 5,720 | 5,737 | +17 |
| webcodecs | 4,138 | 2,726 | 2,737 | +11 |
| html/dom | 72,476 | 69,929 | 69,936 | +7 |
| css/css-sizing | 6,744 | 5,181 | 5,186 | +5 |
| css/css-cascade | 1,759 | 1,335 | 1,339 | +4 |
| html/interaction | 842 | 338 | 342 | +4 |
| css/css-values | 10,473 | 6,257 | 6,260 | +3 |
| html/infrastructure | 1,664 | 983 | 985 | +2 |
| IndexedDB | 5,853 | 5,503 | 5,504 | +1 |
| dom/nodes | 16,229 | 15,487 | 15,488 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 6 directories, the first 6)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| performance-timeline | 58 | 1 |
| page-lifecycle | 13 | 1 |
| html/semantics | 3 | 1 |
| preload | 1 | 1 |
| third_party/test262 | 1 | 1 |
| xhr | 1 | 1 |

**Tests that lost most** (the first 6 of 6)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /performance-timeline/idlharness.any.html | 58 | 0 | 58 |
| /page-lifecycle/idlharness.html | 13 | 0 | 19 |
| /html/semantics/embedded-content/the-img-element/naturalWidth-naturalHeight-width-height.html | 18 | 15 | 258 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |
| /third_party/test262/test/built-ins/Temporal/PlainYearMonth/prototype/until/calendar-temporal-object.test262.html | 1 | 0 | 1 |
| /xhr/xhr-timeout-longtask.any.html | 1 | 0 | 1 |

**Commits between** (26)

- `bfdf8c654` Foafnaut: new tab page, Settings page repaired, console with level colours and counts (issue 1031)
- `38cd7746b` Foafnaut new tab: one shared document and square corners, measured on the Linux rig (issue 1031)
- `3b09d84d1` fallback_fonts_test: the new tab page may fetch one emoji slice, for its dinosaur (issue 1031)
- `3312ae035` Apply CSS transforms to positioned and block replaced boxes (#1062)
- `a580a2c92` WebRoute: nameAndArgument, with types, for foafnaut:NAME?QUERY (the build of 38cd7746b stopped at WebRoute)
- `37ebba864` Resolve horizontal-grid percentage edges after track sizing (#1052)
- `3f499a901` Use HTML’s element-specific defaults for tabIndex (#1070)
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
- `d2d98b99e` Size replaced aspect ratios in the selected box (#1094)
- `c9a112895` Foafnaut architecture briefing for an outside engineer: design rules, measured state, causes of slowness, where help pays off (issue 1031)
- `cbd84d30e` Read only complete WPT worker records while polling (#1115)
- `dd2a4e2dd` Fix the browser release checks for Particle Rex (#1113)
- `5d4a43662` Round-trip CSS border-radius corner values (#1099)
- `acfa63c86` Supply static image bytes in targeted WPT layout diagnostics (#1116)

