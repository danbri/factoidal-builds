### Since the previous full run: -29 subtests (-0.0013 points)

Previous: `20261114T1811Z-wpt-macos-arm64-gh43625172646a1`, core `c3d227a9f`, 91.6571%. This run: core `c3d227a9f`, 91.6558% (the same commit: the difference is flakiness).
Tests that lost subtests: 8 (-36); that gained: 4 (+7). Page outcomes: OK +2, STALL -1, TIMEOUT -1.

**Directories that fell** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/semantics | 22,381 | 15,048 | 15,024 | -24 |
| referrer-policy | 8,815 | 4,581 | 4,571 | -10 |
| third_party/test262 | 53,833 | 42,514 | 42,513 | -1 |

**Directories that rose** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 3,922 | 2,574 | 2,578 | +4 |
| preload | 956 | 46 | 47 | +1 |
| xhr | 2,344 | 1,814 | 1,815 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 4 directories, the first 4)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| html/semantics | 24 | 1 |
| referrer-policy/4K+1 | 6 | 3 |
| referrer-policy/4K-1 | 4 | 2 |
| third_party/test262 | 2 | 2 |

**Tests that lost most** (the first 8 of 8)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /html/semantics/embedded-content/the-img-element/relevant-mutations.html | 96 | 72 | 113 |
| /referrer-policy/4K+1/gen/top.http-rp/strict-origin-when-cross-origin/xhr.http.html | 2 | 0 | 2 |
| /referrer-policy/4K+1/gen/top.meta/origin-when-cross-origin/xhr.http.html | 2 | 0 | 2 |
| /referrer-policy/4K+1/gen/top.meta/unset/xhr.http.html | 2 | 0 | 2 |
| /referrer-policy/4K-1/gen/top.http-rp/strict-origin-when-cross-origin/xhr.http.html | 2 | 0 | 2 |
| /referrer-policy/4K-1/gen/top.meta/origin-when-cross-origin/xhr.http.html | 2 | 0 | 2 |
| /third_party/test262/test/annexB/language/global-code/if-decl-else-decl-b-global-skip-early-err-for-in.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/statements/for-of/head-lhs-cover-non-asnmt-trgt.test262.html | 1 | 0 | 1 |

