### Since the previous full run: -5 subtests (-0.0002 points)

Previous: `20261123T2247Z-wpt-linux-x86_64-gh45283028419a1`, core `c6ab4a477`, 92.6332%. This run: core `c22de52e6`, 92.6330%; 1 commits between.
Tests that lost subtests: 4 (-5); that gained: 0 (+0). Page outcomes: OK -2, STALL +2.

**Directories that fell** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/dom | 72,439 | 69,928 | 69,926 | -2 |
| IndexedDB | 5,853 | 5,504 | 5,503 | -1 |
| fetch | 13,290 | 8,807 | 8,806 | -1 |
| webcodecs | 3,974 | 2,608 | 2,607 | -1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 4 directories, the first 4)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| html/dom | 2 | 1 |
| IndexedDB | 1 | 1 |
| fetch/metadata | 1 | 1 |
| webcodecs | 1 | 1 |

**Tests that lost most** (the first 4 of 4)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /html/dom/aria-element-reflection-disconnected.html | 2 | 0 | 2 |
| /IndexedDB/interleaved-cursors-large.any.html | 1 | 0 | 1 |
| /fetch/metadata/generated/element-img.https.sub.html | 18 | 17 | 45 |
| /webcodecs/image-decoder.https.any.html | 8 | 7 | 47 |

**Commits between** (1)

- `c22de52e6` Foafnaut: paint table holds two image stores and the SVG redraws (16 MiB); issue 833

