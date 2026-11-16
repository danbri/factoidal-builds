### Since the previous full run: +887 subtests (+0.0390 points)

Previous: `20261116T0528Z-wpt-linux-x86_64-gh43810495167a1`, core `1b2fc90d5`, 91.9355%. This run: core `0ccd896a0`, 91.9745%; 46 commits between.
Tests that lost subtests: 19 (-34); that gained: 459 (+921). Page outcomes: OK +4, STALL +2, TIMEOUT -6.

**Directories that fell** (5; the first 5)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/css-position | 1,605 | 1,368 | 1,362 | -6 |
| css/css-page | 159 | 60 | 56 | -4 |
| console | 107 | 30 | 28 | -2 |
| css/cssom-view | 2,714 | 1,197 | 1,195 | -2 |
| css/css-anchor-position | 13,670 | 10,895 | 10,894 | -1 |

**Directories that rose** (18; the first 18)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| third_party/test262 | 53,833 | 45,233 | 45,647 | +414 |
| html/rendering | 11,705 | 8,461 | 8,792 | +331 |
| html/infrastructure | 1,664 | 888 | 918 | +30 |
| css/css-grid | 16,017 | 11,116 | 11,140 | +24 |
| css/css-sizing | 6,743 | 5,060 | 5,080 | +20 |
| webcodecs | 3,922 | 2,571 | 2,584 | +13 |
| css/CSS2 | 2,566 | 2,432 | 2,444 | +12 |
| html/webappapis | 3,674 | 3,021 | 3,033 | +12 |
| IndexedDB | 5,853 | 5,493 | 5,504 | +11 |
| js | 160 | 64 | 72 | +8 |
| resize-observer | 131 | 73 | 81 | +8 |
| css/css-values | 10,428 | 4,905 | 4,910 | +5 |
| fetch | 13,288 | 8,812 | 8,816 | +4 |
| intersection-observer | 440 | 209 | 212 | +3 |
| FileAPI | 1,645 | 1,203 | 1,205 | +2 |
| css/css-contain | 499 | 307 | 309 | +2 |
| trusted-types | 3,754 | 2,712 | 2,714 | +2 |
| css/css-borders | 4,906 | 4,348 | 4,349 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 7 directories, the first 7)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| css/css-position | 18 | 11 |
| css/cssom-view | 6 | 1 |
| css/css-page | 4 | 1 |
| console | 2 | 2 |
| third_party/test262 | 2 | 2 |
| IndexedDB | 1 | 1 |
| css/css-anchor-position | 1 | 1 |

**Tests that lost most** (the first 19 of 19)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /css/cssom-view/offsetTopLeft-inline-offsetParent.html | 13 | 7 | 37 |
| /css/css-page/parsing/size-valid.html | 5 | 1 | 15 |
| /css/css-position/sticky/position-sticky-nested-left.html | 3 | 0 | 5 |
| /css/css-position/sticky/position-sticky-left.html | 2 | 0 | 3 |
| /css/css-position/sticky/position-sticky-nested-right.html | 3 | 1 | 5 |
| /css/css-position/sticky/position-sticky-nested-top.html | 3 | 1 | 5 |
| /css/css-position/sticky/position-sticky-overflow-padding.html | 3 | 1 | 3 |
| /css/css-position/sticky/position-sticky-right.html | 2 | 0 | 3 |
| /IndexedDB/idb-partitioned-coverage.sub.html | 30 | 29 | 31 |
| /console/console-log-large-array.any.html | 1 | 0 | 1 |
| /console/console-log-large-array.any.worker.html | 1 | 0 | 1 |
| /css/css-anchor-position/last-successful-change-try-rule.html | 1 | 0 | 3 |
| /css/css-position/sticky/position-sticky-bottom.html | 2 | 1 | 3 |
| /css/css-position/sticky/position-sticky-nested-bottom.html | 3 | 2 | 5 |
| /css/css-position/sticky/position-sticky-top.html | 2 | 1 | 3 |
| /css/css-position/sticky/position-sticky-transforms-translate.html | 1 | 0 | 3 |
| /css/css-position/sticky/position-sticky-transforms.html | 1 | 0 | 3 |
| /third_party/test262/test/built-ins/Uint8Array/prototype/setFromHex/detached-buffer.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/Uint8Array/prototype/toHex/detached-buffer.test262.html | 1 | 0 | 1 |

**Commits between** (46)

- `6f20dd4fd` BubblePopJS: JSON.stringify replacer and space (SerializeJSONProperty), String.prototype methods writable, includes/startsWith/endsWith refu
- `1b5f7b439` Regex/Base64: no dangling else, bounded whitespace skip
- `3b207d02c` BubblePopJS: a Promise subclass constructor settles its own object (super() runs the Promise constructor's steps on this)
- `58f17c53e` BubblePopJS: Array.prototype and %TypedArray%.prototype toLocaleString, subarray through TypedArraySpeciesCreate; guards
- `46396affe` BubblePopJS: Function.prototype.bind per §20.2.3.2 (target's prototype, own length as a Number), closures' toString in the NativeFunction fo
- `af69a1eae` Tail-recursion allow line: Re.refsOf (pattern nesting)
- `d1453e964` Allow list: resolve the merge of main
- `7d0a2e75a` Layers: a chrome answer whose words equal the drawn one keeps its texture (issue 450)
- `521e8a22c` Hub: a page waiting for its timer is not behind; print pages are not made ahead while a page animates (issue 450)
- `8b895fb46` Scene tiles: stroke pieces by cell, fill edges by row band; tile words by counting; retained items as a step with cost theorems (issue 450)
- `36036dd7b` Window: a page whose scripts animate is idle-checked only after 2 s of quiet (issue 450)
- `a4a93476b` Spinal Tap budgets: edges and pieces by cell and band; Hub draw median 75, max 400, GPU median 60, max 250 ms (measured 25, 115, 18.7, 76.1)
- `289c08a55` BubblePopJS generator machine: yield and await in class heritage and computed keys, and in object literal computed keys
- `55208e2e2` import.source(): a SyntaxError, as GetModuleSource of a Source Text Module Record throws
- `a075d6475` Modules: no new.target, super or undeclared private name at module level (early errors)
- `78f0256d1` Syntax: Member.anyYield (the tail-recursion gate's name pattern for the yield walks)
- `54ff0135f` Design record: BubblePopJS Intl (ECMA-402) plan
- `7ca1fa863` Merge pull request #503 from danbri/wip/spinal25
- `f38c52ebe` Merge main into wip/t262-builtins-2
- `26f1404a9` Merge pull request #504 from danbri/wip/t262-builtins-2
- `2c0110fa0` GPU compute kernels generated by Lean (issue 398): kernel IR, race-freedom and bounds theorems, tile binning, GPU differential test
- `0b0efe6c6` GPU residency model with upload-once and budget theorems; GPU gate sleeps through predicted GPU work (issue 398)
- `a664307b6` Tail-recursion allow list: GpuKernel expression ASTs (constant depth), lastWrite (specification only), Resident fit/total (pending accumulat
- `a8bfe7b40` GPU pacing: read FOAFNAUT_GPU_MS_PER_UNIT without needing env permission; gpu_kernel_diff.ts builds its reference with formal/lean4's toolch
- `f3671edfe` test.sh: copy the engine runtime before gpu_kernel_diff.ts (its real scenes load native_html_engine.ts)
- `acad1f3ae` Spinal Tap budgets: RSS growth after warm-up at most 128 MB (accepted: CI runners measure 15 to 86 MB on branches with and without any host 
- `b3fc02c9e` skills: perceived-performance (evidence, metric catalogue, targets, workflows, gaps)
- `8648b7d5b` CLAUDE.md: list the perceived-performance skill
- `06115c15b` Skills: scope-and-sequencing, i18n-layout-testing, cleanup-and-recovery; AGENTS.md for Codex
- `04a3826fc` Hub: Data and documents conformance page, normalised suite records and mapping
- `a95adfcd9` Merge pull request #512 from danbri/wip/spec-hub
- `fa07af1da` WPT reftests as suites of their own: runner (wptrunner rules), CPU-raster drawing, Hub Rendering section, wpt-runs section 10
- `b7a6543b2` Reftest runner: TestRendered as wptrunner fires it, the engine's skips and script errors per page, passes with skips counted
- `b518c4b54` SVG reftests: CSS Color 4 colours, #id/.class selectors by specificity, event handler attributes read past; cssText keeps width/height (no s
- `ed16062ac` wpt-reftests.py clusters: the tests that do not pass grouped by cause, with Chrome's passes
- `892545043` SVG: geometry properties (cx, cy, r, rx, ry, x, y) from style sheets and style; rx/ry auto take the other radius
- `e4fb75f2e` SVG text: a textPath path attribute is drawn up to its first error, and gives way to href when it has no usable data
- `2de83fcf0` reftest-gpu-check.mjs: the reftest pages on WebGPU (the Hub's layer surface) against the CPU raster the score uses; reftest-render.ts --scen
- `550d743e5` reftest-render.ts: uncaught exceptions of page scripts kept as script errors; REFTEST_DEBUG prints each turn
- `25fa7c871` Reftests: an engine refusal is FAIL with its message; validity counts harness errors only, CRASH/STALL listed as engine defects
- `af6f0d932` wpt-reftests.py compare: newly passing tests by the cause they had before
- `c48f99750` SVG markers (SVG 2 §11.6) lowered to transformed copies of the marker content
- `8a4084201` SVG colours of CSS Color 4: rewritten to hex in the page path (SVGCssColour), not in the SVG reader
- `85a9f5736` LabHygiene imports SVGCssColour (the ratchet sees every lab module)
- `4df56d952` svg_test.ts: rx=auto and a style r now draw (SVG 2 geometry properties), as the reader does since this branch
- `0ccd896a0` Merge pull request #496 from danbri/wip/reftests

