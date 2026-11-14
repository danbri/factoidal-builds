### Since the previous full run: +2,481 subtests (+0.1093 points)

Previous: `20261114T0314Z-wpt-linux-x86_64-gh43550560855a1`, core `19fb349c1`, 83.4415%. This run: core `eccbb6b7f`, 83.5508%; 2 commits between.
Tests that lost subtests: 30 (-44); that gained: 1,035 (+2,525). Page outcomes: CRASH -4, ERROR -19, OK +18, TIMEOUT +5.

**Directories that fell** (7; the first 7)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| mixed-content | 2,281 | 1,120 | 1,112 | -8 |
| content-security-policy | 4,544 | 1,608 | 1,602 | -6 |
| upgrade-insecure-requests | 982 | 241 | 236 | -5 |
| fetch | 13,288 | 4,361 | 4,358 | -3 |
| html/cross-origin-embedder-policy | 596 | 94 | 93 | -1 |
| html/cross-origin-opener-policy | 654 | 1 | 0 | -1 |
| preload | 938 | 47 | 46 | -1 |

**Directories that rose** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| urlpattern | 3,266 | 10 | 1,510 | +1,500 |
| third_party/test262 | 53,833 | 35,339 | 36,342 | +1,003 |
| console | 107 | 28 | 30 | +2 |
| js | 160 | 59 | 60 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 9 directories, the first 9)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| mixed-content/gen | 17 | 12 |
| upgrade-insecure-requests/gen | 8 | 5 |
| content-security-policy/gen | 7 | 2 |
| third_party/test262 | 5 | 5 |
| fetch/metadata | 3 | 2 |
| html/cross-origin-embedder-policy | 1 | 1 |
| html/cross-origin-opener-policy | 1 | 1 |
| mixed-content | 1 | 1 |
| preload | 1 | 1 |

**Tests that lost most** (the first 30 of 30)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /content-security-policy/gen/top.meta/script-src-self/sharedworker-import-data.https.html | 6 | 0 | 12 |
| /mixed-content/gen/top.http-rp/opt-in/link-prefetch-tag.https.html | 6 | 2 | 8 |
| /mixed-content/gen/iframe-inherit.meta/opt-in/xhr.https.html | 5 | 2 | 5 |
| /fetch/metadata/worker.https.sub.html | 2 | 0 | 5 |
| /upgrade-insecure-requests/gen/sharedworker-classic-data.http-rp/upgrade/xhr.https.html | 2 | 0 | 6 |
| /upgrade-insecure-requests/gen/top.meta/upgrade/sharedworker-import-data.https.html | 2 | 0 | 6 |
| /upgrade-insecure-requests/gen/worker-module-data.meta/upgrade/xhr.https.html | 2 | 0 | 6 |
| /content-security-policy/gen/top.http-rp/worker-src-wildcard/script-tag.https.html | 12 | 11 | 12 |
| /fetch/metadata/generated/element-iframe.https.sub.html | 1 | 0 | 20 |
| /html/cross-origin-embedder-policy/credentialless/iframe-coep-credentialless.https.window.html?1-4 | 2 | 1 | 4 |
| /html/cross-origin-opener-policy/reporting/navigation-reporting/reporting-coop-navigated-popup.https.html | 1 | 0 | 2 |
| /mixed-content/csp.https.window.html | 2 | 1 | 3 |
| /mixed-content/gen/iframe-inherit.http-rp/opt-in/worker-import-data.https.html | 7 | 6 | 8 |
| /mixed-content/gen/iframe-inherit.http-rp/opt-in/worker-import.https.html | 5 | 4 | 8 |
| /mixed-content/gen/iframe-inherit.http-rp/opt-in/worklet-animation.https.html | 7 | 6 | 8 |
| /mixed-content/gen/iframe-inherit.http-rp/opt-in/worklet-audio-import-data.https.html | 7 | 6 | 8 |
| /mixed-content/gen/iframe-inherit.http-rp/opt-in/worklet-layout.https.html | 6 | 5 | 8 |
| /mixed-content/gen/iframe-inherit.meta/opt-in/worklet-layout-import-data.https.html | 4 | 3 | 5 |
| /mixed-content/gen/srcdoc-inherit.meta/opt-in/link-prefetch-tag.https.html | 4 | 3 | 5 |
| /mixed-content/gen/srcdoc-inherit.meta/opt-in/xhr.https.html | 5 | 4 | 5 |
| /mixed-content/gen/top.meta/unset/link-prefetch-tag.https.html | 7 | 6 | 8 |
| /mixed-content/gen/worker-module-data.meta/opt-in/websocket.https.html | 2 | 1 | 3 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |
| /third_party/test262/test/built-ins/Object/assign/source-non-enum.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/WeakMap/prototype/getOrInsert/does-not-have-weakmapdata-internal-slot-map.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/WeakMap/prototype/getOrInsertComputed/does-not-have-weakmapdata-internal-slot-map.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/statements/class/static-init-arguments-functions.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/statements/class/static-init-arguments-methods.test262.html | 1 | 0 | 1 |
| /upgrade-insecure-requests/gen/top.http-rp/upgrade/fetch.https.html | 1 | 0 | 6 |
| /upgrade-insecure-requests/gen/top.http-rp/upgrade/worker-import-data.https.html | 1 | 0 | 6 |

**Commits between** (2)

- `3b53b618f` BubblePopJS: early errors of classes and async functions; Symbol.for, String.raw, WeakRef, FinalizationRegistry, getOrInsert; URLPattern in 
- `eccbb6b7f` BubblePopJS: no string past maxStringBytes; repeat by doubling

