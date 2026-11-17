### Since the previous full run: +5,358 subtests (+0.2358 points)

Previous: `20261117T0348Z-wpt-linux-x86_64-gh44008205217a1`, core `fbd899f39`, 92.2128%. This run: core `33992d9e7`, 92.4486%; 45 commits between.
Tests that lost subtests: 20 (-180); that gained: 974 (+5,538). Page outcomes: CRASH +1, ERROR -37, OK +49, STALL +1, TIMEOUT -14.

**Directories that fell** (5; the first 5)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/syntax | 8,984 | 8,679 | 8,625 | -54 |
| selection/(root) | 33,918 | 33,664 | 33,640 | -24 |
| server-timing | 540 | 15 | 3 | -12 |
| webcodecs | 3,922 | 2,578 | 2,569 | -9 |
| IndexedDB | 5,853 | 5,504 | 5,503 | -1 |

**Directories that rose** (39; the first 39)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/css-values | 10,428 | 4,911 | 6,206 | +1,295 |
| referrer-policy | 8,815 | 5,028 | 5,754 | +726 |
| css/css-anchor-position | 13,670 | 10,894 | 11,449 | +555 |
| third_party/test262 | 53,833 | 45,718 | 46,248 | +530 |
| css/css-text | 5,863 | 3,805 | 4,237 | +432 |
| user-timing | 862 | 446 | 805 | +359 |
| mathml | 4,321 | 1,090 | 1,413 | +323 |
| performance-timeline | 352 | 40 | 302 | +262 |
| navigation-timing | 465 | 36 | 293 | +257 |
| css/css-align | 5,473 | 4,279 | 4,452 | +173 |
| css/cssom | 4,463 | 3,608 | 3,752 | +144 |
| css/css-viewport | 784 | 645 | 711 | +66 |
| hr-time | 160 | 66 | 130 | +64 |
| css/css-color | 12,760 | 12,303 | 12,355 | +52 |
| svg/interact | 9,295 | 8,808 | 8,858 | +50 |
| resource-timing | 1,207 | 19 | 68 | +49 |
| trusted-types | 3,754 | 2,714 | 2,739 | +25 |
| svg/styling | 421 | 161 | 180 | +19 |
| html/browsers | 3,309 | 768 | 779 | +11 |
| mixed-content | 2,281 | 1,309 | 1,319 | +10 |
| svg/coordinate-systems | 74 | 31 | 40 | +9 |
| timing-entrytypes-registry | 12 | 0 | 8 | +8 |
| event-timing | 183 | 52 | 59 | +7 |
| html/dom | 72,400 | 69,727 | 69,731 | +4 |
| html/infrastructure | 1,664 | 979 | 983 | +4 |
| fetch | 13,288 | 8,822 | 8,825 | +3 |
| html/interaction | 842 | 335 | 338 | +3 |
| shadow-dom | 14,720 | 14,126 | 14,129 | +3 |
| dom/events | 927 | 712 | 714 | +2 |
| intersection-observer | 440 | 213 | 215 | +2 |
| svg/types | 1,136 | 910 | 912 | +2 |
| web-animations | 4,256 | 3,934 | 3,936 | +2 |
| client-hints | 205 | 58 | 59 | +1 |
| css/css-flexbox | 4,933 | 3,789 | 3,790 | +1 |
| html/semantics | 22,381 | 15,189 | 15,190 | +1 |
| layout-instability | 118 | 1 | 2 | +1 |
| soft-navigation-heuristics | 126 | 0 | 1 | +1 |
| svg/render | 1 | 0 | 1 | +1 |
| svg/struct | 108 | 50 | 51 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 10 directories, the first 10)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| css/css-values | 66 | 4 |
| html/syntax | 54 | 1 |
| selection | 24 | 1 |
| server-timing | 12 | 2 |
| html/semantics | 9 | 5 |
| webcodecs | 9 | 1 |
| css/css-anchor-position | 3 | 3 |
| IndexedDB | 1 | 1 |
| css/css-conditional | 1 | 1 |
| service-workers/cache-storage | 1 | 1 |

**Tests that lost most** (the first 20 of 20)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /html/syntax/parsing/html5lib_write_single.html?file=tests10 | 54 | 0 | 54 |
| /css/css-values/calc-size/animation/interpolate-size-max-height-interpolation.html | 234 | 210 | 282 |
| /css/css-values/calc-size/animation/interpolate-size-max-width-interpolation.html | 234 | 210 | 282 |
| /selection/onselectstart-on-key-in-contenteditable.html?preventDefault=no | 24 | 0 | 30 |
| /css/css-values/calc-size/animation/interpolate-size-logical-properties-interpolation.html | 54 | 42 | 144 |
| /webcodecs/image-decoder.https.any.html | 19 | 10 | 47 |
| /css/css-values/calc-size/animation/interpolate-size-min-width-interpolation.html | 108 | 102 | 228 |
| /server-timing/idlharness.https.any.html | 7 | 1 | 97 |
| /server-timing/idlharness.https.any.worker.html | 7 | 1 | 97 |
| /html/semantics/embedded-content/the-img-element/sizes/parse-a-sizes-attribute-display-none.html | 179 | 177 | 179 |
| /html/semantics/embedded-content/the-img-element/sizes/parse-a-sizes-attribute-quirks-mode.html | 179 | 177 | 179 |
| /html/semantics/embedded-content/the-img-element/sizes/parse-a-sizes-attribute-standards-mode.html | 179 | 177 | 179 |
| /html/semantics/embedded-content/the-img-element/sizes/parse-a-sizes-attribute-width-1000px.html | 179 | 177 | 179 |
| /IndexedDB/interleaved-cursors-large.any.html | 1 | 0 | 1 |
| /css/css-anchor-position/anchor-position-inline-002.html | 2 | 1 | 4 |
| /css/css-anchor-position/anchor-position-multicol-001.html | 1 | 0 | 4 |
| /css/css-anchor-position/anchor-scroll-js-expose.html | 1 | 0 | 4 |
| /css/css-conditional/at-supports-named-feature-001.html | 8 | 7 | 9 |
| /html/semantics/embedded-content/the-img-element/list-of-available-images-does-not-coalesce-in-flight-requests.sub.tentative.html | 1 | 0 | 1 |
| /service-workers/cache-storage/cache-abort.https.any.serviceworker.html | 9 | 8 | 9 |

**Commits between** (45)

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
- `bcb6345cc` calcSizeOf: the nested bases by a tail-recursive descent, then a fold out (tail-recursion gate)
- `1726caef4` Merge branch 'wip/wptbulk-calcsize' into wip/wptbulk-batch1
- `98bfd6fbd` Merge remote-tracking branch 'origin/main' into wip/wptbulk-batch1
- `d2250ef3f` Merge remote-tracking branch 'origin/main' into wip/wptbulk-linebreak
- `8448d6ede` Merge remote-tracking branch 'origin/main' into wip/wptbulk-docloc
- `d66d418b5` Merge remote-tracking branch 'origin/main' into wip/wptbulk-anchor
- `621822a5f` BubblePopJS: one Private Name per class evaluation; switch clauses with let/const in generators and async functions
- `2ebee739c` Merge remote-tracking branch 'origin/main' into wip/qt4-xalan
- `61365a905` Merge remote-tracking branch 'origin/main' into wip/t262-clusters
- `63f114e62` BubblePopJS: a private method's name is #x, not its evaluation's key (privDisplay)
- `e6dd87d7f` BubblePopJS: private names resolved on the fastGet miss path only (member read and call)
- `aeeb9298d` Live collections and style-element rule lists are kept while the DOM does not change
- `eec46f629` Merge wip/wptbulk-batch1
- `89944438b` Merge wip/wptbulk-linebreak
- `b8adfbd06` Merge wip/wptbulk-docloc
- `54c3073e4` Merge wip/wptbulk-anchor
- `b845c789b` Merge remote-tracking branch 'origin/wip/wptbulk-perf' into wip/wptbulk-land
- `c1168aabb` Merge pull request #585 from danbri/wip/wptbulk-land
- `11ca430bd` Merge pull request #582 from danbri/wip/t262-clusters
- `1215be017` Merge pull request #583 from danbri/wip/bbc-live-lists
- `33992d9e7` Merge pull request #580 from danbri/wip/qt4-xalan

