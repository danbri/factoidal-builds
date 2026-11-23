### Since the previous full run: -1,236 subtests (-0.0544 points)

Previous: `20261122T2322Z-wpt-linux-x86_64-gh45079388304a1`, core `7444aac0e`, 92.6469%. This run: core `fafc4c199`, 92.5925%; 4 commits between.
Tests that lost subtests: 8 (-1,299); that gained: 25 (+63). Page outcomes: CRASH -1, STALL +2, TIMEOUT -1.

**Directories that fell** (5; the first 5)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| selection/(root) | 33,918 | 33,664 | 32,388 | -1,276 |
| css/css-position | 1,605 | 1,375 | 1,361 | -14 |
| webcodecs | 3,935 | 2,581 | 2,578 | -3 |
| IndexedDB | 5,853 | 5,504 | 5,503 | -1 |
| fetch | 13,290 | 8,808 | 8,807 | -1 |

**Directories that rose** (8; the first 8)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/css-tables | 951 | 534 | 564 | +30 |
| css/css-anchor-position | 13,670 | 11,463 | 11,476 | +13 |
| css/css-values | 10,451 | 6,231 | 6,237 | +6 |
| css/cssom-view | 2,722 | 1,553 | 1,557 | +4 |
| shadow-dom | 14,724 | 14,130 | 14,133 | +3 |
| css/css-flexbox | 4,933 | 3,889 | 3,890 | +1 |
| css/css-grid | 16,018 | 11,273 | 11,274 | +1 |
| preload | 956 | 242 | 243 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 6 directories, the first 6)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| selection | 1,276 | 1 |
| css/css-position | 15 | 1 |
| css/css-anchor-position | 3 | 3 |
| webcodecs | 3 | 1 |
| IndexedDB | 1 | 1 |
| fetch/metadata | 1 | 1 |

**Tests that lost most** (the first 8 of 8)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /selection/addRange-32.html | 1,276 | 0 | 1,276 |
| /css/css-position/position-absolute-fit-content-auto-margin.html | 45 | 30 | 45 |
| /webcodecs/image-decoder.https.any.html | 14 | 11 | 47 |
| /IndexedDB/interleaved-cursors-large.any.html | 1 | 0 | 1 |
| /css/css-anchor-position/anchor-scroll-position-try-007.html | 1 | 0 | 5 |
| /css/css-anchor-position/anchor-scroll-position-try-008.html | 1 | 0 | 4 |
| /css/css-anchor-position/anchor-scroll-position-try-010.html | 1 | 0 | 4 |
| /fetch/metadata/generated/element-img.https.sub.html | 19 | 18 | 45 |

**Commits between** (4)

- `e9fcb09bd` Resolve CSS anchor edges in the correct writing mode (#786)
- `f7e0a22ff` Position the first raster background layer (#780)
- `4f0af0626` Keep fragment-only CSS background URLs local (#787)
- `fafc4c199` Include separated borders in table geometry (#777)

