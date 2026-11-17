### Since the previous full run: +5,805 subtests (+0.2555 points)

Previous: `20261117T0550Z-wpt-macos-arm64-gh44026874658a1`, core `fbd899f39`, 92.2078%. This run: core `16bbfba09`, 92.4633%; 74 commits between.
Tests that lost subtests: 26 (-144); that gained: 1,070 (+5,949). Page outcomes: ERROR -51, NO_RESULT +2, OK +40, STALL +3, TIMEOUT +6.

**Directories that fell** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| streams | 5,796 | 5,580 | 5,547 | -33 |
| server-timing | 540 | 15 | 3 | -12 |
| webcodecs | 3,922 | 2,574 | 2,569 | -5 |
| xhr | 2,344 | 1,820 | 1,819 | -1 |

**Directories that rose** (53; the first 40)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/css-values | 10,428 | 4,911 | 6,206 | +1,295 |
| referrer-policy | 8,815 | 4,914 | 5,752 | +838 |
| css/css-anchor-position | 13,670 | 10,894 | 11,449 | +555 |
| third_party/test262 | 53,833 | 45,718 | 46,246 | +528 |
| css/css-text | 5,863 | 3,805 | 4,237 | +432 |
| user-timing | 862 | 446 | 805 | +359 |
| mathml | 4,321 | 1,091 | 1,414 | +323 |
| performance-timeline | 352 | 40 | 302 | +262 |
| navigation-timing | 465 | 36 | 293 | +257 |
| css/css-align | 5,473 | 4,279 | 4,452 | +173 |
| css/cssom | 4,463 | 3,608 | 3,752 | +144 |
| resource-timing | 1,207 | 24 | 115 | +91 |
| css/cssom-view | 2,714 | 1,195 | 1,275 | +80 |
| css/css-viewport | 784 | 645 | 711 | +66 |
| hr-time | 160 | 66 | 130 | +64 |
| css/css-color | 12,760 | 12,303 | 12,355 | +52 |
| svg/interact | 9,295 | 8,808 | 8,858 | +50 |
| html-aam | 891 | 810 | 851 | +41 |
| dpub-aam | 39 | 0 | 39 | +39 |
| html/browsers | 3,309 | 768 | 797 | +29 |
| trusted-types | 3,754 | 2,714 | 2,739 | +25 |
| svg/styling | 421 | 161 | 180 | +19 |
| intersection-observer | 440 | 213 | 231 | +18 |
| svg-aam | 54 | 31 | 48 | +17 |
| wai-aria | 588 | 544 | 557 | +13 |
| accname | 509 | 423 | 432 | +9 |
| svg/coordinate-systems | 74 | 31 | 40 | +9 |
| timing-entrytypes-registry | 12 | 0 | 8 | +8 |
| event-timing | 183 | 52 | 59 | +7 |
| dom/events | 927 | 712 | 718 | +6 |
| css/css-writing-modes | 421 | 218 | 222 | +4 |
| html/dom | 72,400 | 69,727 | 69,731 | +4 |
| html/infrastructure | 1,664 | 979 | 983 | +4 |
| webidl | 838 | 647 | 651 | +4 |
| fetch | 13,288 | 8,811 | 8,814 | +3 |
| graphics-aria | 3 | 0 | 3 | +3 |
| html/interaction | 842 | 335 | 338 | +3 |
| html/semantics | 22,381 | 15,188 | 15,191 | +3 |
| css/css-display | 669 | 623 | 625 | +2 |
| css/css-scroll-anchoring | 98 | 8 | 10 | +2 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 12 directories, the first 12)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| css/css-values | 66 | 4 |
| streams/piping | 33 | 1 |
| server-timing | 12 | 2 |
| mixed-content/gen | 10 | 5 |
| html/semantics | 8 | 4 |
| webcodecs | 5 | 1 |
| css/css-anchor-position | 3 | 3 |
| referrer-policy/4K-1 | 2 | 1 |
| third_party/test262 | 2 | 2 |
| css/css-conditional | 1 | 1 |
| css/css-scroll-snap | 1 | 1 |
| xhr | 1 | 1 |

**Tests that lost most** (the first 26 of 26)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /streams/piping/abort.any.sharedworker.html | 33 | 0 | 33 |
| /css/css-values/calc-size/animation/interpolate-size-max-height-interpolation.html | 234 | 210 | 282 |
| /css/css-values/calc-size/animation/interpolate-size-max-width-interpolation.html | 234 | 210 | 282 |
| /css/css-values/calc-size/animation/interpolate-size-logical-properties-interpolation.html | 54 | 42 | 144 |
| /css/css-values/calc-size/animation/interpolate-size-min-width-interpolation.html | 108 | 102 | 228 |
| /server-timing/idlharness.https.any.html | 7 | 1 | 97 |
| /server-timing/idlharness.https.any.worker.html | 7 | 1 | 97 |
| /webcodecs/image-decoder.https.any.html | 15 | 10 | 47 |
| /html/semantics/embedded-content/the-img-element/sizes/parse-a-sizes-attribute-display-none.html | 179 | 177 | 179 |
| /html/semantics/embedded-content/the-img-element/sizes/parse-a-sizes-attribute-quirks-mode.html | 179 | 177 | 179 |
| /html/semantics/embedded-content/the-img-element/sizes/parse-a-sizes-attribute-standards-mode.html | 179 | 177 | 179 |
| /html/semantics/embedded-content/the-img-element/sizes/parse-a-sizes-attribute-width-1000px.html | 179 | 177 | 179 |
| /mixed-content/gen/iframe-inherit.http-rp/opt-in/worker-import.https.html | 8 | 6 | 8 |
| /mixed-content/gen/iframe-inherit.meta/unset/worker-import.https.html | 8 | 6 | 8 |
| /mixed-content/gen/srcdoc-inherit.http-rp/opt-in/worker-import.https.html | 8 | 6 | 8 |
| /mixed-content/gen/srcdoc-inherit.meta/unset/worker-import.https.html | 8 | 6 | 8 |
| /mixed-content/gen/top.meta/opt-in/worker-import.https.html | 5 | 3 | 5 |
| /referrer-policy/4K-1/gen/top.http-rp/strict-origin-when-cross-origin/xhr.http.html | 2 | 0 | 2 |
| /css/css-anchor-position/anchor-position-inline-002.html | 2 | 1 | 4 |
| /css/css-anchor-position/anchor-position-multicol-001.html | 1 | 0 | 4 |
| /css/css-anchor-position/anchor-scroll-js-expose.html | 1 | 0 | 4 |
| /css/css-conditional/at-supports-named-feature-001.html | 8 | 7 | 9 |
| /css/css-scroll-snap/snap-events/scrollsnapchanging/scrollsnapchanging-on-user-root-scroll.tentative.html | 1 | 0 | 7 |
| /third_party/test262/test/built-ins/Array/prototype/forEach/15.4.4.18-2-7.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/Iterator/prototype/includes/closes-on-match.test262.html | 1 | 0 | 1 |
| /xhr/xhr-timeout-longtask.any.html | 1 | 0 | 1 |

**Commits between** (74)

- `8553647ee` tabIndex and autofocus on SVG and MathML elements (HTMLOrSVGElement)
- `63a775f66` BubblePopJS: Symbols as weak keys (CanBeHeldWeakly) and missing early errors
- `de46fc602` Performance in Web IDL shape; PerformanceObserver; Navigation Timing; User Timing fixes
- `5e654612a` tabIndex default of MathML elements: 0 for a, -1 for the others
- `11589be47` The Xalan XSLT 1.0 corpus as two recorded suites: the XSLT 1.0 engine and the XSLT 4.0 processor on 1.0 stylesheets
- `cf7e6351d` Resolved insets: a calc() of a percentage and a length in px
- `2715b6b1f` CSS Box Alignment: first baseline serialises as baseline
- `7a43c9af4` Named access on the Window: an element of any namespace by its id
- `0f281e880` CSS math: infinity and NaN values (CSS Values 4 10.7.1, 10.9.1, 10.12)
- `196e883f0` XNum theorems: add_comm, nan_absorbs, min_max_nan
- `bd0e31aca` Colour channels: an infinite or NaN calc() is read before numeric
- `fb3465ebe` BubblePopJS: length-tracking typed arrays; %TypedArray% iteration methods on TypedArrayLength
- `b86d3e0eb` calc-size() in the sizing properties (CSS Values 5 section 7.1)
- `5c860485a` Merge branch 'wip/wptbulk-named' into wip/wptbulk-batch1
- `86959babe` Merge branch 'wip/wptbulk-insets' into wip/wptbulk-batch1
- `ff6d16e00` Merge branch 'wip/wptbulk-calcsize' into wip/wptbulk-batch1
- `2f41d01e5` line-break: normal and loose let a small kana start a line (CSS Text 3 section 5.3)
- `16022a968` LineBreakTheorems: name the classes of LineBreakData
- `c83db2605` document.location of a frame's document is its frame's Location
- `9d62f41b2` BubblePopJS: private names are own elements; global eval code has no super or new.target
- `aaad05d6f` Anchor positioning: anchor-name, position-anchor and anchor() insets (CSS Anchor Positioning 1)
- `e7a8007cb` Merge remote-tracking branch 'origin/main' into wip/wptbulk-batch1
- `40f5b1529` position-area: the containing block is an area of the grid around the default anchor
- `65f48df55` position-area: normal self-alignment toward the anchor (CSS Anchor Positioning 1 3.1.3)
- `e495228bf` BubblePopJS: ToNumber of a Number with no call (toNumQ) in the numeric and bit operators, unary -, ~ and typedConv
- `45e929c5d` BubblePopJS: a typed array's element is read by a Number key with no key string
- `5aa1ea62b` BubblePopJS: a typed array's element is written by a Number key with no key string
- `87bef5c0b` BubblePopJS: String.front compiled as one read (Prim/StringFront.lean), not a slice and an Option
- `0d2c0a349` CSSOM View bindings: Screen, MediaQueryList(Event), the window's scroll and screen offsets as attributes, scrollingElement
- `d402cf5f9` Window operations scroll/scrollTo/scrollBy/moveTo/moveBy/resizeTo/resizeBy/matchMedia: enumerable own properties of the global, with their a
- `bcb6345cc` calcSizeOf: the nested bases by a tail-recursive descent, then a fold out (tail-recursion gate)
- `1726caef4` Merge branch 'wip/wptbulk-calcsize' into wip/wptbulk-batch1
- `98bfd6fbd` Merge remote-tracking branch 'origin/main' into wip/wptbulk-batch1
- `d4099cfaf` BubblePopJS regular expressions: a search for a pattern anchored with ^ stops at position 0
- `93f2ac365` A page's start in slices: the first frame does not wait for module scripts and tasks
- `d2250ef3f` Merge remote-tracking branch 'origin/main' into wip/wptbulk-linebreak
- `8448d6ede` Merge remote-tracking branch 'origin/main' into wip/wptbulk-docloc
- `d66d418b5` Merge remote-tracking branch 'origin/main' into wip/wptbulk-anchor
- `31ed8df06` BubblePopJS register machine: a typed array's element is read before the registers are stashed
- `621822a5f` BubblePopJS: one Private Name per class evaluation; switch clauses with let/const in generators and async functions
- `a9b0ad53c` Accessibility tree in the engine, exposed in the macOS window and on the Hub
- `3c741b1d2` Roles and names for the accessibility tests; accessibility properties for the test driver
- `2ebee739c` Merge remote-tracking branch 'origin/main' into wip/qt4-xalan
- `ca08e419c` lean-csimp-reach.py: String.front is a core left side (Prim/StringFront.lean)
- `c2e8c52de` Merge main into wip/hotpath-b
- `61365a905` Merge remote-tracking branch 'origin/main' into wip/t262-clusters
- `63f114e62` BubblePopJS: a private method's name is #x, not its evaluation's key (privDisplay)
- `e6dd87d7f` BubblePopJS: private names resolved on the fastGet miss path only (member read and call)
- `5b0827eed` Merge main into wip/a11y-engine
- `ad2c6a351` Merge wip/a11y-engine (with main) into wip/a11y-wpt
- `aeeb9298d` Live collections and style-element rule lists are kept while the DOM does not change
- `eec46f629` Merge wip/wptbulk-batch1
- `89944438b` Merge wip/wptbulk-linebreak
- `b8adfbd06` Merge wip/wptbulk-docloc
- `54c3073e4` Merge wip/wptbulk-anchor
- `b845c789b` Merge remote-tracking branch 'origin/wip/wptbulk-perf' into wip/wptbulk-land
- `c1168aabb` Merge pull request #585 from danbri/wip/wptbulk-land
- `2e4d84944` Host contract: accessibilityTree is a query operation (69 operations)
- `11ca430bd` Merge pull request #582 from danbri/wip/t262-clusters
- `1215be017` Merge pull request #583 from danbri/wip/bbc-live-lists
- `33992d9e7` Merge pull request #580 from danbri/wip/qt4-xalan
- `c5794fdd2` Merge remote-tracking branch 'origin/main' into hotpath-b
- `11d2f763f` Merge remote-tracking branch 'origin/main' into bbc-start-slices
- `5d92ffb11` Merge remote-tracking branch 'origin/main' into cssomview
- `53cf39d46` Hot paths 2 on main: typed-array fast paths use typedLenOf (length-tracking views); index keys are never private keys (lemma); putV/getV ref
- `a2dffab63` Merge remote-tracking branch 'origin/main' into a11y
- `efd07bd22` Merge pull request #586 from danbri/wip/wptbulk-cssomview
- `db1cda1d2` Merge pull request #573 from danbri/wip/bbc-start-slices
- `68b2a2a1c` Merge pull request #571 from danbri/wip/hotpath-b
- `b5743868e` test.sh: accessibility_tree_test needs the engine (restore its exclusion from the pure tests)
- `bc883e19b` Merge remote-tracking branch 'origin/main' into a11y
- `e360123cb` Merge pull request #577 from danbri/wip/a11y-engine
- `8567870ad` Merge remote-tracking branch 'origin/main' into a11ywpt
- `16bbfba09` Merge pull request #579 from danbri/wip/a11y-wpt

