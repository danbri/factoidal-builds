### Since the previous full run: +1,397 subtests (+0.0615 points)

Previous: `20261121T2354Z-wpt-linux-x86_64-gh44964067068a1`, core `7f3bcf9ab`, 92.5007%. This run: core `7f3bcf9ab`, 92.5622% (the same commit: the difference is flakiness).
Tests that lost subtests: 2 (-2); that gained: 2 (+1,399). Page outcomes: STALL +1, TIMEOUT -1.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| IndexedDB | 5,853 | 5,504 | 5,503 | -1 |
| preload | 956 | 243 | 242 | -1 |

**Directories that rose** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| quirks | 6,984 | 5,214 | 6,612 | +1,398 |
| webcodecs | 3,935 | 2,581 | 2,582 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| IndexedDB | 1 | 1 |
| preload | 1 | 1 |

**Tests that lost most** (the first 2 of 2)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /IndexedDB/interleaved-cursors-large.any.html | 1 | 0 | 1 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |

