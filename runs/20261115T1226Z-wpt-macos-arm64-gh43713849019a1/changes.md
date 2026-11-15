### Since the previous full run: +633 subtests (+0.0279 points)

Previous: `20261115T1122Z-wpt-macos-arm64-gh43708563060a1`, core `2f3e888e2`, 91.8188%. This run: core `2f3e888e2`, 91.8467% (the same commit: the difference is flakiness).
Tests that lost subtests: 12 (-42); that gained: 32 (+675). Page outcomes: ERROR -7, NO_RESULT -4, OK +13, STALL +1, TIMEOUT -3.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/semantics | 22,381 | 15,177 | 15,158 | -19 |
| referrer-policy | 8,815 | 5,016 | 5,005 | -11 |

**Directories that rose** (13; the first 13)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| wasm/core | 188,396 | 185,226 | 185,597 | +371 |
| webidl | 838 | 500 | 647 | +147 |
| web-animations | 4,256 | 3,901 | 3,934 | +33 |
| xhr | 2,344 | 1,789 | 1,815 | +26 |
| webcodecs | 3,922 | 2,554 | 2,578 | +24 |
| user-timing | 862 | 426 | 446 | +20 |
| wasm/jsapi | 2,529 | 2,023 | 2,034 | +11 |
| wasm/webapi | 1,066 | 1,005 | 1,016 | +11 |
| mixed-content | 2,281 | 1,309 | 1,317 | +8 |
| url | 12,437 | 11,761 | 11,768 | +7 |
| third_party/test262 | 53,833 | 43,373 | 43,375 | +2 |
| websockets | 2,389 | 1,258 | 1,260 | +2 |
| webmessaging | 304 | 152 | 153 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 5 directories, the first 5)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| referrer-policy/gen | 20 | 8 |
| html/semantics | 19 | 1 |
| referrer-policy/4K+1 | 1 | 1 |
| referrer-policy/4K-1 | 1 | 1 |
| xhr | 1 | 1 |

**Tests that lost most** (the first 12 of 12)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /html/semantics/embedded-content/the-img-element/relevant-mutations.html | 95 | 76 | 113 |
| /referrer-policy/gen/top.meta/always/fetch.http.html | 12 | 0 | 12 |
| /referrer-policy/gen/top.http-rp/unset/iframe-tag.http.html | 2 | 0 | 12 |
| /referrer-policy/4K+1/gen/top.meta/unset/xhr.http.html | 2 | 1 | 2 |
| /referrer-policy/4K-1/gen/top.http-rp/strict-origin-when-cross-origin/xhr.http.html | 2 | 1 | 2 |
| /referrer-policy/gen/req.attr/origin-when-cross-origin/script-tag.http.html | 2 | 1 | 12 |
| /referrer-policy/gen/srcdoc-inherit.http-rp/origin/worker-module.http.html | 2 | 1 | 2 |
| /referrer-policy/gen/srcdoc-inherit.meta/default/worker-module.http.html | 2 | 1 | 2 |
| /referrer-policy/gen/srcdoc-inherit.meta/no-referrer-when-downgrade/worker-module.http.html | 2 | 1 | 2 |
| /referrer-policy/gen/srcdoc-inherit.meta/strict-origin-when-cross-origin/worker-module.http.html | 2 | 1 | 2 |
| /referrer-policy/gen/srcdoc.meta/unsafe-url/worker-module.http.html | 2 | 1 | 2 |
| /xhr/xhr-timeout-longtask.any.html | 1 | 0 | 1 |

