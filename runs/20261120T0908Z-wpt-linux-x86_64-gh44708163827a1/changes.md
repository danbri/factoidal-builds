### Since the previous full run: -1,322 subtests (-0.0582 points)

Previous: `20261120T0829Z-wpt-linux-x86_64-gh44702966491a1`, core `d0d956ffe`, 92.6182%. This run: core `d0d956ffe`, 92.5601% (the same commit: the difference is flakiness).
Tests that lost subtests: 4 (-1,324); that gained: 2 (+2). Page outcomes: OK -1, TIMEOUT +1.

**Directories that fell** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| selection/(root) | 33,918 | 33,664 | 32,388 | -1,276 |
| sanitizer-api | 3,834 | 2,635 | 2,589 | -46 |
| third_party/test262 | 53,838 | 46,250 | 46,249 | -1 |
| webcodecs | 3,935 | 2,581 | 2,580 | -1 |

**Directories that rose** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| IndexedDB | 5,853 | 5,503 | 5,504 | +1 |
| preload | 956 | 242 | 243 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 4 directories, the first 4)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| selection | 1,276 | 1 |
| sanitizer-api | 46 | 1 |
| third_party/test262 | 1 | 1 |
| webcodecs | 1 | 1 |

**Tests that lost most** (the first 4 of 4)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /selection/addRange-32.html | 1,276 | 0 | 1,276 |
| /sanitizer-api/sanitizer-parseHTML.html | 46 | 0 | 49 |
| /third_party/test262/test/language/expressions/class/dstr/async-private-gen-meth-static-dflt-ary-ptrn-rest-obj-id.test262.html | 1 | 0 | 1 |
| /webcodecs/image-decoder.https.any.html | 14 | 13 | 47 |

