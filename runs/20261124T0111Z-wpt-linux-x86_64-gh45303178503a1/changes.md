### Since the previous full run: -49 subtests (-0.0022 points)

Previous: `20261123T2247Z-wpt-linux-x86_64-gh45283028419a1`, core `c6ab4a477`, 92.6332%. This run: core `c6ab4a477`, 92.6310% (the same commit: the difference is flakiness).
Tests that lost subtests: 3 (-49); that gained: 0 (+0). Page outcomes: OK -1, STALL +2, TIMEOUT -1.

**Directories that fell** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| sanitizer-api | 3,839 | 2,639 | 2,593 | -46 |
| html/dom | 72,439 | 69,928 | 69,926 | -2 |
| IndexedDB | 5,853 | 5,504 | 5,503 | -1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 3 directories, the first 3)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| sanitizer-api | 46 | 1 |
| html/dom | 2 | 1 |
| IndexedDB | 1 | 1 |

**Tests that lost most** (the first 3 of 3)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /sanitizer-api/sanitizer-parseHTML.html | 46 | 0 | 49 |
| /html/dom/aria-element-reflection-disconnected.html | 2 | 0 | 2 |
| /IndexedDB/interleaved-cursors-large.any.html | 1 | 0 | 1 |

