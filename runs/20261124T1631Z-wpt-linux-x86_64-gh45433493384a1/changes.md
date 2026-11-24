### Since the previous full run: -3 subtests (-0.0001 points)

Previous: `20261124T1524Z-wpt-linux-x86_64-gh45419800075a1`, core `b5ff72304`, 92.6235%. This run: core `8088106e8`, 92.6234%; 3 commits between.
Tests that lost subtests: 2 (-7); that gained: 1 (+4). Page outcomes: CRASH +1, OK -1, STALL -1, TIMEOUT +1.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| referrer-policy | 8,815 | 5,754 | 5,748 | -6 |
| IndexedDB | 5,853 | 5,504 | 5,503 | -1 |

**Directories that rose** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 4,168 | 2,638 | 2,642 | +4 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| referrer-policy/4K+1 | 6 | 1 |
| IndexedDB | 1 | 1 |

**Tests that lost most** (the first 2 of 2)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /referrer-policy/4K+1/gen/top.http-rp/unsafe-url/fetch.http.html | 12 | 6 | 12 |
| /IndexedDB/interleaved-cursors-large.any.html | 1 | 0 | 1 |

**Commits between** (3)

- `f43b16f15` Match snapshot HTML to the Chrome reference on request (#903)
- `44f71d2e6` Record the measured web-render binary sizes (#906)
- `8088106e8` Reuse one picture map for the background style pass (#904)

