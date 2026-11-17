### Since the previous full run: +315 subtests (+0.0139 points)

Previous: `20261117T1519Z-wpt-linux-x86_64-gh44112973310a1`, core `528b04055`, 92.4634%. This run: core `a5f53231e`, 92.4773%; 7 commits between.
Tests that lost subtests: 1 (-3); that gained: 24 (+318). Page outcomes: OK +1, STALL -2, TIMEOUT +1.

**Directories that fell** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| shadow-dom | 14,720 | 14,129 | 14,126 | -3 |

**Directories that rose** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/semantics | 22,381 | 15,191 | 15,478 | +287 |
| html/rendering | 11,705 | 10,054 | 10,083 | +29 |
| IndexedDB | 5,853 | 5,503 | 5,504 | +1 |
| webcodecs | 3,922 | 2,571 | 2,572 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 1 directories, the first 1)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| shadow-dom/declarative | 3 | 1 |

**Tests that lost most** (the first 1 of 1)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /shadow-dom/declarative/declarative-shadow-dom-repeats.html | 3 | 0 | 3 |

**Commits between** (7)

- `cefa638a7` Style: align attributes map to text-align; th centred; bgcolor on row groups; table bordercolor
- `7f43e1fa9` alignHints_other: prove by rewriting the guard
- `a21c49ce9` alignHints_other: simp only, so contains stays a Bool
- `d858d907d` Forms: input value modes and the dirty value flag (HTML 4.10.5)
- `f133de544` Forms: a clone of an input takes its indeterminateness (HTML 4.10.5 cloning steps)
- `19f13304e` Merge pull request #595 from danbri/wip/wptbulk4-align
- `a5f53231e` Merge pull request #597 from danbri/wip/wptbulk4-value

