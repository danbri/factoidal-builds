### Since the previous full run: +43 subtests (+0.0019 points)

Previous: `20261116T2019Z-wpt-linux-x86_64-gh43948541942a1`, core `efa7f089c`, 92.0305%. This run: core `696f967ab`, 92.0323%; 57 commits between.
Tests that lost subtests: 1 (-16); that gained: 26 (+59). Page outcomes: OK +2, TIMEOUT -2.

**Directories that fell** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/webappapis | 3,674 | 3,033 | 3,017 | -16 |

**Directories that rose** (7; the first 7)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| urlpattern | 3,266 | 2,994 | 3,030 | +36 |
| workers | 1,598 | 704 | 714 | +10 |
| fetch | 13,288 | 8,816 | 8,821 | +5 |
| mixed-content | 2,281 | 1,304 | 1,309 | +5 |
| css/css-values | 10,428 | 4,910 | 4,911 | +1 |
| html/semantics | 22,381 | 15,176 | 15,177 | +1 |
| preload | 956 | 242 | 243 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 1 directories, the first 1)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| html/webappapis | 16 | 1 |

**Tests that lost most** (the first 1 of 1)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /html/webappapis/dynamic-markup-insertion/opening-the-input-stream/no-new-global.window.html | 16 | 0 | 17 |

**Commits between** (57)

- `a8876ef1e` URL parser as the standard's state machine (step/run), with a proved bound of 3n + 16 rounds
- `365fd53d3` URLPattern: compile regular expressions with the v flag, as the Standard does
- `369ebcf9e` URL parser: run is irreducible, so proofs about callers of parseUrl do not unfold the machine
- `f09f27a87` Serif as the initial font-family, drawn with bundled Liberation Serif
- `3d6ecd00f` Generated demo pages say sans-serif (build-demo-pages.py, status-to-html.py)
- `af15cd6d6` Keep status-to-html.py as it was (its output is a web-render fixture)
- `6975e5b06` familyFontsWith_none: one more proof route
- `bee60274c` Serif choice theorems: mem form for simp, rewrite proofs for familyFontsWith
- `1850a5240` familyFontsWith_none: name the condition before rewriting
- `d4cbe3993` BubblePopJS parser: peek, peekAt, advance, atP, atK are inlined
- `0f063eb40` docs/bubblepopjs-heap.md: step 6 checks the estimate model (34% predicted, 37% measured on marked)
- `959b35810` bubblepop_perf/alloc: the counting build records the line of each call site in the generated C
- `6f4a8a958` Merge remote-tracking branch 'origin/main' into wip/serif-default
- `fa6f92ff5` Scripts: undo of a sync request by a log of the cells an action writes; no heap limit
- `cd474766b` Origin isolation C6: a classic script of another origin runs from the engine's copy; its bytes never enter the page's realm; muted errors (i
- `8e646f2ea` Origin isolation C2e: a VideoFrame from a source that is not origin-clean is refused (check)
- `a5ba1dea4` Muted errors for parsed classic scripts of another origin (HTML report an exception); C6 covers them
- `7cd6128d6` Muted errors: an absolute script URL needs no base tracking
- `492ea833a` serveScript through scriptAns; serveScript_answer by cases on the source
- `6277c08c9` Frames: a frame's src is parsed against its node document's base URL, not the page's (HTML 4.8.5); check C1b
- `fc4639d80` Origin isolation record: C1b and C6 results; follow-up for a cross-origin frame session's network
- `f46f625ad` Trial merge: 547 + 549
- `7a2010cca` Trial merge: 547 + 549 + 548 on main 8a22b20a3
- `2242b58da` Canvas: a VideoFrame read of a source that is not origin-clean is refused (C2e theorems)
- `dd1284199` Merge main into wip/heap-parser (PR 540)
- `f42e2fea6` Merge remote-tracking branch 'origin/main' into wip/serif-default
- `34c6b0842` Merge main (fuel monotonicity of the whole evaluator, PR 539; natives split, PR 545)
- `4e5a94f10` Skills: JSFuelMono is checked by the js-fuel-mono job of build.yml (a Linux merge gate); what to regenerate when a change to the evaluator o
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
- `45e492f95` Merge remote-tracking branch 'origin/main' into wip/no-default-search
- `f51919862` Merge main (origin isolation 547/548/549, parser inlining 540, serif default 537)
- `fb3fcb8ec` Serif face before the first layout: serif pages laid out once
- `52aa4453b` Merge pull request #555 from danbri/wip/iso4-c2e
- `590808305` hub_boot_breakdown: serve bundled fonts from this checkout (a font not yet on the live Hub, such as Liberation Serif)
- `a03c69222` Merge pull request #552 from danbri/wip/jit2-fuelmono-ci
- `d451fae34` Merge main (C2e theorems 555, JSFuelMono CI job 552)
- `6be1f3e3b` Merge pull request #550 from danbri/wip/xhr-undo
- `ade143123` Skills: the Mac release lane (mac-release.yml), the macOS budget, the landing label and darwin-status.json
- `0b423e0fd` Merge pull request #553 from danbri/wip/no-default-search
- `8d3af851b` Merge pull request #558 from danbri/wip/macalways-docs
- `127fe321d` Merge main into wip/sizefix (PR 554)
- `fcdbf523f` Merge pull request #556 from danbri/wip/serif-preload
- `64d719451` binary-budget.json: leanjs on macOS arm64 11,868,032 B after the merge of main 8d3af851b (PR 550 undo log and others; +3.9%, raised by hand 
- `bc4261b99` Merge pull request #554 from danbri/wip/sizefix
- `27d198efe` Merge remote-tracking branch 'origin/main' into wip/url-theorems
- `696f967ab` Merge pull request #525 from danbri/wip/url-theorems

