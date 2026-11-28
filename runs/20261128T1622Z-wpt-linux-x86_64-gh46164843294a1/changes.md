### Since the previous full run: +105 subtests (+0.0046 points)

Previous: `20261128T1235Z-wpt-linux-x86_64-gh46145420734a1`, core `bd0d78dd1`, 92.8145%. This run: core `bd0d78dd1`, 92.8191% (the same commit: the difference is flakiness).
Tests that lost subtests: 3 (-12); that gained: 2 (+117). Page outcomes: OK +1, STALL -1.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| referrer-policy | 8,815 | 5,754 | 5,744 | -10 |
| preload | 956 | 243 | 242 | -1 |

**Directories that rose** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| selection/(root) | 33,921 | 33,548 | 33,664 | +116 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 3 directories, the first 3)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| referrer-policy/gen | 10 | 1 |
| preload | 1 | 1 |
| third_party/test262 | 1 | 1 |

**Tests that lost most** (the first 3 of 3)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /referrer-policy/gen/iframe.meta/strict-origin-when-cross-origin/script-tag.http.html | 10 | 0 | 12 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |
| /third_party/test262/test/built-ins/Array/prototype/indexOf/15.4.4.14-9-b-i-14.test262.html | 1 | 0 | 1 |

