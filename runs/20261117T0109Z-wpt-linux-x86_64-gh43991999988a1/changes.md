### Since the previous full run: -1 subtests (-0.0000 points)

Previous: `20261117T0014Z-wpt-linux-x86_64-gh43985987467a1`, core `696f967ab`, 92.0323%. This run: core `094a8d872`, 92.0323%; 2 commits between.
Tests that lost subtests: 4 (-17); that gained: 1 (+16). Page outcomes: ERROR +3, NO_RESULT +1, OK -2, TIMEOUT -2.

**Directories that fell** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| referrer-policy | 8,815 | 5,029 | 5,021 | -8 |
| webcodecs | 3,922 | 2,584 | 2,577 | -7 |
| fetch | 13,288 | 8,821 | 8,820 | -1 |
| service-workers | 3,262 | 1,393 | 1,392 | -1 |

**Directories that rose** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/webappapis | 3,674 | 3,017 | 3,033 | +16 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 4 directories, the first 4)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| referrer-policy/gen | 8 | 1 |
| webcodecs | 7 | 1 |
| fetch/metadata | 1 | 1 |
| service-workers/service-worker | 1 | 1 |

**Tests that lost most** (the first 4 of 4)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /referrer-policy/gen/iframe.http-rp/origin-when-cross-origin/script-tag.http.html | 10 | 2 | 12 |
| /webcodecs/image-decoder.https.any.html | 25 | 18 | 47 |
| /fetch/metadata/generated/element-img.https.sub.html | 18 | 17 | 45 |
| /service-workers/service-worker/worker-in-sandboxed-iframe-by-csp-fetch-event.https.html | 1 | 0 | 5 |

**Commits between** (2)

- `58ce03cab` Lean memory-management overhead: analysis record, idiom and steering microbenchmarks, opt-in ThinLTO of the native engine with the runtime's
- `094a8d872` Merge pull request #559 from danbri/wip/leanmem

