### Since the previous full run: -9 subtests (-0.0004 points)

Previous: `20261125T0529Z-wpt-macos-arm64-gh45553942472a1`, core `e586b539d`, 92.6341%. This run: core `dd387abb3`, 92.6337%; 3 commits between.
Tests that lost subtests: 5 (-12); that gained: 3 (+3). Page outcomes: CRASH -1, ERROR +1, OK +2, STALL +2, TIMEOUT -4.

**Directories that fell** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| workers | 1,598 | 716 | 708 | -8 |
| webrtc-stats | 338 | 2 | 0 | -2 |
| webcodecs | 4,168 | 2,641 | 2,640 | -1 |

**Directories that rose** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| preload | 956 | 242 | 243 | +1 |
| third_party/test262 | 53,838 | 46,285 | 46,286 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 5 directories, the first 5)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| workers/interfaces | 4 | 1 |
| workers/modules | 4 | 1 |
| webrtc-stats | 2 | 1 |
| third_party/test262 | 1 | 1 |
| webcodecs | 1 | 1 |

**Tests that lost most** (the first 5 of 5)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /workers/interfaces/WorkerGlobalScope/onerror/message-module-DOMException.html | 8 | 4 | 10 |
| /workers/modules/shared-worker-options-credentials.html | 6 | 2 | 33 |
| /webrtc-stats/idlharness.window.html | 2 | 0 | 2 |
| /third_party/test262/test/built-ins/Temporal/PlainDateTime/prototype/toPlainTime/branding.test262.html | 1 | 0 | 1 |
| /webcodecs/image-decoder.https.any.html | 13 | 12 | 47 |

**Commits between** (3)

- `4a0c174b7` Track the renamed CSS variable recursion in the compiled audit (#1007)
- `01edc5a42` Reuse pinned HTTPS connections within each image worker (#1010)
- `dd387abb3` node_query writes: a reflected attribute setter is noted as set_attribute is (issue 871)

