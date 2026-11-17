### Since the previous full run: +2,595 subtests (+0.1142 points)

Previous: `20261117T0109Z-wpt-linux-x86_64-gh43991999988a1`, core `094a8d872`, 92.0323%. This run: core `47802c23c`, 92.1465%; 5 commits between.
Tests that lost subtests: 2 (-2); that gained: 29 (+2,597). Page outcomes: ERROR -3, NO_RESULT -1, OK +2, TIMEOUT +2.

**Directories that fell** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| preload | 956 | 243 | 242 | -1 |

**Directories that rose** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| wasm/core | 188,396 | 185,597 | 188,177 | +2,580 |
| referrer-policy | 8,815 | 5,021 | 5,029 | +8 |
| webcodecs | 3,922 | 2,577 | 2,584 | +7 |
| fetch | 13,288 | 8,820 | 8,821 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| preload | 1 | 1 |
| service-workers/cache-storage | 1 | 1 |

**Tests that lost most** (the first 2 of 2)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |
| /service-workers/cache-storage/cache-abort.https.any.serviceworker.html | 9 | 8 | 9 |

**Commits between** (5)

- `762867872` WasmVM: memory64 and table64 (64-bit address types)
- `1217260fb` foafnaut launcher: newest main build by lookup over all release pages; clearer modes (0.37.1)
- `77027f06a` Merge remote-tracking branch 'origin/main' into wip/wptbulk
- `aaf06eacc` Merge pull request #561 from danbri/wip/latestfix
- `47802c23c` Merge pull request #562 from danbri/wip/wptbulk

