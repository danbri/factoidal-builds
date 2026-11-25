### Since the previous full run: -28 subtests (-0.0012 points)

Previous: `20261125T1313Z-wpt-linux-x86_64-gh45621325132a1`, core `e4445d147`, 92.6336%. This run: core `100307076`, 92.6323%; 6 commits between.
Tests that lost subtests: 4 (-71); that gained: 6 (+43). Page outcomes: CRASH -1, OK -2, STALL +3.

**Directories that fell** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| sanitizer-api | 3,839 | 2,639 | 2,576 | -63 |
| webcodecs | 4,168 | 2,644 | 2,638 | -6 |
| html/semantics | 22,498 | 15,588 | 15,587 | -1 |
| preload | 956 | 243 | 242 | -1 |

**Directories that rose** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/css-sizing | 6,743 | 5,139 | 5,181 | +42 |
| css/css-writing-modes | 421 | 231 | 232 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 4 directories, the first 4)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| sanitizer-api | 63 | 1 |
| webcodecs | 6 | 1 |
| html/semantics | 1 | 1 |
| preload | 1 | 1 |

**Tests that lost most** (the first 4 of 4)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /sanitizer-api/sanitizer-processing-instructions.html | 63 | 0 | 63 |
| /webcodecs/image-decoder.https.any.html | 16 | 10 | 47 |
| /html/semantics/embedded-content/the-video-element/intrinsic_sizes.htm | 3 | 2 | 5 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |

**Commits between** (6)

- `34c12a749` Apply height limits to inline-block layout (#1012)
- `cb3a9c76e` Foafnaut: design record on threads, tabs, processes, DNS and HTTP connections
- `9125f2091` Concurrency record: link PR 490, 600, 418, issues 398, 498, Paralliverse and GDSL
- `c397ebd17` Foafnaut: desktop gestures answered at once is a priority (issue 1031)
- `0d4758853` CLAUDE.md: issue 1031 work is metrics driven (owner, 2026-11-25)
- `100307076` CLAUDE.md: owner accepts the JIT mode parameter; LTO default and tier 2 start (issue 471)

