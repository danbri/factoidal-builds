### Since the previous full run: +109 subtests (+0.0048 points)

Previous: `20261124T1631Z-wpt-linux-x86_64-gh45433493384a1`, core `8088106e8`, 92.6234%. This run: core `074a3e51f`, 92.6282%; 9 commits between.
Tests that lost subtests: 3 (-6); that gained: 18 (+115). Page outcomes: OK +2, STALL -1, TIMEOUT -1.

**Directories that fell** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 4,168 | 2,642 | 2,638 | -4 |
| preload | 956 | 243 | 242 | -1 |
| resize-observer | 135 | 82 | 81 | -1 |

**Directories that rose** (11; the first 11)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/css-anchor-position | 13,670 | 11,476 | 11,544 | +68 |
| html/rendering | 11,722 | 10,094 | 10,118 | +24 |
| referrer-policy | 8,815 | 5,748 | 5,754 | +6 |
| css/css-fonts | 8,740 | 7,852 | 7,857 | +5 |
| css/css-overflow | 1,215 | 787 | 791 | +4 |
| css/css-flexbox | 4,933 | 3,891 | 3,893 | +2 |
| css/cssom-view | 2,722 | 1,558 | 1,560 | +2 |
| IndexedDB | 5,853 | 5,503 | 5,504 | +1 |
| css/css-tables | 979 | 579 | 580 | +1 |
| css/css-transforms | 5,531 | 5,323 | 5,324 | +1 |
| html/semantics | 22,498 | 15,585 | 15,586 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 3 directories, the first 3)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| webcodecs | 4 | 1 |
| preload | 1 | 1 |
| resize-observer | 1 | 1 |

**Tests that lost most** (the first 3 of 3)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /webcodecs/image-decoder.https.any.html | 14 | 10 | 47 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |
| /resize-observer/notify.html | 11 | 10 | 15 |

**Commits between** (9)

- `99222ad9b` Resolve viewport-unit margins and padding at layout time (#900)
- `c9c5d3cf6` Clear generated CSS counter recursion from the release path (#912)
- `46261abfe` Prioritize pending scroll input during page rendering (#911)
- `388cf8d08` Keep out-of-flow anchors out of block height (#913)
- `980583359` Apply legacy HTML font size and colour hints (#910)
- `86b72bb6c` Add reusable SPARQL parsing, Wikidata rewriting and Hub result views (#917)
- `0ac58b427` Prepare Factoidal Core 0.37.3 release metadata
- `63f74e538` Add the bounded WebP container and VP8L prefix readers (#914)
- `074a3e51f` Preserve inline SVG carrying category and icon metadata (#907)

