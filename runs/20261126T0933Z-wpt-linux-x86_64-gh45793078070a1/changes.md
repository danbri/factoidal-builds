### Since the previous full run: +40 subtests (+0.0018 points)

Previous: `20261126T0450Z-wpt-linux-x86_64-gh45753184456a1`, core `21a8f7532`, 92.6628%. This run: core `547af47fc`, 92.6645%; 31 commits between.
Tests that lost subtests: 2 (-2); that gained: 2 (+42). Page outcomes: CRASH +1, OK +2, STALL -3.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/semantics | 22,523 | 15,752 | 15,751 | -1 |
| preload | 956 | 243 | 242 | -1 |

**Directories that rose** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/dom | 72,476 | 69,895 | 69,936 | +41 |
| third_party/test262 | 53,838 | 46,355 | 46,356 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| html/semantics | 1 | 1 |
| preload | 1 | 1 |

**Tests that lost most** (the first 2 of 2)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /html/semantics/embedded-content/the-img-element/list-of-available-images-does-not-coalesce-in-flight-requests.sub.tentative.html | 1 | 0 | 1 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |

**Commits between** (31)

- `f957d56f6` Foafnaut: fill edge ends of the tile listing as one array pass (issue 1124)
- `7111c6c24` Canvas 2D: the run scan of rleRangeInto compares two pixels per 8-byte load; receiver checks with no optional chain (issue 1098)
- `14bc1cf1c` Canvas 2D host: unrle reads each run's pixel with a DataView and the replay reuses one output buffer (issue 1098)
- `9cf548be4` Design record 2026-11-26-canvas-upload-and-call-cost: the night's later steps and their measurements (issue 1098)
- `2bb5bee23` CSS matching: ancestor filter (a bit set of ancestor keys per element) refuses selectors whose ancestor keys are absent, before any walk
- `ce29f87c0` Ancestor filter: an element also gives the lower-case form of its name (an HTML element named with capitals by createElementNS)
- `7285ab374` Ancestor filter: proof of ownOf coverage follows the extra lower-case name entry
- `861c0f1ad` BubblePopJS fuel monotonicity: callBody takes the argument count (repair of 068b8b4b0, issue 1098)
- `559284f82` Foafnaut engine sessions: inventory of the native engine's global state (stage 1, issue 1031)
- `0575d4b54` Foafnaut engine sessions: engine state per session in one library, and a session on its own Lean task (stages 2 and 3, issue 1031; not yet b
- `42de5f9e3` Foafnaut engine sessions: cancel a task session (stage 4), measurement driver, fixes (issue 1031)
- `a26d3409f` Foafnaut engine sessions: the first task session starts the runtime through nonblocking FFI; record of stage 4 (issue 1031)
- `92c7adf80` Foafnaut engine sessions: the library stays loaded from the first task session (issue 1031)
- `37f1222bc` Foafnaut: an engine session per tab on its own Lean task is the default (issue 1031)
- `c5c727aff` Foafnaut engine sessions: test that a task session decodes layout sections (issue 1031)
- `37fc3a0a9` Foafnaut engine sessions record: section 6a, the rebase onto main b7286ac7 and the tests of the merged build (issue 1031)
- `dda771bf6` Foafnaut engine sessions record: byte comparison with main b7286ac7; D2 counts as measured (issue 1031)
- `728a0e5a2` Foafnaut engine sessions: confirmation against main b7286ac7; new tab first frame measured on every tab (issue 1031)
- `85c0505d6` Foafnaut host: name a held page answer only for the document on screen (issues 1124, 1031)
- `797a8bfb7` Foafnaut SVG.lean: edgeYs takes NativeSVGPath.LinearContour, so the lab builds again (issue 1124)
- `a9e39faf0` Foafnaut engine sessions record: section 6b, the rebase onto main 7285ab37, D13 (issues 1031, 1124)
- `78dad01f7` Foafnaut engine sessions: copies stays the default engine mode; tasks and sessions are options (issue 1031)
- `6d51c25c7` BubblePopJS: a new ArrayBuffer's bytes are pushed into one array, not made as an array of boxed values (issue 1098)
- `f2100d239` BubblePopJS: TypedArray.prototype.set of Numbers in one write; skills/foafnaut: check the fuel proofs after an interpreter change (issue 109
- `8010aa5f9` Design record 2026-11-26-canvas-upload-and-call-cost: the zeroed-buffer and set steps, and the fuel-proof error of the night (issue 1098)
- `9283a644e` Tail-recursion allow list: three CSS ancestor filter functions, pending issue 1157
- `023a9ce12` @factoidal/core 0.38.0: first publication of the 0.37.3 changes, engine of 2026-11-26
- `30e4290e1` CSS ancestor filter and GPU resident set: loops proved equal by @[csimp] (issues 1157, 398)
- `48aa98e60` CLAUDE.md: owner input on engine per tab (pool Deno workers; steady state weighs more than first frame)
- `cbb2db235` Foafnaut engine sessions: steady-state scenarios with 5, 20 and 50 tabs (issue 1031)
- `547af47fc` Foafnaut: --hidden-tabs stopped|throttled|running; steady scenarios wait for each page (issue 1031)

