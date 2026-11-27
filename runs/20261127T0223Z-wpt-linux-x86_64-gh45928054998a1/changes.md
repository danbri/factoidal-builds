### Since the previous full run: -1 subtests (-0.0000 points)

Previous: `20261126T2325Z-wpt-linux-x86_64-gh45909899695a1`, core `b70f732cd`, 92.7761%. This run: core `b70f732cd`, 92.7761% (the same commit: the difference is flakiness).
Tests that lost subtests: 3 (-3); that gained: 2 (+2). Page outcomes: STALL +1, TIMEOUT -1.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/semantics | 22,535 | 15,745 | 15,744 | -1 |
| secure-contexts | 86 | 14 | 13 | -1 |

**Directories that rose** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| preload | 956 | 242 | 243 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 3 directories, the first 3)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| html/semantics | 1 | 1 |
| secure-contexts | 1 | 1 |
| third_party/test262 | 1 | 1 |

**Tests that lost most** (the first 3 of 3)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /html/semantics/embedded-content/the-img-element/list-of-available-images-does-not-coalesce-in-flight-requests.sub.tentative.html | 1 | 0 | 1 |
| /secure-contexts/basic-shared-worker.html | 1 | 0 | 5 |
| /third_party/test262/test/built-ins/Temporal/PlainYearMonth/prototype/era/basic.test262.html | 1 | 0 | 1 |

