### Since the previous full run: +1,281 subtests (+0.0564 points)

Previous: `20261121T1515Z-wpt-linux-x86_64-gh44918181149a1`, core `3486f29c6`, 92.5619%. This run: core `9dcfb0515`, 92.6183%; 3 commits between.
Tests that lost subtests: 2 (-2); that gained: 4 (+1,283). Page outcomes: CRASH +1, OK +2, STALL -1, TIMEOUT -2.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/semantics | 22,429 | 15,575 | 15,574 | -1 |
| preload | 956 | 243 | 242 | -1 |

**Directories that rose** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| selection/(root) | 33,918 | 32,388 | 33,664 | +1,276 |
| mixed-content | 2,281 | 1,315 | 1,319 | +4 |
| webcodecs | 3,935 | 2,578 | 2,580 | +2 |
| IndexedDB | 5,853 | 5,503 | 5,504 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| html/semantics | 1 | 1 |
| preload | 1 | 1 |

**Tests that lost most** (the first 2 of 2)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /html/semantics/embedded-content/the-img-element/list-of-available-images-does-not-coalesce-in-flight-requests.sub.tentative.html | 1 | 0 | 1 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |

**Commits between** (3)

- `76502cc52` GSSL: test GPU BGP using genuine Lean-generated SBM11 term IDs (#695)
- `342effcbd` GSSL: general-purpose GPU-resident compute sessions, inspection and worklet boundary (#697)
- `9dcfb0515` GSSL 0.1 spec and public exploratory GPU-resident Hub workbench (#703)

