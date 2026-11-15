### Since the previous full run: -44 subtests (-0.0019 points)

Previous: `20261115T0459Z-wpt-macos-arm64-gh43679059743a1`, core `3bf480d92`, 91.8461%. This run: core `3bf480d92`, 91.8442% (the same commit: the difference is flakiness).
Tests that lost subtests: 10 (-55); that gained: 4 (+11). Page outcomes: ERROR +4, OK -5, STALL -1, TIMEOUT +2.

**Directories that fell** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| streams | 5,796 | 5,580 | 5,534 | -46 |
| xhr | 2,344 | 1,814 | 1,810 | -4 |
| referrer-policy | 8,815 | 5,029 | 5,027 | -2 |
| preload | 956 | 47 | 46 | -1 |

**Directories that rose** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/semantics | 22,381 | 15,154 | 15,159 | +5 |
| webcodecs | 3,922 | 2,572 | 2,576 | +4 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 7 directories, the first 7)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| streams/transform-streams | 20 | 2 |
| streams/readable-byte-streams | 16 | 1 |
| streams/readable-streams | 10 | 1 |
| xhr | 4 | 2 |
| referrer-policy/4K-1 | 2 | 1 |
| third_party/test262 | 2 | 2 |
| preload | 1 | 1 |

**Tests that lost most** (the first 10 of 10)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /streams/readable-byte-streams/construct-byob-request.any.sharedworker.html | 16 | 0 | 16 |
| /streams/transform-streams/backpressure.any.sharedworker.html | 14 | 0 | 14 |
| /streams/readable-streams/reentrant-strategies.any.worker.html | 10 | 0 | 10 |
| /streams/transform-streams/flush.any.sharedworker.html | 6 | 0 | 6 |
| /xhr/response-json.htm | 4 | 1 | 4 |
| /referrer-policy/4K-1/gen/top.meta/unsafe-url/sharedworker-classic.http.html | 2 | 0 | 2 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |
| /third_party/test262/test/built-ins/Proxy/defineProperty/return-boolean-and-define-target.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/statements/function/dstr/obj-init-null.test262.html | 1 | 0 | 1 |
| /xhr/xmlhttprequest-timeout-worker-aborted.html?aborted immediately after send() | 3 | 2 | 3 |

