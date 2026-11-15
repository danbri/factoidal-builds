### Since the previous full run: -5 subtests (-0.0002 points)

Previous: `20261115T1226Z-wpt-macos-arm64-gh43713849019a1`, core `2f3e888e2`, 91.8467%. This run: core `cc73af028`, 91.8464%; 3 commits between.
Tests that lost subtests: 21 (-46); that gained: 7 (+41). Page outcomes: ERROR -2, NO_RESULT +1, OK +2, STALL -3, TIMEOUT +2.

**Directories that fell** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| referrer-policy | 8,815 | 5,005 | 4,981 | -24 |
| webcodecs | 3,922 | 2,578 | 2,573 | -5 |
| xhr | 2,344 | 1,815 | 1,813 | -2 |
| preload | 956 | 243 | 242 | -1 |

**Directories that rose** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/semantics | 22,381 | 15,158 | 15,185 | +27 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 7 directories, the first 7)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| referrer-policy/gen | 31 | 12 |
| webcodecs | 5 | 1 |
| referrer-policy/4K | 4 | 3 |
| referrer-policy/4K-1 | 2 | 1 |
| xhr | 2 | 2 |
| preload | 1 | 1 |
| referrer-policy/4K+1 | 1 | 1 |

**Tests that lost most** (the first 21 of 21)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /referrer-policy/gen/top.http-rp/same-origin/script-tag.http.html | 10 | 4 | 10 |
| /referrer-policy/gen/top.meta/default/xhr.http.html | 12 | 6 | 12 |
| /webcodecs/image-decoder.https.any.html | 19 | 14 | 47 |
| /referrer-policy/gen/top.meta/default/a-tag.http.html | 3 | 0 | 4 |
| /referrer-policy/4K-1/gen/top.meta/origin-when-cross-origin/xhr.http.html | 2 | 0 | 2 |
| /referrer-policy/4K/gen/top.meta/origin-when-cross-origin/fetch.http.html | 2 | 0 | 2 |
| /referrer-policy/gen/srcdoc.meta/origin-when-crossorigin/worker-module.http.html | 2 | 0 | 2 |
| /referrer-policy/gen/srcdoc.meta/origin/worker-module.http.html | 2 | 0 | 2 |
| /referrer-policy/gen/srcdoc.meta/same-origin/worker-module.http.html | 2 | 0 | 2 |
| /referrer-policy/gen/srcdoc.meta/strict-origin-when-cross-origin/worker-module.http.html | 2 | 0 | 2 |
| /referrer-policy/gen/srcdoc.meta/strict-origin/worker-module.http.html | 2 | 0 | 2 |
| /referrer-policy/gen/top.http-rp/no-referrer/svg-a-tag.http.html | 2 | 0 | 4 |
| /referrer-policy/gen/top.meta/no-referrer/svg-a-tag.http.html | 2 | 0 | 4 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |
| /referrer-policy/4K+1/gen/top.http-rp/strict-origin-when-cross-origin/xhr.http.html | 2 | 1 | 2 |
| /referrer-policy/4K/gen/top.http-rp/strict-origin-when-cross-origin/xhr.http.html | 2 | 1 | 2 |
| /referrer-policy/4K/gen/top.meta/unset/xhr.http.html | 2 | 1 | 2 |
| /referrer-policy/gen/srcdoc-inherit.http-rp/origin/worker-module.http.html | 1 | 0 | 2 |
| /referrer-policy/gen/srcdoc.meta/unsafe-url/worker-module.http.html | 1 | 0 | 2 |
| /xhr/access-control-preflight-request-headers-origin.htm | 1 | 0 | 1 |
| /xhr/xhr-timeout-longtask.any.worker.html | 1 | 0 | 1 |

**Commits between** (3)

- `109319318` textnaut 0.1.3: pin the Wasm engine of 2f3e888e2 (build-2f3e888e2d0e-foafnaut-web; the ff075ad5a asset was re-uploaded by a rebuild and no l
- `a00f54025` test.sh: run every check and list all failures at the end (exit 1 if any); --fail-fast stops at the first; per-check times; summary to GITHU
- `cc73af028` showcase_gaps_test: issue 369 is closed (an empty block inside an inline-block is painted: one more primitive), so the test asserts it; test

