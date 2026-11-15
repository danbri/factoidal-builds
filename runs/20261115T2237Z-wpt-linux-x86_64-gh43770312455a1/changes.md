### Since the previous full run: +174 subtests (+0.0077 points)

Previous: `20261115T1927Z-wpt-linux-x86_64-gh43752553929a1`, core `5029cc163`, 91.8474%. This run: core `9504dce9e`, 91.8550%; 50 commits between.
Tests that lost subtests: 4 (-8); that gained: 165 (+182). Page outcomes: OK +2, STALL -1, TIMEOUT -1.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/semantics | 22,381 | 15,160 | 15,155 | -5 |
| preload | 956 | 243 | 242 | -1 |

**Directories that rose** (6; the first 6)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| third_party/test262 | 53,833 | 43,375 | 43,533 | +158 |
| webcodecs | 3,922 | 2,572 | 2,584 | +12 |
| resource-timing | 1,207 | 19 | 24 | +5 |
| shadow-dom | 14,720 | 14,126 | 14,129 | +3 |
| fetch | 13,288 | 8,812 | 8,813 | +1 |
| html/dom | 72,400 | 69,540 | 69,541 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 3 directories, the first 3)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| html/semantics | 6 | 2 |
| preload | 1 | 1 |
| third_party/test262 | 1 | 1 |

**Tests that lost most** (the first 4 of 4)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /html/semantics/embedded-content/the-img-element/relevant-mutations.html | 77 | 72 | 113 |
| /html/semantics/embedded-content/the-img-element/list-of-available-images-does-not-coalesce-in-flight-requests.sub.tentative.html | 1 | 0 | 1 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |
| /third_party/test262/test/built-ins/RegExp/property-escapes/special-property-value-Script_Extensions-Unknown.test262.html | 1 | 0 | 1 |

**Commits between** (50)

- `1ae070e99` Retained compile reuses equal primitives, not only the same objects (issue 450)
- `ef77f50be` Tests of reuse after a relayout; plus-timer in the fast bisect budgets (issue 450)
- `23c7734fa` Merge pull request #469 from danbri/wip/prim-reuse
- `91aba4a0c` Real-page survey: runner, page list and budgets, comparison, and two run_html.ts options
- `1032f2a18` Real-page survey offline: snapshots (snapshot.ts, ZIP with provenance, vendored in factoidal-builds), replay into any host by --preload (rep
- `c95d0bb67` Real-page snapshots hold the built-in engine's own requests: replay.ts record mode (REALPAGES_RECORD), snapshot.ts --engine loads the page o
- `7424c5871` Merge pull request #472 from danbri/wip/realpages-ci
- `15b4152e9` Script turns: rule matchers of the layout reads are data made once (no n² key reads); reads counted at the boundary
- `a81bc2ffa` Merge pull request #466 from danbri/wip/script-turns-pr
- `42c287e74` Inline SVG deep in an HTML document no longer refuses the page
- `a71d1e3ce` Script sessions: a session the engine no longer holds ends the page's scripts
- `839127616` Merge pull request #467 from danbri/wip/svg-depth
- `b2b716fa2` BubblePopJS: RegExp property escapes \p{…} and \P{…} with the u flag
- `4492339c2` Merge pull request #468 from danbri/wip/regex-props
- `e38191c65` Module graphs: modules fetched and parsed by earlier attempts of a start are kept
- `1720a095a` Merge pull request #470 from danbri/wip/module-memo
- `ab8c98056` Real-page snapshots always keep the page itself (the United States article is over the 1.5 MB file cap); offline, a page missing from its sn
- `8ec037f3c` Merge pull request #478 from danbri/wip/realpages-ci-2
- `499aec440` script_session_gone_test.ts: typed log callbacks (deno check)
- `56dfb14d5` passmap-data.py: WPT Pass Map data from the recorded runs, with Test262
- `d46dd5e5d` Merge pull request #480 from danbri/wip/passmap-data
- `d087a0953` Add the .claude/skills symlink for the realpages-survey skill
- `e01634578` Hub: a Conformance page, Test262 first, then WPT, from data files kept in git
- `1a6dd0ecf` Merge pull request #481 from danbri/wip/hub-conformance
- `e6a544a7d` Per-tile edge lists for a path's fill (issue 450)
- `19ac380c7` Tile edge lists: a margin of a sixteenth of the tile's local rows (was half), Array filter with edgesMeeting_eq to the List form; one refere
- `a8553cdef` Tile edge lists made once per compiled primitive: Primitive.tileListing kept in RetainedItem.listing, tilesOfListings assembles the words; a
- `4162bda37` Tiles and damage by a primitive's paint box: its box cut to its clips' boxes (Primitive.paintBox, ClipRect.screenBox); a zoomed path clipped
- `72dcbb58d` Per-tile stroke piece lists (issue 450, spinal-bisect: strokes on SVG text were 728 of 866 ms GPU a frame)
- `3dae7447e` Window: a heavy frame is drawn in bands of about 16 ms, so input is taken between them (issue 450)
- `580d5119d` spinal_perf.ts: stroke pieces tested per tick (tick.draw.pieces_m)
- `c9286e10d` tilesOfListings: listings as an array taken by index, no List.zip of the primitives and their listings (List.zip of 10,000 primitives overfl
- `39c96de6e` scene-work.mjs: piece lists read only from a scene whose shader has them
- `04740693f` Spinal Tap budgets: draw counts of the tile edge and piece lists and paint boxes (native edges max 700, pieces max 600, pixels a tick 400k);
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
- `9504dce9e` Mac app launcher: rotate trace.jsonl over 64 MiB at launch (#488)

