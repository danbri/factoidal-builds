### Since the previous full run: +570 subtests (+0.0251 points)

Previous: `20261114T2233Z-wpt-macos-arm64-gh43648723982a1`, core `ff075ad5a`, 91.8122%. This run: core `8c96d3ec8`, 91.8373%; 3 commits between.
Tests that lost subtests: 24 (-220); that gained: 254 (+790). Page outcomes: ERROR +2, NO_RESULT -2, OK +427, STALL +1, TIMEOUT -428.

**Directories that fell** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| xhr | 2,344 | 1,815 | 1,810 | -5 |
| subresource-integrity | 491 | 186 | 184 | -2 |
| content-security-policy | 4,544 | 2,501 | 2,500 | -1 |
| preload | 956 | 47 | 46 | -1 |

**Directories that rose** (10; the first 10)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| streams | 5,796 | 5,160 | 5,381 | +221 |
| referrer-policy | 8,815 | 4,858 | 5,029 | +171 |
| third_party/test262 | 53,833 | 43,245 | 43,374 | +129 |
| websockets | 2,389 | 1,229 | 1,260 | +31 |
| mixed-content | 2,281 | 1,291 | 1,309 | +18 |
| connection-allowlist | 365 | 85 | 89 | +4 |
| shadow-dom | 14,712 | 14,125 | 14,127 | +2 |
| svg/shapes | 18 | 0 | 1 | +1 |
| svg/types | 1,136 | 909 | 910 | +1 |
| webcodecs | 3,922 | 2,573 | 2,574 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 8 directories, the first 8)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| streams/readable-byte-streams | 175 | 4 |
| streams/transform-streams | 14 | 1 |
| third_party/test262 | 12 | 12 |
| streams/readable-streams | 10 | 1 |
| xhr | 5 | 3 |
| subresource-integrity/unencoded-digest | 2 | 1 |
| content-security-policy/connect-src | 1 | 1 |
| preload | 1 | 1 |

**Tests that lost most** (the first 24 of 24)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /streams/readable-byte-streams/general.any.sharedworker.html | 101 | 0 | 101 |
| /streams/readable-byte-streams/templated.any.sharedworker.html | 34 | 0 | 34 |
| /streams/readable-byte-streams/read-min.any.sharedworker.html | 24 | 0 | 24 |
| /streams/readable-byte-streams/construct-byob-request.any.sharedworker.html | 16 | 0 | 16 |
| /streams/transform-streams/backpressure.any.sharedworker.html | 14 | 0 | 14 |
| /streams/readable-streams/reentrant-strategies.any.worker.html | 10 | 0 | 10 |
| /xhr/response-json.htm | 4 | 1 | 4 |
| /subresource-integrity/unencoded-digest/tentative/script.window.html?include=integrity-none | 9 | 7 | 14 |
| /content-security-policy/connect-src/connect-src-websocket-allowed.sub.html | 1 | 0 | 1 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |
| /third_party/test262/test/annexB/built-ins/String/prototype/bold/prop-desc.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/annexB/built-ins/String/prototype/fontcolor/not-a-constructor.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/annexB/built-ins/String/prototype/link/not-a-constructor.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/annexB/built-ins/String/prototype/sub/not-a-constructor.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/annexB/language/eval-code/direct/global-switch-case-eval-global-no-skip-try.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/Array/prototype/forEach/15.4.4.18-7-c-i-27.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/Array/prototype/pop/S15.4.4.6_A4_T1.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/ArrayIteratorPrototype/next/property-descriptor.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/AsyncDisposableStack/prototype/adopt/prop-desc.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/DataView/prototype/buffer/prop-desc.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/DataView/prototype/getFloat32/detached-buffer-before-outofrange-byteoffset.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/Function/internals/Construct/base-ctor-revoked-proxy-realm.test262.html | 1 | 0 | 1 |
| /xhr/xhr-timeout-longtask.any.worker.html | 1 | 0 | 1 |
| /xhr/xmlhttprequest-timeout-worker-aborted.html?aborted immediately after send() | 3 | 2 | 3 |

**Commits between** (3)

- `421f10a45` WebSocket: a socket in its opening handshake keeps the page waiting for the network (Net.Xhr.State.waiting), so settling stops there; before
- `a4a046275` Textnaut 0.1.3: the engine of 0.37.0 (build-ff075ad5af99-foafnaut-web, 11.7 MB); the package carries page-load.mjs inside app/ and rewrites 
- `8c96d3ec8` Hub: a script turn whose animated values changed asks for a layered frame, as the engine's animation clock does; a whole-page frame at the r

