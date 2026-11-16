### Since the previous full run: +66 subtests (+0.0029 points)

Previous: `20261116T0833Z-wpt-linux-x86_64-gh43832195994a1`, core `0ccd896a0`, 91.9745%. This run: core `0391fe0d0`, 91.9774%; 19 commits between.
Tests that lost subtests: 3 (-8); that gained: 72 (+74). Page outcomes: OK -2, STALL -2, TIMEOUT +4.

**Directories that fell** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 3,922 | 2,584 | 2,578 | -6 |
| fetch | 13,288 | 8,817 | 8,816 | -1 |
| html/semantics | 22,381 | 15,172 | 15,171 | -1 |

**Directories that rose** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| third_party/test262 | 53,833 | 45,647 | 45,718 | +71 |
| shadow-dom | 14,720 | 14,126 | 14,129 | +3 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 3 directories, the first 3)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| webcodecs | 6 | 1 |
| fetch/metadata | 1 | 1 |
| html/semantics | 1 | 1 |

**Tests that lost most** (the first 3 of 3)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /webcodecs/image-decoder.https.any.html | 25 | 19 | 47 |
| /fetch/metadata/generated/element-img.https.sub.html | 18 | 17 | 45 |
| /html/semantics/embedded-content/the-img-element/list-of-available-images-does-not-coalesce-in-flight-requests.sub.tentative.html | 1 | 0 | 1 |

**Commits between** (19)

- `c0cf1cdac` BubblePopJS: Array sort and splice on any object (SortIndexedProperties, §23.1.3.31), the comparator check; JSON.parse reviver (InternalizeJ
- `15ff386db` BubblePopJS: JSON.parse reviver context with the source of unmodified primitives
- `787ea172c` Tail-recursion allow lines: arraySpliceGeneric, deleteProp
- `2bfc1218c` jsonSources: walk the list
- `7ac0f3094` Merge main into wip/t262-builtins-3
- `0d1d3f609` Merge main into wip/t262-builtins-3
- `f9eff8909` Origin isolation: model, statement and lemma plan (theorem pipeline item 1, scoping)
- `3c4b2e6f3` Add primary code zones and static dependency analysis
- `ceea71927` Document theorem workflow and inspect code-zone boundaries
- `7d2d37940` Record measured zone dependencies and theorem candidates
- `3ab56a754` Record code-zone verification results
- `113236673` Merge pull request #517 from danbri/wip/code-zones
- `dc4d60910` Origin isolation record: result of the standalone check of the unwinding theorem
- `008727680` Merge pull request #519 from danbri/wip/origin-isolation
- `71d503e4b` Skill links for code-zones and theorem-pipeline in .claude/skills
- `dbbb4bb32` Merge pull request #507 from danbri/wip/t262-builtins-3
- `af5642d54` WPT and Test262 records: runs not counted shown on the Hub with their reason; wpt-runs skill: how shard and run failures are recorded
- `6e2d79003` Merge pull request #509 from danbri/wip/wpt-robust-records
- `0391fe0d0` realpages: add nature-telemetry, infobomb, w3c-maxf to the survey (#528)

