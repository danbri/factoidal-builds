### Since the previous full run: -7 subtests (-0.0003 points)

Previous: `20261116T1108Z-wpt-linux-x86_64-gh43855017559a1`, core `0b1e2a908`, 91.9773%. This run: core `9fd90c894`, 91.9770%; 2 commits between.
Tests that lost subtests: 5 (-15); that gained: 3 (+8). Page outcomes: ERROR +2, OK -1, TIMEOUT -1.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| mixed-content | 2,281 | 1,309 | 1,296 | -13 |
| service-workers | 3,262 | 1,393 | 1,391 | -2 |

**Directories that rose** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| shadow-dom | 14,720 | 14,120 | 14,126 | +6 |
| html/semantics | 22,381 | 15,172 | 15,173 | +1 |
| preload | 956 | 242 | 243 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| mixed-content/gen | 13 | 4 |
| service-workers/cache-storage | 2 | 1 |

**Tests that lost most** (the first 5 of 5)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /mixed-content/gen/iframe-inherit.meta/unset/worklet-paint-import-data.https.html | 6 | 0 | 8 |
| /mixed-content/gen/iframe-inherit.meta/opt-in/worklet-animation-import-data.https.html | 4 | 0 | 5 |
| /mixed-content/gen/srcdoc-inherit.http-rp/opt-in/img-tag.https.html | 2 | 0 | 8 |
| /service-workers/cache-storage/cache-abort.https.any.serviceworker.html | 9 | 7 | 9 |
| /mixed-content/gen/srcdoc-inherit.meta/opt-in/script-tag.https.html | 5 | 4 | 5 |

**Commits between** (2)

- `c5121e3aa` BubblePopJS: the built-in dispatchers out of the evaluator's mutual block
- `9fd90c894` Merge pull request #506 from danbri/wip/natives-out

