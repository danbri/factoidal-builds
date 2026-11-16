### Since the previous full run: +58 subtests (+0.0026 points)

Previous: `20261116T0857Z-wpt-macos-arm64-gh43835522545a1`, core `0ccd896a0`, 91.9560%. This run: core `6e2d79003`, 91.9586%; 18 commits between.
Tests that lost subtests: 11 (-238); that gained: 156 (+296). Page outcomes: ERROR -5, NO_RESULT -14, OK +27, STALL -1, TIMEOUT -7.

**Directories that fell** (5; the first 5)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webidl | 838 | 647 | 500 | -147 |
| streams | 5,796 | 5,313 | 5,283 | -30 |
| html/semantics | 22,381 | 15,200 | 15,189 | -11 |
| webmessaging | 304 | 153 | 150 | -3 |
| preload | 956 | 243 | 242 | -1 |

**Directories that rose** (8; the first 8)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| referrer-policy | 8,815 | 4,911 | 5,029 | +118 |
| third_party/test262 | 53,833 | 45,626 | 45,717 | +91 |
| websockets | 2,389 | 1,243 | 1,260 | +17 |
| xhr | 2,344 | 1,803 | 1,816 | +13 |
| webcodecs | 3,922 | 2,569 | 2,576 | +7 |
| subresource-integrity | 491 | 195 | 197 | +2 |
| intersection-observer | 440 | 211 | 212 | +1 |
| workers | 1,598 | 703 | 704 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 9 directories, the first 9)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| webidl | 147 | 1 |
| streams/readable-streams | 50 | 1 |
| streams/writable-streams | 14 | 1 |
| html/semantics | 11 | 2 |
| streams/piping | 9 | 1 |
| webmessaging | 3 | 1 |
| third_party/test262 | 2 | 2 |
| preload | 1 | 1 |
| xhr | 1 | 1 |

**Tests that lost most** (the first 11 of 11)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /webidl/idlharness.any.worker.html | 147 | 0 | 159 |
| /streams/readable-streams/from.any.worker.html | 50 | 0 | 50 |
| /streams/writable-streams/bad-underlying-sinks.any.worker.html | 14 | 0 | 14 |
| /html/semantics/embedded-content/the-img-element/relevant-mutations.html | 99 | 89 | 113 |
| /streams/piping/multiple-propagation.any.sharedworker.html | 9 | 0 | 9 |
| /webmessaging/Channel_postMessage_transfer_target_port.any.worker.html | 3 | 0 | 3 |
| /html/semantics/embedded-content/the-img-element/list-of-available-images-does-not-coalesce-in-flight-requests.sub.tentative.html | 1 | 0 | 1 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |
| /third_party/test262/test/built-ins/Array/prototype/Symbol.unscopables/value.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/Object/assign/strings-and-symbol-order-proxy.test262.html | 1 | 0 | 1 |
| /xhr/xhr-timeout-longtask.any.html | 1 | 0 | 1 |

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

