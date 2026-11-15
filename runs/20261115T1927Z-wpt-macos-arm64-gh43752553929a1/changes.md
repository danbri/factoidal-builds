### Since the previous full run: -191 subtests (-0.0084 points)

Previous: `20261115T1831Z-wpt-macos-arm64-gh43747247746a1`, core `5029cc163`, 91.8447%. This run: core `5029cc163`, 91.8363% (the same commit: the difference is flakiness).
Tests that lost subtests: 24 (-284); that gained: 33 (+93). Page outcomes: ERROR +1, NO_RESULT +1, OK -6, STALL +1, TIMEOUT +3.

**Directories that fell** (8; the first 8)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webidl | 838 | 647 | 500 | -147 |
| mathml | 4,321 | 1,089 | 1,049 | -40 |
| user-timing | 862 | 446 | 426 | -20 |
| mixed-content | 2,281 | 1,317 | 1,309 | -8 |
| webgl | 4,279 | 4,258 | 4,252 | -6 |
| referrer-policy | 8,815 | 4,978 | 4,973 | -5 |
| webcodecs | 3,922 | 2,576 | 2,571 | -5 |
| third_party/test262 | 53,833 | 43,375 | 43,374 | -1 |

**Directories that rose** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/semantics | 22,381 | 15,156 | 15,186 | +30 |
| websockets | 2,389 | 1,250 | 1,260 | +10 |
| workers | 1,598 | 702 | 703 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 8 directories, the first 8)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| webidl | 147 | 1 |
| referrer-policy/gen | 56 | 12 |
| mathml/relations | 40 | 1 |
| user-timing | 20 | 1 |
| mixed-content/gen | 8 | 4 |
| webgl | 6 | 1 |
| webcodecs | 5 | 2 |
| third_party/test262 | 2 | 2 |

**Tests that lost most** (the first 24 of 24)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /webidl/idlharness.any.worker.html | 147 | 0 | 159 |
| /mathml/relations/html5-tree/style-src-attr-meta.html?217-last | 40 | 0 | 72 |
| /user-timing/idlharness.any.sharedworker.html | 20 | 0 | 36 |
| /referrer-policy/gen/top.http-rp/origin-when-cross-origin/fetch.http.html | 12 | 0 | 12 |
| /referrer-policy/gen/top.http-rp/origin/xhr.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/top.meta/always/script-tag.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/top.meta/origin-when-cross-origin/fetch.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/top.meta/origin-when-crossorigin/xhr.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/top.meta/unset/script-tag.http.html | 12 | 6 | 12 |
| /webgl/framebuffer-without-color-attachment.html | 6 | 0 | 6 |
| /referrer-policy/gen/top.meta/origin-when-crossorigin/a-tag.http.html | 3 | 0 | 4 |
| /referrer-policy/gen/top.meta/strict-origin-when-cross-origin/svg-a-tag.http.html | 3 | 0 | 4 |
| /webcodecs/video-frame-serialization.any.worker.html | 3 | 0 | 7 |
| /mixed-content/gen/iframe-inherit.meta/opt-in/worker-import.https.html | 5 | 3 | 5 |
| /mixed-content/gen/srcdoc-inherit.meta/opt-in/worker-import.https.html | 5 | 3 | 5 |
| /mixed-content/gen/top.http-rp/opt-in/worker-import.https.html | 8 | 6 | 8 |
| /mixed-content/gen/top.meta/unset/worker-import.https.html | 8 | 6 | 8 |
| /referrer-policy/gen/top.http-rp/no-referrer/iframe-tag.http.html | 2 | 0 | 12 |
| /referrer-policy/gen/top.http-rp/origin/a-tag.http.html | 2 | 0 | 4 |
| /referrer-policy/gen/top.http-rp/strict-origin/svg-a-tag.http.html | 2 | 0 | 4 |
| /referrer-policy/gen/top.meta/no-referrer/iframe-tag.http.html | 2 | 0 | 12 |
| /webcodecs/image-decoder.https.any.html | 17 | 15 | 47 |
| /third_party/test262/test/language/statements/function/dstr/dflt-ary-ptrn-rest-init-id.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/statements/function/dstr/dflt-obj-ptrn-id-init-fn-name-class.test262.html | 1 | 0 | 1 |

