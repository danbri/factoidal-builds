### Since the previous full run: -1,306 subtests (-0.0575 points)

Previous: `20261116T1417Z-wpt-macos-arm64-gh43884214800a1`, core `ddf6be714`, 91.9668%. This run: core `c5121e3aa`, 91.9093%; 1 commits between.
Tests that lost subtests: 15 (-1,444); that gained: 41 (+138). Page outcomes: ERROR -5, NO_RESULT -6, OK -3, STALL +1, TIMEOUT +13.

**Directories that fell** (6; the first 6)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| selection/(root) | 33,918 | 33,664 | 32,388 | -1,276 |
| webidl | 838 | 647 | 500 | -147 |
| third_party/test262 | 53,833 | 45,718 | 45,710 | -8 |
| shadow-dom | 14,720 | 14,127 | 14,121 | -6 |
| mathml | 4,321 | 1,089 | 1,088 | -1 |
| xhr | 2,344 | 1,817 | 1,816 | -1 |

**Directories that rose** (7; the first 7)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| referrer-policy | 8,815 | 4,856 | 4,911 | +55 |
| intersection-observer | 440 | 161 | 212 | +51 |
| html/semantics | 22,381 | 15,176 | 15,193 | +17 |
| page-visibility | 41 | 23 | 27 | +4 |
| websockets | 2,389 | 1,256 | 1,260 | +4 |
| preload | 956 | 242 | 243 | +1 |
| webcodecs | 3,922 | 2,574 | 2,575 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 8 directories, the first 8)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| selection | 1,276 | 1 |
| webidl | 147 | 1 |
| shadow-dom/leaktests | 8 | 1 |
| third_party/test262 | 8 | 8 |
| referrer-policy/gen | 2 | 1 |
| html/semantics | 1 | 1 |
| mathml/presentation-markup | 1 | 1 |
| xhr | 1 | 1 |

**Tests that lost most** (the first 15 of 15)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /selection/addRange-16.html | 1,276 | 0 | 1,276 |
| /webidl/idlharness.any.worker.html | 147 | 0 | 159 |
| /shadow-dom/leaktests/html-collection.html | 8 | 0 | 9 |
| /referrer-policy/gen/iframe.http-rp/origin/a-tag.http.html | 2 | 0 | 4 |
| /html/semantics/embedded-content/the-iframe-element/sandbox_025.htm | 1 | 0 | 1 |
| /mathml/presentation-markup/mrow/stretch-along-block-axis-001.html | 1 | 0 | 5 |
| /third_party/test262/test/language/statements/class/dstr/async-gen-meth-obj-ptrn-prop-obj-init.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/statements/class/dstr/async-gen-meth-static-obj-ptrn-prop-id-init-skipped.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/statements/class/dstr/async-private-gen-meth-dflt-obj-ptrn-prop-id-trailing-comma.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/statements/class/dstr/async-private-gen-meth-static-dflt-ary-ptrn-elem-id-iter-val-array-prototype.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/statements/class/elements/after-same-line-static-method-rs-static-generator-method-privatename-identifier.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/statements/class/elements/nested-direct-eval-err-contains-newtarget.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/statements/const/dstr/obj-ptrn-prop-id-init.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/statements/while/decl-cls.test262.html | 1 | 0 | 1 |
| /xhr/xhr-timeout-longtask.any.html | 1 | 0 | 1 |

**Commits between** (1)

- `c5121e3aa` BubblePopJS: the built-in dispatchers out of the evaluator's mutual block

