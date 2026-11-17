### Since the previous full run: +3,536 subtests (+0.1556 points)

Previous: `20261117T1802Z-wpt-linux-x86_64-gh44142882898a1`, core `489cd1a98`, 92.4773%. This run: core `30355c147`, 92.6329%; 31 commits between.
Tests that lost subtests: 13 (-89); that gained: 244 (+3,625). Page outcomes: CRASH -1, ERROR -47, OK -107, STALL +4, TIMEOUT +151.

**Directories that fell** (5; the first 5)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| compression | 1,316 | 944 | 904 | -40 |
| fetch | 13,288 | 8,824 | 8,807 | -17 |
| html/browsers | 3,309 | 797 | 796 | -1 |
| service-workers | 3,262 | 1,394 | 1,393 | -1 |
| webcodecs | 3,922 | 2,572 | 2,571 | -1 |

**Directories that rose** (56; the first 40)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/geometry | 1,575 | 561 | 1,542 | +981 |
| css/mediaqueries | 1,786 | 1,195 | 1,626 | +431 |
| scroll-animations | 2,167 | 929 | 1,344 | +415 |
| css/css-fonts | 8,740 | 7,507 | 7,850 | +343 |
| html/dom | 72,400 | 69,731 | 69,927 | +196 |
| css/fill-stroke | 409 | 203 | 367 | +164 |
| mathml | 4,321 | 1,413 | 1,575 | +162 |
| html/semantics | 22,381 | 15,479 | 15,572 | +93 |
| css/css-images | 3,628 | 3,516 | 3,599 | +83 |
| css/css-animations | 1,442 | 1,082 | 1,156 | +74 |
| css/css-masking | 6,586 | 6,267 | 6,328 | +61 |
| webvtt | 251 | 8 | 57 | +49 |
| resource-timing | 1,207 | 68 | 115 | +47 |
| webmessaging | 304 | 153 | 196 | +43 |
| html/editing | 868 | 510 | 551 | +41 |
| dom/(root) | 2,768 | 2,440 | 2,480 | +40 |
| css/motion | 4,959 | 4,796 | 4,832 | +36 |
| wasm/jsapi | 2,529 | 2,034 | 2,068 | +34 |
| css/css-shapes | 7,527 | 7,198 | 7,224 | +26 |
| subresource-integrity | 491 | 184 | 209 | +25 |
| css/css-typed-om | 13,449 | 12,139 | 12,161 | +22 |
| FileAPI | 1,645 | 1,205 | 1,226 | +21 |
| css/css-grid | 16,017 | 11,140 | 11,158 | +18 |
| css/css-lists | 974 | 886 | 904 | +18 |
| css/css-transforms | 5,531 | 5,306 | 5,323 | +17 |
| css/css-content | 276 | 253 | 269 | +16 |
| web-animations | 4,256 | 3,936 | 3,952 | +16 |
| xhr | 2,344 | 1,821 | 1,834 | +13 |
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
| dom/nodes | 15,595 | 14,837 | 14,840 | +3 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 8 directories, the first 8)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| compression | 40 | 4 |
| fetch/orb | 28 | 1 |
| subresource-integrity/signatures | 15 | 2 |
| css/css-typed-om | 2 | 2 |
| html/browsers | 1 | 1 |
| html/semantics | 1 | 1 |
| service-workers/service-worker | 1 | 1 |
| webcodecs | 1 | 1 |

**Tests that lost most** (the first 13 of 13)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /fetch/orb/tentative/img-mime-types-coverage.tentative.sub.html | 46 | 18 | 64 |
| /compression/compression-stream.any.html | 10 | 0 | 13 |
| /compression/compression-stream.any.serviceworker.html | 10 | 0 | 13 |
| /compression/compression-stream.any.sharedworker.html | 10 | 0 | 13 |
| /compression/compression-stream.any.worker.html | 10 | 0 | 13 |
| /subresource-integrity/signatures/tentative/csp.window.html | 12 | 2 | 14 |
| /subresource-integrity/signatures/tentative/client-initiated.cross-origin.window.html | 12 | 7 | 14 |
| /css/css-typed-om/the-stylepropertymap/properties/animation-duration.html | 31 | 30 | 32 |
| /css/css-typed-om/the-stylepropertymap/properties/transition-duration.html | 31 | 30 | 31 |
| /html/browsers/origin/origin-keyed-agent-clusters/popups/noopener-opener-no-openee-yes-same.https.html | 1 | 0 | 2 |
| /html/semantics/embedded-content/the-img-element/list-of-available-images-does-not-coalesce-in-flight-requests.sub.tentative.html | 1 | 0 | 1 |
| /service-workers/service-worker/webvtt-cross-origin.https.html | 2 | 1 | 10 |
| /webcodecs/image-decoder.https.any.html | 13 | 12 | 47 |

**Commits between** (31)

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
- `9852da41f` #590 fixes: subgrid keeps empty line name lists; the typed OM reads a value as it was set; branch checks serve the paths scripts fetch
- `deae71855` binary-budget: raise web-render.wasm to the measured size of PR 590 (owner-approved; +3,110 WPT subtests for +0.82%)
- `30355c147` Merge pull request #590 from danbri/wip/wpt-land2

