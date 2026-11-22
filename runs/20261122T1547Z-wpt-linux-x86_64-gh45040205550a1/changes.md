### Since the previous full run: +1,271 subtests (+0.0559 points)

Previous: `20261122T1157Z-wpt-linux-x86_64-gh45019596682a1`, core `e06668509`, 92.5624%. This run: core `2eddda1e1`, 92.6183%; 4 commits between.
Tests that lost subtests: 3 (-6); that gained: 2 (+1,277). Page outcomes: unchanged.

**Directories that fell** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 3,935 | 2,585 | 2,581 | -4 |
| IndexedDB | 5,853 | 5,504 | 5,503 | -1 |
| fetch | 13,290 | 8,808 | 8,807 | -1 |

**Directories that rose** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| selection/(root) | 33,918 | 32,388 | 33,664 | +1,276 |
| preload | 956 | 242 | 243 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 3 directories, the first 3)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| webcodecs | 4 | 1 |
| IndexedDB | 1 | 1 |
| fetch/metadata | 1 | 1 |

**Tests that lost most** (the first 3 of 3)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /webcodecs/image-decoder.https.any.html | 18 | 14 | 47 |
| /IndexedDB/interleaved-cursors-large.any.html | 1 | 0 | 1 |
| /fetch/metadata/generated/element-img.https.sub.html | 19 | 18 | 45 |

**Commits between** (4)

- `6462a41c7` XML Encryption 1.1: xenc11:DerivedKey and octet decryption (track B item 5, part 3)
- `9d435f273` Merge pull request #742 from danbri/claude/spec-b-xmlenc-derivedkey
- `5ad780d0e` Record the causes of Foafnaut's CSS and SVG reftest failures (issue 747)
- `2eddda1e1` Reftest causes record: add the 2026-11-22 CSS reftest score (issue 747)

