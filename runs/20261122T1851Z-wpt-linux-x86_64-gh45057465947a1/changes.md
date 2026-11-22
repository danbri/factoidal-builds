### Since the previous full run: +1,330 subtests (+0.0585 points)

Previous: `20261122T1749Z-wpt-linux-x86_64-gh45051599967a1`, core `b9f6c92bd`, 92.5664%. This run: core `bbcf55b00`, 92.6249%; 1 commits between.
Tests that lost subtests: 1 (-1); that gained: 5 (+1,331). Page outcomes: CRASH +1, OK +1, STALL -2.

**Directories that fell** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| IndexedDB | 5,853 | 5,504 | 5,503 | -1 |

**Directories that rose** (5; the first 5)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| selection/(root) | 33,918 | 32,388 | 33,664 | +1,276 |
| resource-timing | 1,220 | 68 | 115 | +47 |
| webcodecs | 3,935 | 2,578 | 2,584 | +6 |
| fetch | 13,290 | 8,807 | 8,808 | +1 |
| mixed-content | 2,281 | 1,318 | 1,319 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 1 directories, the first 1)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| IndexedDB | 1 | 1 |

**Tests that lost most** (the first 1 of 1)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /IndexedDB/interleaved-cursors-large.any.html | 1 | 0 | 1 |

**Commits between** (1)

- `bbcf55b00` Keep vertical-align from shifting out-of-flow text (#762)

