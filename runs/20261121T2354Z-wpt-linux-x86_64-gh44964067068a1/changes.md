### Since the previous full run: -1,397 subtests (-0.0615 points)

Previous: `20261121T2156Z-wpt-linux-x86_64-gh44954108733a1`, core `7f3bcf9ab`, 92.5622%. This run: core `7f3bcf9ab`, 92.5007% (the same commit: the difference is flakiness).
Tests that lost subtests: 2 (-1,399); that gained: 2 (+2). Page outcomes: OK -2, STALL +2.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| quirks | 6,984 | 6,612 | 5,214 | -1,398 |
| fetch | 13,290 | 8,808 | 8,807 | -1 |

**Directories that rose** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| preload | 956 | 242 | 243 | +1 |
| webcodecs | 3,935 | 2,580 | 2,581 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| quirks/unitless-length | 1,398 | 1 |
| fetch/metadata | 1 | 1 |

**Tests that lost most** (the first 2 of 2)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /quirks/unitless-length/quirks.html | 1,398 | 0 | 1,590 |
| /fetch/metadata/generated/element-img.https.sub.html | 19 | 18 | 45 |

