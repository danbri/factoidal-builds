### Since the previous full run: +4 subtests (+0.0002 points)

Previous: `20261118T2312Z-wpt-linux-x86_64-gh44418616340a1`, core `34d08979c`, 92.5975%. This run: core `e3303f6ef`, 92.5977%; 1 commits between.
Tests that lost subtests: 2 (-2); that gained: 5 (+6). Page outcomes: OK +2, STALL -1, TIMEOUT -1.

**Directories that fell** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| preload | 956 | 243 | 242 | -1 |

**Directories that rose** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 3,926 | 2,571 | 2,573 | +2 |
| IndexedDB | 5,853 | 5,503 | 5,504 | +1 |
| html/semantics | 22,416 | 15,575 | 15,576 | +1 |
| service-workers | 3,268 | 1,392 | 1,393 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| preload | 1 | 1 |
| third_party/test262 | 1 | 1 |

**Tests that lost most** (the first 2 of 2)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |
| /third_party/test262/test/built-ins/Array/prototype/indexOf/15.4.4.14-9-4.test262.html | 1 | 0 | 1 |

**Commits between** (1)

- `e3303f6ef` docs: record static verified parallel GPU v0.1 architecture and proof gates (#605)

