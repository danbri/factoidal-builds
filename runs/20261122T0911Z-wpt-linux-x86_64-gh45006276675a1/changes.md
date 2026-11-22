### Since the previous full run: +1,271 subtests (+0.0559 points)

Previous: `20261122T0846Z-wpt-linux-x86_64-gh45004386368a1`, core `7f3bcf9ab`, 92.5622%. This run: core `d6f7366a3`, 92.6181%; 6 commits between.
Tests that lost subtests: 3 (-6); that gained: 2 (+1,277). Page outcomes: OK -1, STALL -1, TIMEOUT +2.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| referrer-policy | 8,815 | 5,754 | 5,750 | -4 |
| webcodecs | 3,935 | 2,582 | 2,580 | -2 |

**Directories that rose** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| selection/(root) | 33,918 | 32,388 | 33,664 | +1,276 |
| IndexedDB | 5,853 | 5,503 | 5,504 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| referrer-policy/gen | 4 | 2 |
| webcodecs | 2 | 1 |

**Tests that lost most** (the first 3 of 3)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /referrer-policy/gen/top.meta/strict-origin-when-cross-origin/fetch.http.html | 12 | 10 | 12 |
| /referrer-policy/gen/top.meta/unsafe-url/worker-module.http.html | 2 | 0 | 2 |
| /webcodecs/image-decoder.https.any.html | 15 | 13 | 47 |

**Commits between** (6)

- `bc936a32c` Add a local EPUB 3 reading view and pure Lean API (#714)
- `d929fac2a` Build and link the EPUB reader in Foafnaut (#718)
- `7192fb7c3` Record GDSL PVGraph release entry points (#710)
- `57872a9b3` Keep the Foafnaut import audit on the shared root list (#719)
- `59a28a317` Keep EPUB Base64 independent of XML encryption (#728)
- `d6f7366a3` Add a local EPUB 3 reader to the Factoidal Hub (#730)

