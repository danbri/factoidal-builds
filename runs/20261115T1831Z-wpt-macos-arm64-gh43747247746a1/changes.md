### Since the previous full run: -39 subtests (-0.0017 points)

Previous: `20261115T1500Z-wpt-macos-arm64-gh43727386818a1`, core `cc73af028`, 91.8464%. This run: core `5029cc163`, 91.8447%; 34 commits between.
Tests that lost subtests: 23 (-71); that gained: 14 (+32). Page outcomes: ERROR +6, NO_RESULT -2, OK -1, TIMEOUT -3.

**Directories that fell** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/semantics | 22,381 | 15,185 | 15,156 | -29 |
| websockets | 2,389 | 1,260 | 1,250 | -10 |
| referrer-policy | 8,815 | 4,981 | 4,978 | -3 |
| workers | 1,598 | 703 | 702 | -1 |

**Directories that rose** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 3,922 | 2,573 | 2,576 | +3 |
| xhr | 2,344 | 1,813 | 1,814 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 6 directories, the first 6)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| html/semantics | 29 | 1 |
| referrer-policy/gen | 28 | 15 |
| websockets/stream | 10 | 3 |
| referrer-policy/4K+1 | 2 | 2 |
| referrer-policy/4K-1 | 1 | 1 |
| workers/interfaces | 1 | 1 |

**Tests that lost most** (the first 23 of 23)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /html/semantics/embedded-content/the-img-element/relevant-mutations.html | 103 | 74 | 113 |
| /websockets/stream/tentative/constructor.any.worker.html?wss | 5 | 0 | 8 |
| /websockets/stream/tentative/abort.any.worker.html?wss | 4 | 0 | 5 |
| /referrer-policy/gen/srcdoc-inherit.meta/default/worker-module.http.html | 2 | 0 | 2 |
| /referrer-policy/gen/srcdoc-inherit.meta/never/worker-module.http.html | 2 | 0 | 2 |
| /referrer-policy/gen/srcdoc-inherit.meta/no-referrer/worker-module.http.html | 2 | 0 | 2 |
| /referrer-policy/gen/srcdoc-inherit.meta/origin-when-crossorigin/worker-module.http.html | 2 | 0 | 2 |
| /referrer-policy/gen/srcdoc-inherit.meta/origin/worker-module.http.html | 2 | 0 | 2 |
| /referrer-policy/gen/srcdoc-inherit.meta/strict-origin/worker-module.http.html | 2 | 0 | 2 |
| /referrer-policy/gen/srcdoc-inherit.meta/unset/worker-module.http.html | 2 | 0 | 2 |
| /referrer-policy/gen/srcdoc.meta/default/worker-module.http.html | 2 | 0 | 2 |
| /referrer-policy/gen/srcdoc.meta/never/worker-module.http.html | 2 | 0 | 2 |
| /referrer-policy/gen/srcdoc.meta/no-referrer-when-downgrade/worker-module.http.html | 2 | 0 | 2 |
| /referrer-policy/gen/srcdoc.meta/no-referrer/worker-module.http.html | 2 | 0 | 2 |
| /referrer-policy/gen/srcdoc.meta/origin-when-cross-origin/worker-module.http.html | 2 | 0 | 2 |
| /referrer-policy/gen/worker-module.http-rp/no-referrer-when-downgrade/fetch.http.html | 12 | 10 | 12 |
| /referrer-policy/4K+1/gen/top.meta/origin-when-cross-origin/xhr.http.html | 2 | 1 | 2 |
| /referrer-policy/4K+1/gen/top.meta/unset/xhr.http.html | 1 | 0 | 2 |
| /referrer-policy/4K-1/gen/top.http-rp/strict-origin-when-cross-origin/xhr.http.html | 1 | 0 | 2 |
| /referrer-policy/gen/req.attr/origin-when-cross-origin/script-tag.http.html | 2 | 1 | 12 |
| /referrer-policy/gen/srcdoc-inherit.http-rp/same-origin/worker-module.http.html | 2 | 1 | 2 |
| /websockets/stream/tentative/close.any.sharedworker.html?wpt_flags=h2 | 1 | 0 | 27 |
| /workers/interfaces/WorkerUtils/importScripts/report-error-cross-origin.sub.any.sharedworker.html | 1 | 0 | 4 |

**Commits between** (34)

- `3c3ae4d2c` Hub: Textnaut page and an engine-drawn notebook (wip)
- `644d470db` Hub notebook: anonymous cells return their output; SVG chart in hex colours (the engine refuses space-separated hsl() in an SVG fill and dra
- `265e4318e` Textnaut grid: shaped glyphs no longer paint cell backgrounds
- `b88340231` Merge pull request #456 from danbri/wip/hub-notebook
- `12ec31442` tools/premerge.sh: the cheap CI checks before a push to main, every failure listed at the end
- `b75785156` CI: F* workflows run only by hand
- `d4623deb0` Merge pull request #457 from danbri/wip/premerge
- `7541db440` fast-verify-extract skill: the CI F* caches serve manual runs only
- `dd2a6dfd6` Spinal Tap page as a budgeted test, native and Hub (issue 450)
- `6d452df0d` Hub: a script turn's frame is layered, one rule for every host (issue 450)
- `387a539dc` Draw cost of a zoomed SVG: measured per frame, and the scene shader skips a clipped record's geometry (issue 450)
- `7924732ed` scene-work.mjs: count edges as the scene's own shader walks them (a shader that skips a clipped record does not walk its edges there)
- `9c83819b4` Hub draw split per frame: composite, chrome, plans and pipelines; budgets for the draw counts (issue 450)
- `b4bcecec8` test.sh: spinal_perf_check.ts through check(), as every other check
- `3e6745f19` Finite-float checks in a loop, not every(): 7.6 of 11 ms of an unchanged frame (issue 450)
- `bcc551039` Merge pull request #461 from danbri/wip/no-fstar
- `e98d545ed` Spinal Tap page taken apart: 25 variants, engine and window, feature against added cost (issue 450)
- `e4406808e` spinal_bisect_check.ts in test.sh; budgets from the fast run; SKILL.md; CPU samples of an exited window ignored (issue 450)
- `173c907d0` spinal_bisect.ts: type check clean
- `1a2ddd3c4` Merge pull request #460 from danbri/wip/finite-check
- `074c2aa4d` Merge pull request #462 from danbri/wip/spinal-bisect
- `fc04bef55` Idle window waits for the next event instead of an 8 ms poll (issue 450)
- `05ebe0cd7` Linux libweb-render.so needs no Lean toolchain at run time
- `63f2caee0` Textnaut: --install-native installs the Linux engine; engine_parity.py compares native and Wasm
- `289d29896` Textnaut: --install-native TAG installs that release, if it is self-contained
- `f25d2f899` Textnaut docs: the native engine on Linux; engine_parity.py: several links for Tab, blank grids compare
- `ec6a312d4` build-leanrt-no-gmp.sh (Linux): hidden __isoc23_* forwarders, so the library links against the toolchain's older glibc
- `06d899e03` textnaut sync.mjs: skip a __pycache__ directory left by the Python checks
- `84d5a5ac9` engine_parity.py: read the terminal while textnaut quits, kill its process group, bound the quiet wait, print each key time and the terminal
- `1dbca74ce` engine_parity.py: read the top bar without colour escapes (24-bit gradient splits the words)
- `6efc9cffb` Merge pull request #463 from danbri/wip/linux-native
- `3a317540b` Merge pull request #464 from danbri/wip/idle-loop
- `25b30c375` textnaut sync.mjs: copy finite_floats.ts, which native_html_engine.ts imports since 3e6745f19
- `5029cc163` Merge pull request #465 from danbri/wip/textnaut-sync

