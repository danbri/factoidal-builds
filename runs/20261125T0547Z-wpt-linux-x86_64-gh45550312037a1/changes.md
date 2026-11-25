### Since the previous full run: -12 subtests (-0.0005 points)

Previous: `20261125T0451Z-wpt-linux-x86_64-gh45547526181a1`, core `4a0c174b7`, 92.6338%. This run: core `dd387abb3`, 92.6333%; 2 commits between.
Tests that lost subtests: 5 (-14); that gained: 2 (+2). Page outcomes: CRASH +1, ERROR -2, OK -2, STALL +1, TIMEOUT +2.

**Directories that fell** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| mixed-content | 2,281 | 1,319 | 1,311 | -8 |
| webcodecs | 4,168 | 2,640 | 2,637 | -3 |
| service-workers | 3,267 | 1,392 | 1,390 | -2 |
| IndexedDB | 5,853 | 5,504 | 5,503 | -1 |

**Directories that rose** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/semantics | 22,498 | 15,588 | 15,589 | +1 |
| preload | 956 | 242 | 243 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 4 directories, the first 4)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| mixed-content/gen | 8 | 2 |
| webcodecs | 3 | 1 |
| service-workers/service-worker | 2 | 1 |
| IndexedDB | 1 | 1 |

**Tests that lost most** (the first 5 of 5)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /mixed-content/gen/iframe-inherit.http-rp/opt-in/script-tag.https.html | 8 | 4 | 8 |
| /mixed-content/gen/iframe-inherit.meta/unset/worklet-animation-import-data.https.html | 6 | 2 | 8 |
| /webcodecs/image-decoder.https.any.html | 12 | 9 | 47 |
| /service-workers/service-worker/fetch-request-xhr.https.html | 3 | 1 | 13 |
| /IndexedDB/interleaved-cursors-large.any.html | 1 | 0 | 1 |

**Commits between** (2)

- `01edc5a42` Reuse pinned HTTPS connections within each image worker (#1010)
- `dd387abb3` node_query writes: a reflected attribute setter is noted as set_attribute is (issue 871)

