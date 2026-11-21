### Since the previous full run: +45 subtests (+0.0020 points)

Previous: `20261121T1906Z-wpt-linux-x86_64-gh44939161690a1`, core `9dcfb0515`, 92.6183%. This run: core `fda3bf0a5`, 92.6202%; 1 commits between.
Tests that lost subtests: 2 (-3); that gained: 2 (+48). Page outcomes: CRASH -1, TIMEOUT +1.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 3,935 | 2,580 | 2,578 | -2 |
| IndexedDB | 5,853 | 5,504 | 5,503 | -1 |

**Directories that rose** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| resource-timing | 1,220 | 68 | 115 | +47 |
| preload | 956 | 242 | 243 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| webcodecs | 2 | 1 |
| IndexedDB | 1 | 1 |

**Tests that lost most** (the first 2 of 2)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /webcodecs/image-decoder.https.any.html | 13 | 11 | 47 |
| /IndexedDB/interleaved-cursors-large.any.html | 1 | 0 | 1 |

**Commits between** (1)

- `fda3bf0a5` GDSL 0.2: one typed dataflow graph, JS and S-expression syntax across every domain (#705)

