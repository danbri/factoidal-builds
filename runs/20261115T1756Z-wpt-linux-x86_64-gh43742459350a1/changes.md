### Since the previous full run: +235 subtests (+0.0103 points)

Previous: `20261115T1703Z-wpt-linux-x86_64-gh43736681407a1`, core `6efc9cffb`, 91.8369%. This run: core `5029cc163`, 91.8472%; 4 commits between.
Tests that lost subtests: 2 (-4); that gained: 6 (+239). Page outcomes: OK -2, STALL +2.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| shadow-dom | 14,720 | 14,129 | 14,126 | -3 |
| html/dom | 72,400 | 69,541 | 69,540 | -1 |

**Directories that rose** (5; the first 5)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| selection/(root) | 33,918 | 33,432 | 33,664 | +232 |
| webcodecs | 3,922 | 2,571 | 2,574 | +3 |
| html/semantics | 22,381 | 15,153 | 15,155 | +2 |
| preload | 956 | 242 | 243 | +1 |
| service-workers | 3,262 | 1,392 | 1,393 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| shadow-dom/declarative | 3 | 1 |
| html/dom | 1 | 1 |

**Tests that lost most** (the first 2 of 2)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /shadow-dom/declarative/declarative-shadow-dom-repeats.html | 3 | 0 | 3 |
| /html/dom/documents/dom-tree-accessors/document.scripts.html | 1 | 0 | 1 |

**Commits between** (4)

- `fc04bef55` Idle window waits for the next event instead of an 8 ms poll (issue 450)
- `3a317540b` Merge pull request #464 from danbri/wip/idle-loop
- `25b30c375` textnaut sync.mjs: copy finite_floats.ts, which native_html_engine.ts imports since 3e6745f19
- `5029cc163` Merge pull request #465 from danbri/wip/textnaut-sync

