### Since the previous full run: +2 subtests (+0.0001 points)

Previous: `20261116T2225Z-wpt-macos-arm64-gh43969844046a1`, core `cc857117d`, 92.0061%. This run: core `0137191ed`, 92.0062%; 4 commits between.
Tests that lost subtests: 0 (-0); that gained: 2 (+2). Page outcomes: NO_RESULT -1, OK -2, STALL +3.

**Directories that rose** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/semantics | 22,381 | 15,176 | 15,177 | +1 |
| webcodecs | 3,922 | 2,576 | 2,577 | +1 |

**Commits between** (4)

- `47c19ac05` BubblePopJS heap: measured allocation baseline, design record and counting instruments
- `0df197c3b` bubblepop_perf/alloc: build-count.sh can also make a plain -O3 leanjs from the same generated C
- `2ffeb7bdf` BubblePopJS RegExp matcher: a character read allocates nothing; no continuation for a first term that fails
- `0137191ed` Merge pull request #538 from danbri/wip/heap-design

