### Since the previous full run: +945 subtests (+0.0416 points)

Previous: `20261114T0647Z-wpt-linux-x86_64-gh43566439745a1`, core `d799500c7`, 85.0629%. This run: core `d799500c7`, 85.1045% (the same commit: the difference is flakiness).
Tests that lost subtests: 3 (-55); that gained: 1 (+1,000). Page outcomes: CRASH +1, ERROR -1, STALL +1, TIMEOUT -1.

**Directories that fell** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| fetch | 13,288 | 4,486 | 4,445 | -41 |
| geolocation | 134 | 27 | 14 | -13 |
| preload | 938 | 47 | 46 | -1 |

**Directories that rose** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| encoding/legacy-mb-japanese | 447,723 | 446,722 | 447,722 | +1,000 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 3 directories, the first 3)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| fetch/api | 41 | 1 |
| geolocation | 13 | 1 |
| preload | 1 | 1 |

**Tests that lost most** (the first 3 of 3)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /fetch/api/abort/general.any.html | 41 | 0 | 61 |
| /geolocation/idlharness.https.window.html | 13 | 0 | 68 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |

