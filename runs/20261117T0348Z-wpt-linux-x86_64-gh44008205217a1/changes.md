### Since the previous full run: -7 subtests (-0.0003 points)

Previous: `20261117T0243Z-wpt-linux-x86_64-gh44004164035a1`, core `fbd899f39`, 92.2131%. This run: core `fbd899f39`, 92.2128% (the same commit: the difference is flakiness).
Tests that lost subtests: 3 (-9); that gained: 2 (+2). Page outcomes: ERROR +1, OK -1, STALL -1, TIMEOUT +1.

**Directories that fell** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 3,922 | 2,584 | 2,578 | -6 |
| referrer-policy | 8,815 | 5,030 | 5,028 | -2 |
| preload | 956 | 243 | 242 | -1 |

**Directories that rose** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| fetch | 13,288 | 8,821 | 8,822 | +1 |
| html/semantics | 22,381 | 15,188 | 15,189 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 3 directories, the first 3)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| webcodecs | 6 | 1 |
| referrer-policy/gen | 2 | 1 |
| preload | 1 | 1 |

**Tests that lost most** (the first 3 of 3)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /webcodecs/image-decoder.https.any.html | 25 | 19 | 47 |
| /referrer-policy/gen/srcdoc.meta/same-origin/sharedworker-classic.http.html | 2 | 0 | 2 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |

