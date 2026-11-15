### Since the previous full run: +8 subtests (+0.0004 points)

Previous: `20261115T1513Z-wpt-linux-x86_64-gh43728700893a1`, core `cc73af028`, 91.8474%. This run: core `b4bcecec8`, 91.8477%; 12 commits between.
Tests that lost subtests: 0 (-0); that gained: 3 (+8). Page outcomes: unchanged.

**Directories that rose** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 3,922 | 2,578 | 2,584 | +6 |
| html/semantics | 22,381 | 15,154 | 15,155 | +1 |
| preload | 956 | 242 | 243 | +1 |

**Commits between** (12)

- `3c3ae4d2c` Hub: Textnaut page and an engine-drawn notebook (wip)
- `644d470db` Hub notebook: anonymous cells return their output; SVG chart in hex colours (the engine refuses space-separated hsl() in an SVG fill and dra
- `265e4318e` Textnaut grid: shaped glyphs no longer paint cell backgrounds
- `b88340231` Merge pull request #456 from danbri/wip/hub-notebook
- `12ec31442` tools/premerge.sh: the cheap CI checks before a push to main, every failure listed at the end
- `d4623deb0` Merge pull request #457 from danbri/wip/premerge
- `dd2a6dfd6` Spinal Tap page as a budgeted test, native and Hub (issue 450)
- `6d452df0d` Hub: a script turn's frame is layered, one rule for every host (issue 450)
- `387a539dc` Draw cost of a zoomed SVG: measured per frame, and the scene shader skips a clipped record's geometry (issue 450)
- `7924732ed` scene-work.mjs: count edges as the scene's own shader walks them (a shader that skips a clipped record does not walk its edges there)
- `9c83819b4` Hub draw split per frame: composite, chrome, plans and pipelines; budgets for the draw counts (issue 450)
- `b4bcecec8` test.sh: spinal_perf_check.ts through check(), as every other check

