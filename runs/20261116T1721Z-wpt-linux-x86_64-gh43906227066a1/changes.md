### Since the previous full run: +603 subtests (+0.0265 points)

Previous: `20261116T1211Z-wpt-linux-x86_64-gh43864240722a1`, core `9fd90c894`, 91.9770%. This run: core `cc857117d`, 92.0036%; 43 commits between.
Tests that lost subtests: 5 (-77); that gained: 40 (+680). Page outcomes: ERROR -2, OK -1, STALL +1, TIMEOUT +2.

**Directories that fell** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| sanitizer-api | 3,816 | 2,625 | 2,562 | -63 |
| webcodecs | 3,922 | 2,584 | 2,576 | -8 |
| dom/nodes | 15,595 | 14,838 | 14,837 | -1 |

**Directories that rose** (8; the first 8)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| url | 12,437 | 11,768 | 12,356 | +588 |
| html/infrastructure | 1,664 | 918 | 979 | +61 |
| mixed-content | 2,281 | 1,296 | 1,309 | +13 |
| content-security-policy | 4,544 | 2,499 | 2,503 | +4 |
| html/semantics | 22,381 | 15,173 | 15,176 | +3 |
| xhr | 2,344 | 1,818 | 1,821 | +3 |
| service-workers | 3,262 | 1,391 | 1,393 | +2 |
| html/browsers | 3,309 | 766 | 767 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 4 directories, the first 4)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| sanitizer-api | 63 | 1 |
| webcodecs | 8 | 1 |
| dom/nodes | 5 | 2 |
| html/semantics | 1 | 1 |

**Tests that lost most** (the first 5 of 5)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /sanitizer-api/sanitizer-processing-instructions.html | 63 | 0 | 63 |
| /webcodecs/image-decoder.https.any.html | 25 | 17 | 47 |
| /dom/nodes/Document-cloneNode-about-base-url.window.html | 4 | 1 | 5 |
| /dom/nodes/Document-cloneNode-base-url-xml.window.html | 2 | 0 | 3 |
| /html/semantics/embedded-content/the-img-element/list-of-available-images-does-not-coalesce-in-flight-requests.sub.tentative.html | 1 | 0 | 1 |

**Commits between** (43)

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
- `43a97d928` Frozen base URL: <base href> set or changed by script resolves reflected URLs (url/ a-element*); BaseURL theorems, 46 guards
- `fe719a70a` Base URLs at zero cost on pages without a base: inlined idle checks, slow paths out of line, base fields in BaseURL.State; encoding prescan 
- `893901e4e` Base URLs: select again only when a change can alter the selected base (no tree walk per append on a page with a base); removals name the re
- `fa038a174` Base URLs tracked from the first use only: no base work at mutations of a page that reads no URL; changedBases out of the records so command
- `1ad66797e` Frozen base URL record: lazy tracking, gated selection, timings against main, checks
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

