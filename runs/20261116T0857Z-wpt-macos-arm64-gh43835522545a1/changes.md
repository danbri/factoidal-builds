### Since the previous full run: +2,621 subtests (+0.1154 points)

Previous: `20261115T2148Z-wpt-macos-arm64-gh43765681204a1`, core `04740693f`, 91.8407%. This run: core `0ccd896a0`, 91.9560%; 91 commits between.
Tests that lost subtests: 117 (-502); that gained: 2,237 (+3,123). Page outcomes: CRASH +1, ERROR -44, NO_RESULT +6, OK +34, STALL +2, TIMEOUT +1.

**Directories that fell** (10; the first 10)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| streams | 5,796 | 5,580 | 5,313 | -267 |
| referrer-policy | 8,815 | 5,029 | 4,911 | -118 |
| urlpattern | 3,266 | 3,014 | 2,994 | -20 |
| custom-elements | 4,822 | 3,833 | 3,820 | -13 |
| css/css-position | 1,605 | 1,368 | 1,362 | -6 |
| websockets | 2,389 | 1,249 | 1,243 | -6 |
| css/css-page | 159 | 60 | 56 | -4 |
| console | 107 | 30 | 28 | -2 |
| css/cssom-view | 2,714 | 1,197 | 1,195 | -2 |
| css/css-anchor-position | 13,670 | 10,895 | 10,894 | -1 |

**Directories that rose** (26; the first 26)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| third_party/test262 | 53,833 | 43,491 | 45,626 | +2,135 |
| html/rendering | 11,705 | 8,461 | 8,792 | +331 |
| webidl | 838 | 500 | 647 | +147 |
| html/infrastructure | 1,664 | 775 | 918 | +143 |
| html/semantics | 22,381 | 15,121 | 15,200 | +79 |
| html/webappapis | 3,674 | 2,975 | 3,033 | +58 |
| css/css-grid | 16,017 | 11,116 | 11,140 | +24 |
| css/css-sizing | 6,743 | 5,060 | 5,080 | +20 |
| user-timing | 862 | 426 | 446 | +20 |
| xhr | 2,344 | 1,788 | 1,803 | +15 |
| css/CSS2 | 2,566 | 2,432 | 2,444 | +12 |
| IndexedDB | 5,853 | 5,493 | 5,504 | +11 |
| subresource-integrity | 491 | 184 | 195 | +11 |
| resize-observer | 131 | 73 | 81 | +8 |
| webcodecs | 3,922 | 2,561 | 2,569 | +8 |
| js | 160 | 65 | 72 | +7 |
| webmessaging | 304 | 147 | 153 | +6 |
| css/css-values | 10,428 | 4,905 | 4,910 | +5 |
| ecmascript | 21 | 13 | 17 | +4 |
| fetch | 13,288 | 8,800 | 8,804 | +4 |
| workers | 1,598 | 700 | 703 | +3 |
| FileAPI | 1,645 | 1,203 | 1,205 | +2 |
| css/css-contain | 499 | 307 | 309 | +2 |
| intersection-observer | 440 | 209 | 211 | +2 |
| trusted-types | 3,754 | 2,712 | 2,714 | +2 |
| css/css-borders | 4,906 | 4,348 | 4,349 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 23 directories, the first 23)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| streams | 218 | 1 |
| referrer-policy/gen | 117 | 39 |
| streams/piping | 35 | 2 |
| third_party/test262 | 23 | 23 |
| urlpattern | 20 | 12 |
| css/css-position | 18 | 11 |
| xhr | 14 | 7 |
| custom-elements | 12 | 1 |
| streams/writable-streams | 8 | 1 |
| websockets/interfaces | 7 | 4 |
| css/cssom-view | 6 | 1 |
| streams/transform-streams | 6 | 1 |
| css/css-page | 4 | 1 |
| html/semantics | 3 | 3 |
| console | 2 | 2 |
| webcodecs | 2 | 1 |
| IndexedDB | 1 | 1 |
| css/css-anchor-position | 1 | 1 |
| custom-elements/registries | 1 | 1 |
| intersection-observer | 1 | 1 |
| referrer-policy/4K | 1 | 1 |
| websockets/constructor | 1 | 1 |
| workers/interfaces | 1 | 1 |

**Tests that lost most** (the first 40 of 117)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /streams/idlharness.any.sharedworker.html | 218 | 0 | 228 |
| /streams/piping/close-propagation-forward.any.sharedworker.html | 30 | 0 | 30 |
| /custom-elements/CustomElementRegistry.html | 43 | 31 | 46 |
| /streams/writable-streams/start.any.worker.html | 8 | 0 | 8 |
| /css/cssom-view/offsetTopLeft-inline-offsetParent.html | 13 | 7 | 37 |
| /referrer-policy/gen/top.http-rp/no-referrer/fetch.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/top.http-rp/same-origin/script-tag.http.html | 10 | 4 | 10 |
| /referrer-policy/gen/top.meta/origin/script-tag.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/top.meta/unset/fetch.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/worker-classic.http-rp/no-referrer-when-downgrade/fetch.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/worker-classic.http-rp/origin/fetch.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/worker-classic.http-rp/strict-origin/fetch.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/worker-module.http-rp/no-referrer-when-downgrade/fetch.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/worker-module.http-rp/origin/fetch.http.html | 12 | 6 | 12 |
| /streams/transform-streams/terminate.any.worker.html | 6 | 0 | 6 |
| /streams/piping/flow-control.any.sharedworker.html | 5 | 0 | 5 |
| /xhr/formdata.html | 8 | 3 | 9 |
| /css/css-page/parsing/size-valid.html | 5 | 1 | 15 |
| /referrer-policy/gen/worker-module.http-rp/strict-origin/fetch.http.html | 12 | 8 | 12 |
| /websockets/interfaces/WebSocket/events/019.html?default | 4 | 0 | 4 |
| /css/css-position/sticky/position-sticky-nested-left.html | 3 | 0 | 5 |
| /referrer-policy/gen/top.http-rp/origin-when-cross-origin/a-tag.http.html | 3 | 0 | 4 |
| /referrer-policy/gen/top.meta/always/fetch.http.html | 12 | 9 | 12 |
| /referrer-policy/gen/top.meta/default/a-tag.http.html | 3 | 0 | 4 |
| /xhr/access-control-and-redirects-async-same-origin.any.worker.html | 6 | 3 | 6 |
| /css/css-position/sticky/position-sticky-left.html | 2 | 0 | 3 |
| /css/css-position/sticky/position-sticky-nested-right.html | 3 | 1 | 5 |
| /css/css-position/sticky/position-sticky-nested-top.html | 3 | 1 | 5 |
| /css/css-position/sticky/position-sticky-overflow-padding.html | 3 | 1 | 3 |
| /css/css-position/sticky/position-sticky-right.html | 2 | 0 | 3 |
| /referrer-policy/gen/req.attr/unsafe-url/svg-a-tag.http.html | 2 | 0 | 4 |
| /referrer-policy/gen/srcdoc-inherit.http-rp/no-referrer/worker-module.http.html | 2 | 0 | 2 |
| /referrer-policy/gen/srcdoc.meta/no-referrer-when-downgrade/worker-module.http.html | 2 | 0 | 2 |
| /referrer-policy/gen/srcdoc.meta/no-referrer/worker-module.http.html | 2 | 0 | 2 |
| /referrer-policy/gen/srcdoc.meta/origin-when-cross-origin/iframe-tag.http.html | 2 | 0 | 12 |
| /referrer-policy/gen/srcdoc.meta/origin-when-cross-origin/worker-module.http.html | 2 | 0 | 2 |
| /referrer-policy/gen/srcdoc.meta/origin-when-crossorigin/iframe-tag.http.html | 2 | 0 | 12 |
| /referrer-policy/gen/srcdoc.meta/origin-when-crossorigin/worker-module.http.html | 2 | 0 | 2 |
| /referrer-policy/gen/srcdoc.meta/origin/iframe-tag.http.html | 2 | 0 | 12 |
| /referrer-policy/gen/srcdoc.meta/origin/worker-module.http.html | 2 | 0 | 2 |

**Commits between** (91)

- `a71d1e3ce` Script sessions: a session the engine no longer holds ends the page's scripts
- `499aec440` script_session_gone_test.ts: typed log callbacks (deno check)
- `9e11a8041` leanjs test262-files ROOT LIST: each listed test in every mode Test262 runs it in (modesOf: sloppy and strict, onlyStrict, noStrict/raw, mod
- `16264b02b` leanjs test262-files: module tests as module graphs loaded from the files they name (resolution-phase negatives), $262 with global and detac
- `bb0ccb4bc` skills/wpt-runs: section 9, full Test262 runs (suite, rules, engine, score and ex-features share, validity, triggers, records, test262.fyi r
- `a1f43352d` Test262 runner on any realm (JS/Test262.lean, from Main.lean) and lake exe bubblepop-test262: Test262 files on the page realm of LeanJS.prep
- `e0a24a924` skills/wpt-runs section 9: the score runs on the page realm (bubblepop-test262); leanjs is a diagnostic
- `8bc312206` Merge pull request #477 from danbri/wip/nosession
- `c7e1c5fde` skills/wpt-runs: the workflow is named Test262
- `b418e7589` Conformance wording: the 80% Test262 and 90% WPT thresholds are Apple's rule, not the EU's (#484)
- `1dbb28396` Textnaut 0.1.4: version and README notes (native Linux pin; 0.1.3's Wasm pin no longer matches its rebuilt release)
- `16c3e288e` Textnaut 0.1.4: pin the Wasm and the self-contained native Linux engine of 5029cc163 (build-5029cc163906-foafnaut-web, -foafnaut-linux-x86_6
- `649292c51` Real-page survey: a tripped log gate (native-html-log-flood) is counted per page (log_floods, the first trip's top messages) and fails the o
- `294271ec2` Merge pull request #485 from danbri/wip/realpages-logflood
- `f83009612` Log gate: a flood of console lines is summarised and named, never silent
- `18f1f4bed` log-gate.mjs: option types for deno check
- `5058e9f29` Agent brief and skills: coordination in fncg, memory caps on Lean processes, disk and timing locks, releases never replaced, vendored real p
- `93b1d9ef8` BubblePopJS: register machine is a parameter of the run (HeapOf.useVm, BUBBLEPOP_VM=off for leanjs); blockN in Stmt.contOutF and genEnter; t
- `901932f5b` BubblePopJS: a halt passes through every handler (catchJS at 69 tryCatch sites)
- `8bcef5c72` BubblePopJS: fuel monotonicity, the relation and its rules (JS/FuelMono.lean); drop the tier-1 cases on this branch
- `80443298d` BubblePopJS fuel monotonicity: rules for forIn (List, Array, Range), mapM, foldlM, filterMapM, map; walk tactic in two halves around the gen
- `71f6b49aa` BubblePopJS fuel monotonicity spike: 75 of 116 step lemmas proved by a generated walk (JS/FuelMonoSteps.lean); the state of the proof in JS/
- `9504dce9e` Mac app launcher: rotate trace.jsonl over 64 MiB at launch (#488)
- `553226525` Merge pull request #487 from danbri/wip/jit-proof
- `c95c532d8` Light shared start page, stress tests page, demo index tidy, ray-marching demo (#492)
- `44d660c16` raymarch.html: frame-rate modes and frame-time percentiles
- `d2c0d20ab` Veil models: system-level transition systems in formal/veil (#494)
- `82ad63988` Hub Conformance: semantic web and data formats, one row per suite, OWL 2 by population (#497)
- `e0e235b17` Test262 host for BubblePopJS: no CRASH or STALL, $262 realms, import(), top-level await, JSON modules
- `01156778d` Modules: indirect exports resolved at link, a module's functions are lexical, for-in with await on the generator machine, shared Symbol regi
- `cf22c0eae` Promise combinators append values without Array.prototype setters; runner heap 2^22; import.source() rejects with a TypeError
- `b79e7bb92` Tail-recursion gate: constructNative and protoFromCtor, fuel-bounded calls as construct and get
- `4d8f37e72` Test262 runner: an error of the module graph after an import is the test's outcome
- `501d91d02` Import attributes: an unknown key parses and is refused when the module is loaded (SyntaxError at resolution)
- `1d014d20d` BubblePopJS Test262 built-ins: RegExp (Unicode 17 properties, code points with u/v, Canonicalize, backward lookbehind, modifiers, v class se
- `11ef3831b` Merge pull request #499 from danbri/wip/t262-builtins
- `6f20dd4fd` BubblePopJS: JSON.stringify replacer and space (SerializeJSONProperty), String.prototype methods writable, includes/startsWith/endsWith refu
- `1b5f7b439` Regex/Base64: no dangling else, bounded whitespace skip
- `3b207d02c` BubblePopJS: a Promise subclass constructor settles its own object (super() runs the Promise constructor's steps on this)
- `0a62bf28a` HostContract: every Foafnaut target described in Lean (model, trace conformance, cross-host agreement theorems)
- `2fcec0287` Host contract: boundary traces from Textnaut (native, Wasm) and the Hub's Textnaut host, checked by the engine (op hostContract); scroll lim
- `d1cae0dfe` Host contract: point the records at issue 458
- `3860cbdf9` HostContract: violations after its csimp theorem, so the compiled checker uses the loop (lean-csimp-reach gate)
- `1513ef6be` LabHygiene imports WebHostContract, so the hygiene ratchet sees the new lab module
- `07f5983f9` cpu_render_diff_check: serve finite-floats.mjs, which render_plan.ts imports since 3e6745f19 (the Hub layer surface failed to load)
- `ce5f07d65` spinal-bisect budgets: static probe frame limit at spinal-perf's 1500 ms (accepted: 560 ms on the macOS CI runner, about 500 ms on an M1 in 
- `be8f7503e` Merge pull request #459 from danbri/wip/host-contract
- `58f17c53e` BubblePopJS: Array.prototype and %TypedArray%.prototype toLocaleString, subarray through TypedArraySpeciesCreate; guards
- `46396affe` BubblePopJS: Function.prototype.bind per §20.2.3.2 (target's prototype, own length as a Number), closures' toString in the NativeFunction fo
- `1b2fc90d5` Tail-recursion allow lines: deleteOrThrow (Proxy chain) and arrayGeneric (fuel-bounded [[Get]]/[[Set]] cycle) from #499
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

