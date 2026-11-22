### Since the previous full run: -1,274 subtests (-0.0560 points)

Previous: `20261122T1108Z-wpt-linux-x86_64-gh45012448598a1`, core `9a0e966fb`, 92.6184%. This run: core `e06668509`, 92.5624%; 6 commits between.
Tests that lost subtests: 2 (-1,277); that gained: 3 (+3). Page outcomes: unchanged.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| selection/(root) | 33,918 | 33,664 | 32,388 | -1,276 |
| preload | 956 | 243 | 242 | -1 |

**Directories that rose** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| IndexedDB | 5,853 | 5,503 | 5,504 | +1 |
| fetch | 13,290 | 8,807 | 8,808 | +1 |
| webcodecs | 3,935 | 2,584 | 2,585 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| selection | 1,276 | 1 |
| preload | 1 | 1 |

**Tests that lost most** (the first 2 of 2)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /selection/addRange-32.html | 1,276 | 0 | 1,276 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |

**Commits between** (6)

- `9c4db521e` XML Encryption 1.1: PBKDF2 key derivation in key agreement (track B item 5, part 2)
- `4ca1c7669` Give the full SPARQL proof closure its cold-build budget
- `42b8fb017` Allow the cold SPARQL proof closure to finish (#735)
- `693c83827` Merge pull request #733 from danbri/claude/spec-b-xmlenc-pbkdf2
- `d2d29abfe` Print the required mixed query plan axiom report
- `e06668509` Emit the checked mixed query plan axiom report (#738)

