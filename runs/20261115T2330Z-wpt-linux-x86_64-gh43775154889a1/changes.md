### Since the previous full run: -13 subtests (-0.0006 points)

Previous: `20261115T2237Z-wpt-linux-x86_64-gh43770312455a1`, core `9504dce9e`, 91.8550%. This run: core `9504dce9e`, 91.8545% (the same commit: the difference is flakiness).
Tests that lost subtests: 3 (-14); that gained: 1 (+1). Page outcomes: OK +1, STALL -1.

**Directories that fell** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 3,922 | 2,584 | 2,576 | -8 |
| resource-timing | 1,207 | 24 | 19 | -5 |
| service-workers | 3,262 | 1,393 | 1,392 | -1 |

**Directories that rose** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| preload | 956 | 242 | 243 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 3 directories, the first 3)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| webcodecs | 8 | 1 |
| resource-timing | 5 | 1 |
| service-workers/cache-storage | 1 | 1 |

**Tests that lost most** (the first 3 of 3)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /webcodecs/image-decoder.https.any.html | 25 | 17 | 47 |
| /resource-timing/idlharness.any.worker.html | 5 | 0 | 79 |
| /service-workers/cache-storage/cache-abort.https.any.serviceworker.html | 9 | 8 | 9 |

