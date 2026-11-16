### Since the previous full run: +615 subtests (+0.0271 points)

Previous: `20261116T1721Z-wpt-linux-x86_64-gh43906227066a1`, core `cc857117d`, 92.0036%. This run: core `8a22b20a3`, 92.0306%; 36 commits between.
Tests that lost subtests: 6 (-7); that gained: 72 (+622). Page outcomes: OK +1, STALL -1.

**Directories that fell** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/css-overflow | 1,215 | 728 | 726 | -2 |
| css/css-conditional | 3,298 | 2,239 | 2,238 | -1 |
| html/semantics | 22,381 | 15,176 | 15,175 | -1 |
| preload | 956 | 243 | 242 | -1 |

**Directories that rose** (10; the first 10)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/css-text | 5,863 | 3,297 | 3,805 | +508 |
| sanitizer-api | 3,816 | 2,562 | 2,625 | +63 |
| css/css-multicol | 1,625 | 1,406 | 1,424 | +18 |
| html/canvas | 6,251 | 3,675 | 3,686 | +11 |
| webcodecs | 3,922 | 2,576 | 2,584 | +8 |
| css/css-break | 787 | 585 | 590 | +5 |
| css/css-flexbox | 4,933 | 3,786 | 3,789 | +3 |
| mathml | 4,321 | 1,088 | 1,090 | +2 |
| css/css-inline | 869 | 636 | 637 | +1 |
| html/rendering | 11,705 | 8,792 | 8,793 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 5 directories, the first 5)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| css/css-multicol | 2 | 2 |
| css/css-overflow | 2 | 1 |
| css/css-conditional | 1 | 1 |
| html/semantics | 1 | 1 |
| preload | 1 | 1 |

**Tests that lost most** (the first 6 of 6)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /css/css-overflow/scroll-markers/column-scroll-marker-focus-004.html | 2 | 0 | 11 |
| /css/css-conditional/container-queries/column-spanner-in-container.html | 2 | 1 | 3 |
| /css/css-multicol/getclientrects-004.html | 1 | 0 | 13 |
| /css/css-multicol/subpixel-column-progression.html | 1 | 0 | 4 |
| /html/semantics/embedded-content/the-iframe-element/cross_origin_parentage.sub.html | 2 | 1 | 3 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |

**Commits between** (36)

- `f3f1f41a3` Real pages: compressible images in lines, list bullets with shaped fonts, larger images held, WOFF 1.0, linear-gradient backgrounds
- `cb72465e3` Real pages: multicol, gradient line exact on the sides, flex content bases rounded up, tests
- `ba32b1e1c` Style: the new properties are among apply's own (apply_other)
- `ed4949397` Layout: listMarker public; bullets of a shaped font checked directly
- `e36169ad6` WebRepaint: sameShape knows the new style fields (gradients never repaint-only; column fields compared)
- `4951df347` Multicol: each column's children laid out in their column (no paint drawn twice); columnFirsts
- `9debb1ff7` Decoders: no Nat left shift in the bit readers (inflate, JPEG, PNG samples, base64)
- `163d391c5` lean4-performance skill: Nat left shift is a big-number call; decimal literals in pixel loops
- `805522b26` WebRender: the outer svg's style gives background-image to HTML layout, never to the SVG reader
- `ff086b653` Real-page fixes: no site names in code, tests or manifest; wording general
- `47c19ac05` BubblePopJS heap: measured allocation baseline, design record and counting instruments
- `0df197c3b` bubblepop_perf/alloc: build-count.sh can also make a plain -O3 leanjs from the same generated C
- `2ffeb7bdf` BubblePopJS RegExp matcher: a character read allocates nothing; no continuation for a first term that fails
- `ba5ba448e` Origin isolation checks C1 to C5 as tests (issue 518)
- `ba2cecc3a` Workers: the engine refuses a script URL of another origin (issue 518, C4)
- `713f38993` Origin isolation lemmas L0 and L6 (issue 518)
- `8fc690365` DOM imports refuse nodes of a cross-origin frame's document (issue 518, C1)
- `143ec5031` dataflow inventory: the Isolation directory
- `ab80d5487` Merge main into wip/rp-fix-grid (PR 530)
- `0137191ed` Merge pull request #538 from danbri/wip/heap-design
- `dd705f88f` bubblepop_perf/alloc: the counting build records the line of each call site in the generated C
- `f4164ecbc` BubblePopJS: a call's step decrement updates the heap record in place (HeapOf.decStep)
- `f94e20707` Merge pull request #529 from danbri/wip/iso-checks
- `6b996226c` Add .claude/skills symlink for the background-watchers skill
- `fbe8649d4` Hub: a link never leaves Foafnaut by itself; Wikimedia articles read through their CORS REST API, other sites read directly when they allow 
- `e6b492ab0` Hub: a page read from another site keeps its address's fragment; link check returns to the index after a failure too
- `3ffcaa8ac` Hub: CSS '{#copy' in index.njk opened a Nunjucks comment and failed the Pages build; a space, and a test against '{#' in the Hub app templat
- `2f40646b8` Merge pull request #530 from danbri/wip/rp-fix-grid
- `9919aba78` Merge pull request #544 from danbri/wip/heap-callpath
- `e23ffe3ab` BubblePopJS: iterCloseAbrupt runs out of fuel at fuel 0, as every function of the evaluator's block does (it threw its completion); theorems
- `899dc08bd` BubblePopJS: moreNative and callNative split into one definition per family of built-ins (issue 531)
- `c1d519d09` Merge pull request #543 from danbri/wip/hub-links
- `08984f4e3` Canvas origin-clean flags in the engine; no image bytes in the page's realm (issue 524)
- `e7604a84f` Merge pull request #534 from danbri/wip/c2-taint
- `65a5c0237` Merge pull request #542 from danbri/wip/itercloseabrupt-fuel0
- `8a22b20a3` Merge pull request #545 from danbri/wip/split531

