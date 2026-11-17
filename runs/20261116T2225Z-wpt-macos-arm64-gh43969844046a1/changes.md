### Since the previous full run: +174 subtests (+0.0077 points)

Previous: `20261116T1712Z-wpt-macos-arm64-gh43915829144a1`, core `1ad66797e`, 91.9984%. This run: core `cc857117d`, 92.0061%; 40 commits between.
Tests that lost subtests: 2 (-9); that gained: 75 (+183). Page outcomes: ERROR -5, NO_RESULT -20, OK +61, STALL -3, TIMEOUT -33.

**Directories that fell** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 3,922 | 2,584 | 2,576 | -8 |

**Directories that rose** (8; the first 8)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| referrer-policy | 8,815 | 4,949 | 5,029 | +80 |
| third_party/test262 | 53,833 | 45,688 | 45,718 | +30 |
| xhr | 2,344 | 1,791 | 1,819 | +28 |
| html/syntax | 8,984 | 8,656 | 8,679 | +23 |
| websockets | 2,389 | 1,246 | 1,260 | +14 |
| html/semantics | 22,381 | 15,171 | 15,176 | +5 |
| preload | 956 | 242 | 243 | +1 |
| workers | 1,598 | 703 | 704 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| webcodecs | 8 | 1 |
| xhr | 1 | 1 |

**Tests that lost most** (the first 2 of 2)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /webcodecs/image-decoder.https.any.html | 25 | 17 | 47 |
| /xhr/xhr-timeout-longtask.any.worker.html | 1 | 0 | 1 |

**Commits between** (40)

- `f2e1e546e` Incremental equals full (issue 513 item 2): inventory, statement, culling theorems
- `3c33486aa` build-web-render.sh: C compiles COMPILE_JOBS at a time; every compile command in compile-commands.txt
- `fbfa91b94` skills/foafnaut/ci-caching.md: CI jobs, caches and their keys, the cache audit, cold builds, timing records
- `cdb310373` Hub: Web platform lists Textnaut, start, demos, stress, settings, notebook, conformance; Hub copies of openly licensed pages open in place i
- `17c7b1bc9` Test results: an index page for the site toolbar's Test Results link (it answered 404)
- `19eac6182` Settings in every UI: Textnaut's s key opens a settings screen (engine build, page scripts, strictness); the Hub passes the system's dark mo
- `dae92ae22` Hub README: Hub copies, how they are made, served and added
- `3cc24f393` Chrome: a flat look by default (light and dark faces, rounded address field with a focus ring, vector line icons, settings button in a circl
- `14ba800e3` Web platform page: link the data and documents conformance page
- `86b7fea8f` Chrome: line icons 20 points and a little heavier (readable at 1x); copy licence line spacing
- `cce8aea38` Chrome: circles as 16-sided polygons, square caps and mitred joins (no curve to flatten; the flat look cost 1.5 to 3 times the classic chrom
- `6cfb23d66` Chrome: the gear is one filled shape with the hub as a hole; each icon's lines are one stroked path (at most two primitives an icon)
- `aa42acc12` Chrome: icon lines are filled quadrilaterals in one path (nonzero), not strokes
- `336905e13` Start page: a Books, texts and essays group and a Small tools group, 32 more plain sites (probed with Textnaut 0.1.4 native), 10 more Hub co
- `ddf6be714` scroll_layers_check: chrome rows apart; a sloped or round chrome edge sampled by the other rule (issue 1269) is counted as that expected fai
- `c5121e3aa` BubblePopJS: the built-in dispatchers out of the evaluator's mutual block
- `9fd90c894` Merge pull request #506 from danbri/wip/natives-out
- `3ed44ba03` realpages-survey skill: snapshots are development test inputs only; nothing derived from sites ships (#533)
- `54fa9b357` realpages-survey skill: snapshot directory cap 200 MB (#535)
- `f009bffee` Merge pull request #521 from danbri/wip/incr-equals-full
- `a9ad7c7eb` Merge pull request #527 from danbri/wip/base-href
- `c2fa4b5cd` Merge pull request #516 from danbri/wip/hub-fix
- `697f4ba31` Merge rule: Linux jobs of build.yml + premerge + theorems; macOS nightly and on main; ci-runner skill
- `ed912267f` Merge remote-tracking branch 'origin/main' into mg/ci-cache
- `8ebe34266` Merge branch 'mg/ci-cache' into mg/ci-gate
- `ebde345c9` Native engine starts Lean's task manager (capped pool); scene tile listings in parallel chunks with Par.mapChunks_eq, listingsOf_eq, listRet
- `efc4ef135` Host frame pipeline as a Lean transition system (HostPipeline.Model: reachable_inv, no_deadlock, drain, check_nil_sound); GPU waits start on
- `8e06c8fc2` dataflow inventory: directory line for Par and HostPipeline
- `fd573fef9` Engine builds: L4Factoidal.Par.Chunked in the core module lists (SVG.lean imports it)
- `8149e775c` SVG.retainItemBare_listed: state the compile step before the case split (the bind of an ok render is not reduced by cases)
- `d01b4fc45` GPU gate: each submission carries the cost of what it drew, answers count when the blocking ask returns, the loop turns when an ask is due (
- `cdac8208d` GPU gate: only asks about 4 units of work or more teach the rate (a run of scroll composites must not wear it down before a heavy frame); wo
- `cbf8dcfdf` pipeline_trace_check.ts: Spinal Tap budgets (no GPU submission without its cost; ceilings on frame p95 and on main-thread time in GPU waits)
- `c91c2dd7b` gpu_pacing_test.ts: the gate's new rules under test (no-cost work keeps its own estimate, light asks teach no rate, the machine prior before
- `c7a89c3e0` GPU gate: the machine prior is slept for at most 100 ms, an ask that found the GPU done bounds the rate, a late ask only bounds it from abov
- `94b282c74` Merge pull request #526 from danbri/wip/ci-cache
- `e436bd863` Merge pull request #536 from danbri/wip/ci-gate
- `88b2d2959` Merge pull request #490 from danbri/wip/par
- `7f6767296` Skill link for ci-runner in .claude/skills
- `cc857117d` skills: background-watchers (watchers that end: twin pgrep -f deadlock, PID waits, deadlines, CI run IDs, cleanup); brief points to it (#541

