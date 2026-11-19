### Since the previous full run: -5 subtests (-0.0002 points)

Previous: `20261119T0927Z-wpt-linux-x86_64-gh44496605306a1`, core `aae1fda3d`, 92.5624%. This run: core `aae1fda3d`, 92.5621% (the same commit: the difference is flakiness).
Tests that lost subtests: 4 (-6); that gained: 1 (+1). Page outcomes: OK -2, STALL +3, TIMEOUT -1.

**Directories that fell** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 3,935 | 2,584 | 2,581 | -3 |
| IndexedDB | 5,853 | 5,504 | 5,503 | -1 |
| fetch | 13,290 | 8,808 | 8,807 | -1 |
| html/semantics | 22,429 | 15,575 | 15,574 | -1 |

**Directories that rose** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| preload | 956 | 242 | 243 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 4 directories, the first 4)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| webcodecs | 3 | 1 |
| IndexedDB | 1 | 1 |
| fetch/metadata | 1 | 1 |
| html/semantics | 1 | 1 |

**Tests that lost most** (the first 4 of 4)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /webcodecs/image-decoder.https.any.html | 17 | 14 | 47 |
| /IndexedDB/interleaved-cursors-large.any.html | 1 | 0 | 1 |
| /fetch/metadata/generated/element-img.https.sub.html | 19 | 18 | 45 |
| /html/semantics/embedded-content/the-img-element/list-of-available-images-does-not-coalesce-in-flight-requests.sub.tentative.html | 1 | 0 | 1 |

