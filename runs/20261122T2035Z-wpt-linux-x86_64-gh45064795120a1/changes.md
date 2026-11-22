### Since the previous full run: -1,273 subtests (-0.0560 points)

Previous: `20261122T1939Z-wpt-linux-x86_64-gh45061981963a1`, core `4618bea0c`, 92.6399%. This run: core `a512ab918`, 92.5839%; 4 commits between.
Tests that lost subtests: 2 (-1,280); that gained: 3 (+7). Page outcomes: CRASH +1, ERROR +1, OK -1, STALL -1.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| selection/(root) | 33,918 | 33,664 | 32,388 | -1,276 |
| css/css-values | 10,451 | 6,234 | 6,231 | -3 |

**Directories that rose** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 3,935 | 2,578 | 2,583 | +5 |
| IndexedDB | 5,853 | 5,503 | 5,504 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| selection | 1,276 | 1 |
| css/css-values | 4 | 1 |

**Tests that lost most** (the first 2 of 2)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /selection/addRange-32.html | 1,276 | 0 | 1,276 |
| /css/css-values/urls/fragment-only.html | 5 | 1 | 5 |

**Commits between** (4)

- `e3d6bad29` Render visible fallback glyphs for CSS control characters (#764)
- `0aae22807` Paint: images at their own size on whole pixels draw their pixels exactly
- `89ab7d931` Draw CSS background images (issue 704)
- `a512ab918` Reftest causes record: background images done, with measurements (issue 747)

