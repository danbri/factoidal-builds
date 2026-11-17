### Since the previous full run: -48 subtests (-0.0021 points)

Previous: `20261117T1238Z-wpt-linux-x86_64-gh44084977103a1`, core `c91b7d21d`, 92.4656%. This run: core `528b04055`, 92.4634%; 3 commits between.
Tests that lost subtests: 3 (-49); that gained: 1 (+1). Page outcomes: OK -1, STALL +2, TIMEOUT -1.

**Directories that fell** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| resource-timing | 1,207 | 115 | 68 | -47 |
| IndexedDB | 5,853 | 5,504 | 5,503 | -1 |
| webcodecs | 3,922 | 2,572 | 2,571 | -1 |

**Directories that rose** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| xhr | 2,344 | 1,820 | 1,821 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 3 directories, the first 3)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| resource-timing | 47 | 1 |
| IndexedDB | 1 | 1 |
| webcodecs | 1 | 1 |

**Tests that lost most** (the first 3 of 3)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /resource-timing/idlharness.any.worker.html | 47 | 0 | 79 |
| /IndexedDB/interleaved-cursors-large.any.html | 1 | 0 | 1 |
| /webcodecs/image-decoder.https.any.html | 13 | 12 | 47 |

**Commits between** (3)

- `91e9ca396` XML Signature 1.1: 1024-bit RSA keys only after an explicit opt-in (issue 1227)
- `3dfc6a350` Merge pull request #589: XML Signature 1.1, 1024-bit RSA keys only after an explicit opt-in (issue 1227)
- `528b04055` github-coauthor-policy: the MCP comment tools append the footer on create and edit

