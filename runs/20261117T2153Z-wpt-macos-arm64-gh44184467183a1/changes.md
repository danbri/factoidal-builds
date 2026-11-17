### Since the previous full run: +3,730 subtests (+0.1642 points)

Previous: `20261117T1224Z-wpt-macos-arm64-gh44082763945a1`, core `16bbfba09`, 92.4633%. This run: core `3438c02d9`, 92.6274%; 62 commits between.
Tests that lost subtests: 128 (-190); that gained: 265 (+3,920). Page outcomes: ERROR -45, NO_RESULT -2, OK -173, STALL +5, TIMEOUT +215.

**Directories that fell** (6; the first 6)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| third_party/test262 | 53,833 | 46,246 | 46,139 | -107 |
| compression | 1,316 | 944 | 904 | -40 |
| mixed-content | 2,281 | 1,319 | 1,301 | -18 |
| IndexedDB | 5,853 | 5,504 | 5,503 | -1 |
| html/browsers | 3,309 | 797 | 796 | -1 |
| service-workers | 3,262 | 1,393 | 1,392 | -1 |

**Directories that rose** (56; the first 40)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/geometry | 1,575 | 561 | 1,542 | +981 |
| css/mediaqueries | 1,786 | 1,195 | 1,626 | +431 |
| scroll-animations | 2,167 | 929 | 1,344 | +415 |
| html/semantics | 22,381 | 15,191 | 15,572 | +381 |
| css/css-fonts | 8,740 | 7,507 | 7,850 | +343 |
| html/dom | 72,400 | 69,731 | 69,927 | +196 |
| css/fill-stroke | 409 | 203 | 367 | +164 |
| mathml | 4,321 | 1,414 | 1,576 | +162 |
| css/css-images | 3,628 | 3,516 | 3,599 | +83 |
| css/css-animations | 1,442 | 1,082 | 1,156 | +74 |
| css/css-masking | 6,586 | 6,267 | 6,328 | +61 |
| webvtt | 251 | 8 | 57 | +49 |
| webmessaging | 304 | 153 | 196 | +43 |
| html/editing | 868 | 510 | 551 | +41 |
| dom/(root) | 2,768 | 2,440 | 2,480 | +40 |
| css/motion | 4,959 | 4,796 | 4,832 | +36 |
| wasm/jsapi | 2,529 | 2,034 | 2,068 | +34 |
| streams | 5,796 | 5,547 | 5,580 | +33 |
| html/rendering | 11,705 | 10,054 | 10,083 | +29 |
| css/css-shapes | 7,527 | 7,198 | 7,224 | +26 |
| subresource-integrity | 491 | 184 | 209 | +25 |
| css/css-typed-om | 13,449 | 12,139 | 12,161 | +22 |
| FileAPI | 1,645 | 1,205 | 1,226 | +21 |
| css/css-grid | 16,017 | 11,140 | 11,158 | +18 |
| css/css-lists | 974 | 886 | 904 | +18 |
| css/css-transforms | 5,531 | 5,306 | 5,323 | +17 |
| css/css-content | 276 | 253 | 269 | +16 |
| web-animations | 4,256 | 3,936 | 3,952 | +16 |
| xhr | 2,344 | 1,819 | 1,832 | +13 |
| css/filter-effects | 3,348 | 3,191 | 3,203 | +12 |
| css/css-easing | 167 | 121 | 132 | +11 |
| css/css-cascade | 1,759 | 1,326 | 1,335 | +9 |
| css/css-transitions | 3,439 | 2,707 | 2,715 | +8 |
| svg/types | 1,136 | 912 | 920 | +8 |
| css/css-color-adjust | 171 | 136 | 143 | +7 |
| css/css-backgrounds | 3,429 | 3,261 | 3,267 | +6 |
| svg/painting | 672 | 424 | 430 | +6 |
| css/css-color | 12,760 | 12,355 | 12,360 | +5 |
| html/cross-origin-opener-policy | 658 | 0 | 5 | +5 |
| css/css-values | 10,428 | 6,206 | 6,209 | +3 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 9 directories, the first 9)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| third_party/test262 | 110 | 110 |
| compression | 40 | 4 |
| mixed-content/gen | 18 | 5 |
| subresource-integrity/signatures | 15 | 2 |
| css/css-typed-om | 2 | 2 |
| html/canvas | 2 | 2 |
| IndexedDB | 1 | 1 |
| html/browsers | 1 | 1 |
| service-workers/service-worker | 1 | 1 |

**Tests that lost most** (the first 40 of 128)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /compression/compression-stream.any.html | 10 | 0 | 13 |
| /compression/compression-stream.any.serviceworker.html | 10 | 0 | 13 |
| /compression/compression-stream.any.sharedworker.html | 10 | 0 | 13 |
| /compression/compression-stream.any.worker.html | 10 | 0 | 13 |
| /subresource-integrity/signatures/tentative/csp.window.html | 12 | 2 | 14 |
| /subresource-integrity/signatures/tentative/client-initiated.cross-origin.window.html | 12 | 7 | 14 |
| /mixed-content/gen/iframe-inherit.http-rp/opt-in/sharedworker-import.https.html | 6 | 2 | 8 |
| /mixed-content/gen/iframe-inherit.meta/unset/sharedworker-import.https.html | 6 | 2 | 8 |
| /mixed-content/gen/srcdoc-inherit.http-rp/opt-in/sharedworker-import.https.html | 6 | 2 | 8 |
| /mixed-content/gen/srcdoc-inherit.meta/unset/sharedworker-import.https.html | 6 | 2 | 8 |
| /mixed-content/gen/top.meta/opt-in/sharedworker-import.https.html | 3 | 1 | 5 |
| /IndexedDB/interleaved-cursors-large.any.html | 1 | 0 | 1 |
| /css/css-typed-om/the-stylepropertymap/properties/animation-duration.html | 31 | 30 | 32 |
| /css/css-typed-om/the-stylepropertymap/properties/transition-duration.html | 31 | 30 | 31 |
| /html/browsers/origin/origin-keyed-agent-clusters/popups/noopener-opener-no-openee-yes-same.https.html | 1 | 0 | 2 |
| /html/canvas/offscreen/path-objects/2d.path.arc.negative.worker.html | 1 | 0 | 1 |
| /html/canvas/offscreen/text/2d.text.drawing.style.measure.textAlign.worker.html | 1 | 0 | 1 |
| /service-workers/service-worker/webvtt-cross-origin.https.html | 2 | 1 | 10 |
| /third_party/test262/test/built-ins/Object/S15.2.2.1_A2_T6.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/Object/assign/OnlyOneArgument.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/Object/create/15.2.3.5-4-132.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/Object/create/15.2.3.5-4-155.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/Object/create/15.2.3.5-4-4.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/Object/create/15.2.3.5-4-61.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/Object/create/15.2.3.5-4-84.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/Object/defineProperties/15.2.3.7-5-b-145.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/Object/defineProperties/15.2.3.7-6-a-101.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/Object/defineProperties/15.2.3.7-6-a-156.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/Object/defineProperties/15.2.3.7-6-a-189.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/Object/defineProperties/15.2.3.7-6-a-46.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/Object/defineProperty/15.2.3.6-1.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/Object/defineProperty/15.2.3.6-4-104.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/Object/defineProperty/15.2.3.6-4-115.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/Object/defineProperty/15.2.3.6-4-16.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/Object/defineProperty/15.2.3.6-4-225.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/Object/defineProperty/15.2.3.6-4-236.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/Object/defineProperty/15.2.3.6-4-288.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/Object/defineProperty/15.2.3.6-4-303.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/Object/defineProperty/15.2.3.6-4-354-1.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/Object/defineProperty/15.2.3.6-4-356.test262.html | 1 | 0 | 1 |

**Commits between** (62)

- `8c4c96860` Canonical specified values: transform scaling and skewing, opacity, counters, easing steps, filter amounts, translate, radial gradients
- `742717283` grid, grid-template and track lists: empty line name lists [] left out of the canonical value (CSS Grid 2 7.2)
- `c8c140edf` Canonical values: image-set(), counter lists, font-feature-settings, color-scheme, place-content
- `d6b7ca289` transform canonical form keeps the function names' case
- `9854c1373` animation-range: an end that is its start's default is left out of the canonical value
- `a83348e57` Geometry Interfaces 1: DOMPoint, DOMRect, DOMRectList, DOMQuad, DOMMatrix on Lean's matrices
- `5867965ae` stroke-color (CSS Fill and Stroke 3 §3.2): a colour, inherited, transparent at first; it animates as a colour
- `968b47c23` Merge remote-tracking branch 'origin/main' into wip/wptbulk-canon
- `4a5922c7b` List shorthands read item by item: scroll-timeline, view-timeline, animation-range, timeline-trigger and its ranges
- `1fdb80692` DOM operations throw a TypeError when called with fewer arguments than they require (Web IDL 3.7.6)
- `361bac1c9` Media: text tracks, cues and the track lists (HTML 4.8.11.10-11, 4.8.13)
- `e73473370` DataTransfer, DataTransferItemList, DataTransferItem and FileList; input.files
- `161e36424` BroadcastChannel in the page's realm (HTML 9.5)
- `aef584f91` Animation: shape() arcs interpolate (flags at the ends, either between), path() beside shape() as shape()
- `77df427d0` Frame documents: style elements apply by their type and media, in the frame's viewport
- `0eed8ad49` Animation: a system font keyframe (font: caption) is its longhands, inherited
- `0cfdf0e33` Style: MathML dir, mathcolor, mathbackground and mathsize as presentational hints
- `f70d6c504` Animation shape(): type annotations so shapeOfPath and arcFlag_end elaborate
- `e5ab9084b` gpu_pacing_test: the early-ask rate bound allows for the time the ask really came at (macOS runner timers overshoot: 0.081 > 0.08 failed the
- `c91b7d21d` Merge pull request #587 from danbri/wip/gpu-pacing-flake
- `91e9ca396` XML Signature 1.1: 1024-bit RSA keys only after an explicit opt-in (issue 1227)
- `3dfc6a350` Merge pull request #589: XML Signature 1.1, 1024-bit RSA keys only after an explicit opt-in (issue 1227)
- `528b04055` github-coauthor-policy: the MCP comment tools append the footer on create and edit
- `b336e6830` Merge remote-tracking branch 'origin/wip/wptbulk-geometry' into wip/wpt-land2
- `be521529b` Merge remote-tracking branch 'origin/wip/wptbulk-framemedia' into wip/wpt-land2
- `fa6d58f93` Merge remote-tracking branch 'origin/wip/wpthtml2-tracks' into wip/wpt-land2
- `a9951e30a` Merge remote-tracking branch 'origin/wip/wpthtml2-datatransfer' into wip/wpt-land2
- `bed8e65b4` Merge remote-tracking branch 'origin/wip/wpthtml2-broadcast' into wip/wpt-land2
- `a76cebfe1` Merge remote-tracking branch 'origin/wip/wptbulk-sysfont' into wip/wpt-land2
- `04fb757d3` Merge remote-tracking branch 'origin/wip/wptbulk-arity' into wip/wpt-land2
- `260dc56c4` Merge remote-tracking branch 'origin/wip/wptbulk-mathattr' into wip/wpt-land2
- `cdaa4c615` Merge remote-tracking branch 'origin/wip/wptbulk-shape' into wip/wpt-land2
- `6881c7604` Merge remote-tracking branch 'origin/wip/wptbulk-canon' into wip/wpt-land2
- `cefa638a7` Style: align attributes map to text-align; th centred; bgcolor on row groups; table bordercolor
- `7f43e1fa9` alignHints_other: prove by rewriting the guard
- `a21c49ce9` alignHints_other: simp only, so contains stays a Bool
- `d858d907d` Forms: input value modes and the dirty value flag (HTML 4.10.5)
- `f133de544` Forms: a clone of an input takes its indeterminateness (HTML 4.10.5 cloning steps)
- `eb90b0d8c` Band compile: keep the layout text's head across bands of one layout
- `c03f39658` Scroll: a frame past the band waits for the band being prefetched for the same state
- `d25a50dbc` Grid: do not measure an item whose columns read no contribution
- `4c583484c` Foafnaut everyday use: checklist, host test, error pages, lazy script session, form navigation in the window
- `c9e50a42c` Forms: focus on press, Enter submits, POST plans, the page's own navigation (engine)
- `bf36d240c` SVG: read the round-off numbers of drawing programs and the clip-rule attribute
- `495d6d206` Downloads: the engine decides show or save, a safe name; the window saves to ~/Downloads and keeps the page
- `a39e8c4b8` Images: a new store decodes only the files no kept store decoded
- `50f81a332` SVG: a clipPath whose one path is a rectangle clips as a rect
- `5f3caaae8` SVG: the number guards decide the comparison
- `9852da41f` #590 fixes: subgrid keeps empty line name lists; the typed OM reads a value as it was set; branch checks serve the paths scripts fetch
- `a48c68606` Real sites: page scripts and web fonts run on pages up to 16 MiB of HTML; stylesheets apply up to 8 MiB
- `42aefcb3e` WebDocument page answer: type annotations for the kept-page lambdas (the band-head reuse did not elaborate)
- `19f13304e` Merge pull request #595 from danbri/wip/wptbulk4-align
- `a5f53231e` Merge pull request #597 from danbri/wip/wptbulk4-value
- `5c4e0bb34` Merge pull request #592 from danbri/wip/look-svg
- `8b63244bc` HostContract.ops: the download decision (a query from the response's headers)
- `deae71855` binary-budget: raise web-render.wasm to the measured size of PR 590 (owner-approved; +3,110 WPT subtests for +0.82%)
- `88a39e246` Merge pull request #599 from danbri/wip/coord-limits
- `489cd1a98` Merge pull request #594 from danbri/wip/speed3-scroll
- `43a108824` HostContract: 70 operations with download (count guard; lake build HostContract.Model/Trace green)
- `30355c147` Merge pull request #590 from danbri/wip/wpt-land2
- `06057cf26` Merge remote-tracking branch 'origin/main' into wip/daily-basics
- `3438c02d9` Merge pull request #593 from danbri/wip/daily-basics

