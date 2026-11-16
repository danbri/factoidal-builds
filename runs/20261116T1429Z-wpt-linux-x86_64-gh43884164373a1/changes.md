### Since the previous full run: -13 subtests (-0.0006 points)

Previous: `20261116T0833Z-wpt-linux-x86_64-gh43832195994a1`, core `0ccd896a0`, 91.9745%. This run: core `f2e1e546e`, 91.9739%; 1 commits between.
Tests that lost subtests: 4 (-15); that gained: 2 (+2). Page outcomes: unchanged.

**Directories that fell** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 3,922 | 2,584 | 2,572 | -12 |
| fetch | 13,288 | 8,817 | 8,816 | -1 |
| html/dom | 72,400 | 69,541 | 69,540 | -1 |

**Directories that rose** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| preload | 956 | 242 | 243 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 4 directories, the first 4)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| webcodecs | 12 | 1 |
| fetch/metadata | 1 | 1 |
| html/dom | 1 | 1 |
| html/semantics | 1 | 1 |

**Tests that lost most** (the first 4 of 4)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /webcodecs/image-decoder.https.any.html | 25 | 13 | 47 |
| /fetch/metadata/generated/element-img.https.sub.html | 18 | 17 | 45 |
| /html/dom/documents/dom-tree-accessors/document.scripts.html | 1 | 0 | 1 |
| /html/semantics/embedded-content/the-img-element/list-of-available-images-does-not-coalesce-in-flight-requests.sub.tentative.html | 1 | 0 | 1 |

**Commits between** (1)

- `f2e1e546e` Incremental equals full (issue 513 item 2): inventory, statement, culling theorems

