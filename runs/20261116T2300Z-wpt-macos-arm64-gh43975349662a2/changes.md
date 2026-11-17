### Since the previous full run: +547 subtests (+0.0241 points)

Previous: `20261116T2320Z-wpt-macos-arm64-gh43978344597a1`, core `0137191ed`, 92.0062%. This run: core `efa7f089c`, 92.0302%; 43 commits between.
Tests that lost subtests: 7 (-11); that gained: 71 (+558). Page outcomes: NO_RESULT +1, OK -1, STALL +2, TIMEOUT -2.

**Directories that fell** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/rendering | 11,705 | 8,792 | 8,789 | -3 |
| css/css-overflow | 1,215 | 728 | 726 | -2 |
| html/semantics | 22,381 | 15,177 | 15,175 | -2 |
| css/css-conditional | 3,298 | 2,239 | 2,238 | -1 |

**Directories that rose** (8; the first 8)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/css-text | 5,863 | 3,297 | 3,805 | +508 |
| css/css-multicol | 1,625 | 1,406 | 1,424 | +18 |
| html/canvas | 6,251 | 3,675 | 3,686 | +11 |
| webcodecs | 3,922 | 2,577 | 2,584 | +7 |
| css/css-break | 787 | 585 | 590 | +5 |
| css/css-flexbox | 4,933 | 3,786 | 3,789 | +3 |
| mathml | 4,321 | 1,089 | 1,091 | +2 |
| css/css-inline | 869 | 636 | 637 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 5 directories, the first 5)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| html/rendering | 4 | 1 |
| css/css-multicol | 2 | 2 |
| css/css-overflow | 2 | 1 |
| html/semantics | 2 | 2 |
| css/css-conditional | 1 | 1 |

**Tests that lost most** (the first 7 of 7)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /html/rendering/non-replaced-elements/tables/table-rowspan-height-distribution.html | 4 | 0 | 4 |
| /css/css-overflow/scroll-markers/column-scroll-marker-focus-004.html | 2 | 0 | 11 |
| /css/css-conditional/container-queries/column-spanner-in-container.html | 2 | 1 | 3 |
| /css/css-multicol/getclientrects-004.html | 1 | 0 | 13 |
| /css/css-multicol/subpixel-column-progression.html | 1 | 0 | 4 |
| /html/semantics/embedded-content/the-iframe-element/cross_origin_parentage.sub.html | 2 | 1 | 3 |
| /html/semantics/embedded-content/the-img-element/list-of-available-images-does-not-coalesce-in-flight-requests.sub.tentative.html | 1 | 0 | 1 |

**Commits between** (43)

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
- `b42b559f8` WIP BubblePopJS fuel monotonicity over the whole block (not all checked yet): walk as one tactic with info trees off, built-in lemmas from t
- `4242929c8` WIP fuel monotonicity: rules for if, filterM, inRealm, discard; match reduction; capped split; iterCloseAbrupt out of fuel at 0 (was not mon
- `7888e885d` BubblePopJS fuel monotonicity over the block after the natives move: 126 steps generated in groups, built-in lemmas from the dispatcher (in 
- `ba5ba448e` Origin isolation checks C1 to C5 as tests (issue 518)
- `ba2cecc3a` Workers: the engine refuses a script URL of another origin (issue 518, C4)
- `713f38993` Origin isolation lemmas L0 and L6 (issue 518)
- `8fc690365` DOM imports refuse nodes of a cross-origin frame's document (issue 518, C1)
- `143ec5031` dataflow inventory: the Isolation directory
- `ab80d5487` Merge main into wip/rp-fix-grid (PR 530)
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
- `efca8bc81` BubblePopJS fuel monotonicity: IH_all proved, on the built-ins split by family (issue 531)
- `271146d92` fetch-builds: take the ancestor release nearest HEAD, not the newest published (an older commit published late put an engine without PR 516 
- `08984f4e3` Canvas origin-clean flags in the engine; no image bytes in the page's realm (issue 524)
- `e7604a84f` Merge pull request #534 from danbri/wip/c2-taint
- `65a5c0237` Merge pull request #542 from danbri/wip/itercloseabrupt-fuel0
- `8a22b20a3` Merge pull request #545 from danbri/wip/split531
- `9dafebe13` Fuel-monotonicity tactics: loops in place of recursion in the compiled code (the tail-recursion gate)
- `3b925035e` Merge main (the split of the built-in dispatchers and the iterCloseAbrupt fix are in)
- `fbc67b0bc` Canvas 2D: any change of a canvas's width or height attribute resets its bitmap and context state (HTML 4.12.5), not only the property sette
- `2ff4472d2` Merge pull request #546 from danbri/wip/fetch-builds-nearest
- `f64cb2e67` Merge pull request #539 from danbri/wip/fuelmono-all
- `efa7f089c` Merge pull request #548 from danbri/wip/iso3-canvas

