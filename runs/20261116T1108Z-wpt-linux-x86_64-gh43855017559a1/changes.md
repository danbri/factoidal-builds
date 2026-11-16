### Since the previous full run: -2 subtests (-0.0001 points)

Previous: `20261116T1016Z-wpt-linux-x86_64-gh43847381345a1`, core `0391fe0d0`, 91.9774%. This run: core `0b1e2a908`, 91.9773%; 13 commits between.
Tests that lost subtests: 2 (-9); that gained: 2 (+7). Page outcomes: CRASH -1, OK +2, TIMEOUT -1.

**Directories that fell** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| shadow-dom | 14,720 | 14,129 | 14,120 | -9 |

**Directories that rose** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 3,922 | 2,578 | 2,584 | +6 |
| html/semantics | 22,381 | 15,171 | 15,172 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| shadow-dom | 6 | 1 |
| shadow-dom/declarative | 3 | 1 |

**Tests that lost most** (the first 2 of 2)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /shadow-dom/Element-interface-attachShadow.html | 6 | 0 | 6 |
| /shadow-dom/declarative/declarative-shadow-dom-repeats.html | 3 | 0 | 3 |

**Commits between** (13)

- `08bb40f3e` BubblePopJS script clock at its own rate (500 steps a ms, LeanJS.stepsPerMs), not QuickJS's 100000 instructions a ms
- `8376beed3` Real pages: sliced timer turns, input and scroll first, resumable start, JPEG fast Float.ofNat, cascade skips the table for properties apply
- `1a4323ac0` Proof fixes (setter lemmas, advanceUntil_never), scroll first holds a change made while the first frame is made, frame trace says why
- `13901383d` Start: the parse of a page that waits for module answers is kept for the next attempt (startParsed)
- `3475667a3` WebScripts: doc comment order, no keyword as a name
- `9bbe06dcd` run_html: timers held while a scroll holds a page change; --no-scroll-first and --no-input-first for comparison
- `5efbc58c2` Timeline moves at frames while an animation runs (Host.tickTask, tickTask_running): with the script clock at its own rate a long start no lo
- `657f81d25` Start: the prelude's scan for event handler content attributes reads only the elements that have an on... attribute (node_query 168, eventHa
- `d6d463db2` page-load: optional fields of inputFirst and scrollFirst (deno check)
- `724b00981` Scripts: the undo of a sync request is bounded by the heap (keepsUndo, undoHeapLimit)
- `fd53dac77` Native engine: compiled Lean code counts no heartbeat at each allocation (lean_no_heartbeat.h)
- `adb9da315` Window loop: wait for a page's next timer instead of pumping between its turns
- `0b1e2a908` Merge PRs #501, #510, #515: real pages fast and calm (sliced timer turns, input and scroll first, resumable start; bounded undo of sync requ

