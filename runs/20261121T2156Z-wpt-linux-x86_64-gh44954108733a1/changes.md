### Since the previous full run: -1,320 subtests (-0.0581 points)

Previous: `20261121T1956Z-wpt-linux-x86_64-gh44943449941a1`, core `fda3bf0a5`, 92.6202%. This run: core `7f3bcf9ab`, 92.5622%; 1 commits between.
Tests that lost subtests: 3 (-1,324); that gained: 3 (+4). Page outcomes: CRASH +1, STALL -1.

**Directories that fell** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| selection/(root) | 33,918 | 33,664 | 32,388 | -1,276 |
| resource-timing | 1,220 | 115 | 68 | -47 |
| preload | 956 | 243 | 242 | -1 |

**Directories that rose** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 3,935 | 2,578 | 2,580 | +2 |
| IndexedDB | 5,853 | 5,503 | 5,504 | +1 |
| fetch | 13,290 | 8,807 | 8,808 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 3 directories, the first 3)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| selection | 1,276 | 1 |
| resource-timing | 47 | 1 |
| preload | 1 | 1 |

**Tests that lost most** (the first 3 of 3)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /selection/addRange-32.html | 1,276 | 0 | 1,276 |
| /resource-timing/idlharness.any.html | 47 | 0 | 79 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |

**Commits between** (1)

- `7f3bcf9ab` PVGraph: require native Lean admission for GPU dataflow execution and verify real JSON semantics (#708)

