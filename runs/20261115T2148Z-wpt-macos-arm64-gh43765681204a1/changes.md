### Since the previous full run: +99 subtests (+0.0044 points)

Previous: `20261115T1927Z-wpt-macos-arm64-gh43752553929a1`, core `5029cc163`, 91.8363%. This run: core `04740693f`, 91.8407%; 32 commits between.
Tests that lost subtests: 66 (-166); that gained: 177 (+265). Page outcomes: ERROR +8, NO_RESULT +8, OK -41, TIMEOUT +25.

**Directories that fell** (6; the first 6)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/semantics | 22,381 | 15,186 | 15,121 | -65 |
| xhr | 2,344 | 1,814 | 1,788 | -26 |
| websockets | 2,389 | 1,260 | 1,249 | -11 |
| webcodecs | 3,922 | 2,571 | 2,561 | -10 |
| webmessaging | 304 | 153 | 147 | -6 |
| workers | 1,598 | 703 | 700 | -3 |

**Directories that rose** (5; the first 5)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| third_party/test262 | 53,833 | 43,374 | 43,491 | +117 |
| referrer-policy | 8,815 | 4,973 | 5,029 | +56 |
| mathml | 4,321 | 1,049 | 1,089 | +40 |
| webgl | 4,279 | 4,252 | 4,258 | +6 |
| preload | 956 | 242 | 243 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 13 directories, the first 13)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| html/semantics | 66 | 2 |
| third_party/test262 | 44 | 44 |
| xhr | 26 | 8 |
| webcodecs | 10 | 2 |
| websockets/interfaces | 5 | 2 |
| websockets | 4 | 1 |
| webmessaging | 3 | 1 |
| webmessaging/message-channels | 3 | 1 |
| websockets/constructor | 1 | 1 |
| websockets/stream | 1 | 1 |
| workers/examples | 1 | 1 |
| workers/interfaces | 1 | 1 |
| workers/semantics | 1 | 1 |

**Tests that lost most** (the first 40 of 66)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /html/semantics/the-button-element/command-and-commandfor/invalid-element-types.html?command=show-modal&half=first | 55 | 0 | 55 |
| /xhr/status-async.htm | 24 | 7 | 27 |
| /html/semantics/embedded-content/the-img-element/relevant-mutations.html | 104 | 93 | 113 |
| /webcodecs/videoFrame-orientation-webgl-i420.window.html | 8 | 0 | 8 |
| /websockets/eventhandlers.any.worker.html?wpt_flags=h2 | 4 | 0 | 4 |
| /websockets/interfaces/WebSocket/constants/003.html?wss | 4 | 0 | 4 |
| /webmessaging/Channel_postMessage_transfer_target_port.any.worker.html | 3 | 0 | 3 |
| /webmessaging/message-channels/historical.any.html | 3 | 0 | 3 |
| /webcodecs/encoded-video-chunk.any.html | 2 | 0 | 3 |
| /xhr/access-control-and-redirects-async.any.html | 7 | 5 | 7 |
| /xhr/send-conditional-cors.htm | 2 | 0 | 2 |
| /third_party/test262/test/built-ins/RegExp/property-escapes/special-property-value-Script_Extensions-Unknown.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/TypedArray/prototype/every/values-are-not-cached.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/TypedArray/prototype/reduce/BigInt/callbackfn-return-does-not-change-instance.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/assignmenttargettype/parenthesized-unaryexpression-void-unaryexpression-0.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/async-function/early-errors-expression-binding-identifier-eval.test262.strict.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/async-function/forbidden-ext/b1/async-func-expr-nameless-forbidden-ext-direct-access-prop-arguments.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/async-function/named-await-as-identifier-reference-escaped.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/async-generator/dstr/ary-ptrn-elem-id-init-fn-name-fn.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/async-generator/dstr/ary-ptrn-elem-id-iter-val.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/async-generator/dstr/dflt-ary-ptrn-rest-ary-elision.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/async-generator/dstr/named-ary-ptrn-elem-ary-empty-init.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/async-generator/dstr/named-ary-ptrn-elem-id-init-skipped.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/async-generator/dstr/named-ary-ptrn-rest-not-final-obj.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/async-generator/dstr/named-dflt-ary-ptrn-elem-id-init-skipped.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/async-generator/dstr/named-dflt-ary-ptrn-rest-id-direct.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/async-generator/dstr/named-dflt-obj-ptrn-id-init-skipped.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/async-generator/named-yield-star-getiter-sync-not-callable-object-throw.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/async-generator/named-yield-star-next-then-non-callable-null-fulfillpromise.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/async-generator/yield-identifier-spread-non-strict.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/async-generator/yield-star-next-call-value-get-abrupt.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/bitwise-xor/S11.10.2_A3_T1.2.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/bitwise-xor/S11.10.2_A3_T2.9.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/class/async-gen-method-static/yield-star-next-not-callable-number-throw.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/class/dstr/async-gen-meth-dflt-ary-ptrn-elem-ary-val-null.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/class/dstr/async-gen-meth-static-dflt-ary-ptrn-elem-id-init-fn-name-gen.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/class/dstr/async-private-gen-meth-static-obj-ptrn-rest-getter.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/class/dstr/gen-meth-dflt-ary-ptrn-elem-obj-prop-id-init.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/class/dstr/meth-dflt-ary-ptrn-rest-not-final-obj.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/class/dstr/private-meth-static-ary-ptrn-elem-ary-elem-init.test262.html | 1 | 0 | 1 |

**Commits between** (32)

- `1ae070e99` Retained compile reuses equal primitives, not only the same objects (issue 450)
- `ef77f50be` Tests of reuse after a relayout; plus-timer in the fast bisect budgets (issue 450)
- `23c7734fa` Merge pull request #469 from danbri/wip/prim-reuse
- `91aba4a0c` Real-page survey: runner, page list and budgets, comparison, and two run_html.ts options
- `1032f2a18` Real-page survey offline: snapshots (snapshot.ts, ZIP with provenance, vendored in factoidal-builds), replay into any host by --preload (rep
- `c95d0bb67` Real-page snapshots hold the built-in engine's own requests: replay.ts record mode (REALPAGES_RECORD), snapshot.ts --engine loads the page o
- `7424c5871` Merge pull request #472 from danbri/wip/realpages-ci
- `15b4152e9` Script turns: rule matchers of the layout reads are data made once (no n² key reads); reads counted at the boundary
- `a81bc2ffa` Merge pull request #466 from danbri/wip/script-turns-pr
- `42c287e74` Inline SVG deep in an HTML document no longer refuses the page
- `839127616` Merge pull request #467 from danbri/wip/svg-depth
- `b2b716fa2` BubblePopJS: RegExp property escapes \p{…} and \P{…} with the u flag
- `4492339c2` Merge pull request #468 from danbri/wip/regex-props
- `e38191c65` Module graphs: modules fetched and parsed by earlier attempts of a start are kept
- `1720a095a` Merge pull request #470 from danbri/wip/module-memo
- `ab8c98056` Real-page snapshots always keep the page itself (the United States article is over the 1.5 MB file cap); offline, a page missing from its sn
- `8ec037f3c` Merge pull request #478 from danbri/wip/realpages-ci-2
- `56dfb14d5` passmap-data.py: WPT Pass Map data from the recorded runs, with Test262
- `d46dd5e5d` Merge pull request #480 from danbri/wip/passmap-data
- `d087a0953` Add the .claude/skills symlink for the realpages-survey skill
- `e01634578` Hub: a Conformance page, Test262 first, then WPT, from data files kept in git
- `1a6dd0ecf` Merge pull request #481 from danbri/wip/hub-conformance
- `e6a544a7d` Per-tile edge lists for a path's fill (issue 450)
- `19ac380c7` Tile edge lists: a margin of a sixteenth of the tile's local rows (was half), Array filter with edgesMeeting_eq to the List form; one refere
- `a8553cdef` Tile edge lists made once per compiled primitive: Primitive.tileListing kept in RetainedItem.listing, tilesOfListings assembles the words; a
- `4162bda37` Tiles and damage by a primitive's paint box: its box cut to its clips' boxes (Primitive.paintBox, ClipRect.screenBox); a zoomed path clipped
- `72dcbb58d` Per-tile stroke piece lists (issue 450, spinal-bisect: strokes on SVG text were 728 of 866 ms GPU a frame)
- `3dae7447e` Window: a heavy frame is drawn in bands of about 16 ms, so input is taken between them (issue 450)
- `580d5119d` spinal_perf.ts: stroke pieces tested per tick (tick.draw.pieces_m)
- `c9286e10d` tilesOfListings: listings as an array taken by index, no List.zip of the primitives and their listings (List.zip of 10,000 primitives overfl
- `39c96de6e` scene-work.mjs: piece lists read only from a scene whose shader has them
- `04740693f` Spinal Tap budgets: draw counts of the tile edge and piece lists and paint boxes (native edges max 700, pieces max 600, pixels a tick 400k);

