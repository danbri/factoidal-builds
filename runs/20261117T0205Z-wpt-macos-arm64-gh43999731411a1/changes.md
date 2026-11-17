### Since the previous full run: +270 subtests (+0.0119 points)

Previous: `20261116T2320Z-wpt-macos-arm64-gh43978344597a1`, core `0137191ed`, 92.0062%. This run: core `bc4261b99`, 92.0180%; 95 commits between.
Tests that lost subtests: 26 (-304); that gained: 81 (+574). Page outcomes: ERROR +7, OK -8, TIMEOUT +1.

**Directories that fell** (8; the first 8)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| streams | 5,796 | 5,580 | 5,489 | -91 |
| selection/(root) | 33,918 | 33,664 | 33,581 | -83 |
| html/semantics | 22,381 | 15,177 | 15,118 | -59 |
| xhr | 2,344 | 1,819 | 1,787 | -32 |
| referrer-policy | 8,815 | 5,029 | 5,002 | -27 |
| svg/painting | 672 | 424 | 418 | -6 |
| css/css-overflow | 1,215 | 728 | 726 | -2 |
| css/css-conditional | 3,298 | 2,239 | 2,238 | -1 |

**Directories that rose** (12; the first 12)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/css-text | 5,863 | 3,297 | 3,805 | +508 |
| css/css-multicol | 1,625 | 1,406 | 1,424 | +18 |
| html/canvas | 6,251 | 3,675 | 3,686 | +11 |
| workers | 1,598 | 704 | 714 | +10 |
| webcodecs | 3,922 | 2,577 | 2,584 | +7 |
| css/css-break | 787 | 585 | 590 | +5 |
| fetch | 13,288 | 8,804 | 8,808 | +4 |
| css/css-flexbox | 4,933 | 3,786 | 3,789 | +3 |
| mathml | 4,321 | 1,089 | 1,091 | +2 |
| css/css-inline | 869 | 636 | 637 | +1 |
| css/css-values | 10,428 | 4,910 | 4,911 | +1 |
| html/rendering | 11,705 | 8,792 | 8,793 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 11 directories, the first 11)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| selection | 83 | 1 |
| streams/piping | 75 | 2 |
| html/semantics | 60 | 6 |
| xhr | 32 | 6 |
| referrer-policy/gen | 27 | 4 |
| streams/transform-streams | 11 | 1 |
| svg/painting | 6 | 1 |
| streams/readable-streams | 5 | 1 |
| css/css-multicol | 2 | 2 |
| css/css-overflow | 2 | 1 |
| css/css-conditional | 1 | 1 |

**Tests that lost most** (the first 26 of 26)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /selection/idlharness.window.html | 83 | 0 | 112 |
| /html/semantics/the-button-element/command-and-commandfor/invalid-element-types.html?command=show-modal&half=first | 55 | 0 | 55 |
| /streams/piping/pipe-through.any.sharedworker.html | 42 | 0 | 43 |
| /streams/piping/abort.any.sharedworker.html | 33 | 0 | 33 |
| /xhr/status-async.htm | 24 | 1 | 27 |
| /referrer-policy/gen/worker-module.http-rp/unsafe-url/fetch.http.html | 12 | 0 | 12 |
| /streams/transform-streams/reentrant-strategies.any.worker.html | 11 | 0 | 11 |
| /referrer-policy/gen/worker-module.http-rp/no-referrer/fetch.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/worker-module.http-rp/same-origin/fetch.http.html | 10 | 4 | 10 |
| /svg/painting/parsing/paint-order-computed.svg | 6 | 0 | 16 |
| /streams/readable-streams/garbage-collection.any.worker.html | 5 | 0 | 5 |
| /referrer-policy/gen/worker-classic.http-rp/unsafe-url/fetch.http.html | 12 | 9 | 12 |
| /xhr/cors-expose-star.sub.any.worker.html | 3 | 0 | 3 |
| /css/css-overflow/scroll-markers/column-scroll-marker-focus-004.html | 2 | 0 | 11 |
| /xhr/access-control-and-redirects-async.any.html | 7 | 5 | 7 |
| /xhr/send-conditional-cors.htm | 2 | 0 | 2 |
| /css/css-conditional/container-queries/column-spanner-in-container.html | 2 | 1 | 3 |
| /css/css-multicol/getclientrects-004.html | 1 | 0 | 13 |
| /css/css-multicol/subpixel-column-progression.html | 1 | 0 | 4 |
| /html/semantics/embedded-content/the-iframe-element/cross_origin_parentage.sub.html | 2 | 1 | 3 |
| /html/semantics/embedded-content/the-iframe-element/iframe_sandbox_anchor_download_block_downloads.tentative.html | 2 | 1 | 5 |
| /html/semantics/embedded-content/the-img-element/img.complete.html | 10 | 9 | 19 |
| /html/semantics/embedded-content/the-img-element/list-of-available-images-does-not-coalesce-in-flight-requests.sub.tentative.html | 1 | 0 | 1 |
| /html/semantics/scripting-1/the-template-element/template-element/template-descendant-frameset.html | 3 | 2 | 3 |
| /xhr/access-control-basic-allow-non-cors-safelisted-method.any.worker.html | 1 | 0 | 1 |
| /xhr/open-url-worker-origin.htm | 1 | 0 | 3 |

**Commits between** (95)

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
- `f09f27a87` Serif as the initial font-family, drawn with bundled Liberation Serif
- `3d6ecd00f` Generated demo pages say sans-serif (build-demo-pages.py, status-to-html.py)
- `af15cd6d6` Keep status-to-html.py as it was (its output is a web-render fixture)
- `6975e5b06` familyFontsWith_none: one more proof route
- `bee60274c` Serif choice theorems: mem form for simp, rewrite proofs for familyFontsWith
- `b42b559f8` WIP BubblePopJS fuel monotonicity over the whole block (not all checked yet): walk as one tactic with info trees off, built-in lemmas from t
- `4242929c8` WIP fuel monotonicity: rules for if, filterM, inRealm, discard; match reduction; capped split; iterCloseAbrupt out of fuel at 0 (was not mon
- `7888e885d` BubblePopJS fuel monotonicity over the block after the natives move: 126 steps generated in groups, built-in lemmas from the dispatcher (in 
- `1850a5240` familyFontsWith_none: name the condition before rewriting
- `ba5ba448e` Origin isolation checks C1 to C5 as tests (issue 518)
- `ba2cecc3a` Workers: the engine refuses a script URL of another origin (issue 518, C4)
- `713f38993` Origin isolation lemmas L0 and L6 (issue 518)
- `8fc690365` DOM imports refuse nodes of a cross-origin frame's document (issue 518, C1)
- `143ec5031` dataflow inventory: the Isolation directory
- `ab80d5487` Merge main into wip/rp-fix-grid (PR 530)
- `d4cbe3993` BubblePopJS parser: peek, peekAt, advance, atP, atK are inlined
- `0f063eb40` docs/bubblepopjs-heap.md: step 6 checks the estimate model (34% predicted, 37% measured on marked)
- `959b35810` bubblepop_perf/alloc: the counting build records the line of each call site in the generated C
- `dd705f88f` bubblepop_perf/alloc: the counting build records the line of each call site in the generated C
- `f4164ecbc` BubblePopJS: a call's step decrement updates the heap record in place (HeapOf.decStep)
- `6f4a8a958` Merge remote-tracking branch 'origin/main' into wip/serif-default
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
- `fa6f92ff5` Scripts: undo of a sync request by a log of the cells an action writes; no heap limit
- `65a5c0237` Merge pull request #542 from danbri/wip/itercloseabrupt-fuel0
- `8a22b20a3` Merge pull request #545 from danbri/wip/split531
- `9dafebe13` Fuel-monotonicity tactics: loops in place of recursion in the compiled code (the tail-recursion gate)
- `3b925035e` Merge main (the split of the built-in dispatchers and the iterCloseAbrupt fix are in)
- `cd474766b` Origin isolation C6: a classic script of another origin runs from the engine's copy; its bytes never enter the page's realm; muted errors (i
- `8e646f2ea` Origin isolation C2e: a VideoFrame from a source that is not origin-clean is refused (check)
- `a5ba1dea4` Muted errors for parsed classic scripts of another origin (HTML report an exception); C6 covers them
- `7cd6128d6` Muted errors: an absolute script URL needs no base tracking
- `492ea833a` serveScript through scriptAns; serveScript_answer by cases on the source
- `fbc67b0bc` Canvas 2D: any change of a canvas's width or height attribute resets its bitmap and context state (HTML 4.12.5), not only the property sette
- `6277c08c9` Frames: a frame's src is parsed against its node document's base URL, not the page's (HTML 4.8.5); check C1b
- `fc4639d80` Origin isolation record: C1b and C6 results; follow-up for a cross-origin frame session's network
- `2ff4472d2` Merge pull request #546 from danbri/wip/fetch-builds-nearest
- `f46f625ad` Trial merge: 547 + 549
- `7a2010cca` Trial merge: 547 + 549 + 548 on main 8a22b20a3
- `2242b58da` Canvas: a VideoFrame read of a source that is not origin-clean is refused (C2e theorems)
- `dd1284199` Merge main into wip/heap-parser (PR 540)
- `f42e2fea6` Merge remote-tracking branch 'origin/main' into wip/serif-default
- `f64cb2e67` Merge pull request #539 from danbri/wip/fuelmono-all
- `34c6b0842` Merge main (fuel monotonicity of the whole evaluator, PR 539; natives split, PR 545)
- `4e5a94f10` Skills: JSFuelMono is checked by the js-fuel-mono job of build.yml (a Linux merge gate); what to regenerate when a change to the evaluator o
- `efa7f089c` Merge pull request #548 from danbri/wip/iso3-canvas
- `6db7d8517` Merge main into wip/heap-parser (PR 540)
- `8269aa2e1` Foafnaut: no default search engine, no host list to the system browser
- `3bb133023` WebRoute, WebShell: proofs that do not depend on simp names for String.isEmpty; structural decodeBytes
- `4dc55d8a0` Merge pull request #540 from danbri/wip/heap-parser
- `cfd5785be` WebRoute: decodeBytes as a left fold; WebShell, WebDocument: compile fixes
- `3752f81c8` Merge remote-tracking branch 'origin/main' into wip/no-default-search
- `fc6f7eddb` leanjs no longer links Lean's elaborator: L4Factoidal.JS does not import the fuel-monotonicity tactics (issue 551)
- `9b6307013` binary-budget.json: bubblepop-test262 31,294,992 B and leanjs 11,420,160 B on macOS arm64 (measured on wip/sizefix)
- `7b632b246` Merge pull request #547 from danbri/wip/iso3-script
- `3b1db8e02` Merge pull request #549 from danbri/wip/iso3-frames
- `3c53371c1` HostContract: searchPage, searchChoices, searchSetting and outsidePage are query ops
- `35bf0598d` Merge pull request #537 from danbri/wip/serif-default

