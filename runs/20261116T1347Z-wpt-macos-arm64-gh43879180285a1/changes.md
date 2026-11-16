### Since the previous full run: +311 subtests (+0.0137 points)

Previous: `20261116T0857Z-wpt-macos-arm64-gh43835522545a1`, core `0ccd896a0`, 91.9560%. This run: core `f2e1e546e`, 91.9697%; 1 commits between.
Tests that lost subtests: 36 (-143); that gained: 87 (+454). Page outcomes: ERROR -12, NO_RESULT -10, OK +27, STALL -1, TIMEOUT -4.

**Directories that fell** (5; the first 5)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/semantics | 22,381 | 15,200 | 15,184 | -16 |
| subresource-integrity | 491 | 195 | 184 | -11 |
| media-source | 764 | 24 | 14 | -10 |
| html/syntax | 8,984 | 8,679 | 8,676 | -3 |
| preload | 956 | 243 | 242 | -1 |

**Directories that rose** (8; the first 8)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| streams | 5,796 | 5,313 | 5,580 | +267 |
| third_party/test262 | 53,833 | 45,626 | 45,647 | +21 |
| referrer-policy | 8,815 | 4,911 | 4,931 | +20 |
| websockets | 2,389 | 1,243 | 1,260 | +17 |
| xhr | 2,344 | 1,803 | 1,816 | +13 |
| webcodecs | 3,922 | 2,569 | 2,581 | +12 |
| intersection-observer | 440 | 211 | 212 | +1 |
| workers | 1,598 | 703 | 704 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 10 directories, the first 10)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| referrer-policy/gen | 58 | 16 |
| referrer-policy/4K-1 | 22 | 4 |
| referrer-policy/4K+1 | 20 | 6 |
| html/semantics | 16 | 2 |
| subresource-integrity/unencoded-digest | 11 | 1 |
| media-source | 10 | 1 |
| html/syntax | 3 | 3 |
| preload | 1 | 1 |
| third_party/test262 | 1 | 1 |
| xhr | 1 | 1 |

**Tests that lost most** (the first 36 of 36)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /html/semantics/embedded-content/the-img-element/relevant-mutations.html | 99 | 84 | 113 |
| /referrer-policy/4K-1/gen/top.http-rp/no-referrer-when-downgrade/script-tag.http.html | 12 | 0 | 12 |
| /subresource-integrity/unencoded-digest/tentative/script.window.html?include=integrity-fail | 11 | 0 | 14 |
| /media-source/idlharness.any.html | 10 | 0 | 148 |
| /referrer-policy/4K+1/gen/top.http-rp/no-referrer-when-downgrade/script-tag.http.html | 12 | 6 | 12 |
| /referrer-policy/4K+1/gen/top.http-rp/unsafe-url/script-tag.http.html | 12 | 6 | 12 |
| /referrer-policy/4K-1/gen/top.http-rp/unsafe-url/script-tag.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/top.http-rp/origin-when-cross-origin/fetch.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/top.http-rp/origin/xhr.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/top.meta/always/script-tag.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/top.meta/origin-when-cross-origin/fetch.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/top.meta/origin-when-crossorigin/xhr.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/top.meta/unset/script-tag.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/top.meta/origin-when-crossorigin/a-tag.http.html | 3 | 0 | 4 |
| /referrer-policy/gen/top.meta/strict-origin-when-cross-origin/svg-a-tag.http.html | 3 | 0 | 4 |
| /referrer-policy/4K+1/gen/top.http-rp/strict-origin-when-cross-origin/fetch.http.html | 2 | 0 | 2 |
| /referrer-policy/4K+1/gen/top.meta/origin-when-cross-origin/fetch.http.html | 2 | 0 | 2 |
| /referrer-policy/4K+1/gen/top.meta/same-origin/script-tag.http.html | 2 | 0 | 2 |
| /referrer-policy/4K+1/gen/top.meta/unset/fetch.http.html | 2 | 0 | 2 |
| /referrer-policy/4K-1/gen/top.http-rp/origin-when-cross-origin/worker-module.http.html | 2 | 0 | 2 |
| /referrer-policy/4K-1/gen/top.http-rp/strict-origin-when-cross-origin/fetch.http.html | 2 | 0 | 2 |
| /referrer-policy/gen/iframe.meta/default/a-tag.http.html | 3 | 1 | 4 |
| /referrer-policy/gen/req.attr/no-referrer-when-downgrade/a-tag.http.html | 2 | 0 | 4 |
| /referrer-policy/gen/req.attr/strict-origin-when-cross-origin/iframe-tag.http.html | 2 | 0 | 12 |
| /referrer-policy/gen/req.attr/strict-origin/svg-a-tag.http.html | 2 | 0 | 4 |
| /referrer-policy/gen/top.http-rp/no-referrer/iframe-tag.http.html | 2 | 0 | 12 |
| /referrer-policy/gen/top.http-rp/origin/a-tag.http.html | 2 | 0 | 4 |
| /referrer-policy/gen/top.http-rp/strict-origin/svg-a-tag.http.html | 2 | 0 | 4 |
| /referrer-policy/gen/top.meta/no-referrer/iframe-tag.http.html | 2 | 0 | 12 |
| /html/semantics/embedded-content/the-img-element/list-of-available-images-does-not-coalesce-in-flight-requests.sub.tentative.html | 1 | 0 | 1 |
| /html/syntax/speculative-parsing/generated/page-load/base-in-dsd.tentative.html | 1 | 0 | 1 |
| /html/syntax/speculative-parsing/generated/page-load/math-font-script-src.tentative.html | 1 | 0 | 1 |
| /html/syntax/speculative-parsing/generated/page-load/picture-source-nomatch-media.tentative.html | 1 | 0 | 1 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |
| /third_party/test262/test/built-ins/Object/assign/strings-and-symbol-order-proxy.test262.html | 1 | 0 | 1 |
| /xhr/xhr-timeout-longtask.any.html | 1 | 0 | 1 |

**Commits between** (1)

- `f2e1e546e` Incremental equals full (issue 513 item 2): inventory, statement, culling theorems

