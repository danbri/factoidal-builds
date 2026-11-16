### Since the previous full run: +56 subtests (+0.0025 points)

Previous: `20261116T0833Z-wpt-linux-x86_64-gh43832195994a1`, core `0ccd896a0`, 91.9745%. This run: core `6e2d79003`, 91.9770%; 18 commits between.
Tests that lost subtests: 4 (-16); that gained: 72 (+72). Page outcomes: ERROR +1, OK -2, STALL -1, TIMEOUT +2.

**Directories that fell** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 3,922 | 2,584 | 2,571 | -13 |
| fetch | 13,288 | 8,817 | 8,816 | -1 |
| html/semantics | 22,381 | 15,172 | 15,171 | -1 |
| service-workers | 3,262 | 1,393 | 1,392 | -1 |

**Directories that rose** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| third_party/test262 | 53,833 | 45,647 | 45,718 | +71 |
| preload | 956 | 242 | 243 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 4 directories, the first 4)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| webcodecs | 13 | 1 |
| fetch/metadata | 1 | 1 |
| html/semantics | 1 | 1 |
| service-workers/cache-storage | 1 | 1 |

**Tests that lost most** (the first 4 of 4)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /webcodecs/image-decoder.https.any.html | 25 | 12 | 47 |
| /fetch/metadata/generated/element-img.https.sub.html | 18 | 17 | 45 |
| /html/semantics/embedded-content/the-img-element/list-of-available-images-does-not-coalesce-in-flight-requests.sub.tentative.html | 1 | 0 | 1 |
| /service-workers/cache-storage/cache-abort.https.any.serviceworker.html | 9 | 8 | 9 |

**Commits between** (18)

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

