### Since the previous full run: +6 subtests (+0.0003 points)

Previous: `20261116T1523Z-wpt-linux-x86_64-gh43889852346a1`, core `ddf6be714`, 91.9776%. This run: core `c5121e3aa`, 91.9779%; 1 commits between.
Tests that lost subtests: 2 (-9); that gained: 4 (+15). Page outcomes: OK +1, STALL +1, TIMEOUT -2.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/semantics | 22,381 | 15,180 | 15,173 | -7 |
| fetch | 13,288 | 8,817 | 8,816 | -1 |

**Directories that rose** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 3,922 | 2,576 | 2,584 | +8 |
| resource-timing | 1,207 | 19 | 24 | +5 |
| html/rendering | 11,705 | 8,791 | 8,792 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| html/semantics | 8 | 1 |
| fetch/metadata | 1 | 1 |

**Tests that lost most** (the first 2 of 2)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /html/semantics/embedded-content/the-img-element/relevant-mutations.html | 80 | 72 | 113 |
| /fetch/metadata/generated/element-img.https.sub.html | 18 | 17 | 45 |

**Commits between** (1)

- `c5121e3aa` BubblePopJS: the built-in dispatchers out of the evaluator's mutual block

