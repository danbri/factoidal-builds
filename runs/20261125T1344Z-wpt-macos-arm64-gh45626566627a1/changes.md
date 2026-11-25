### Since the previous full run: +25 subtests (+0.0011 points)

Previous: `20261125T0713Z-wpt-macos-arm64-gh45566389685a1`, core `dd387abb3`, 92.6337%. This run: core `e4445d147`, 92.6348%; 4 commits between.
Tests that lost subtests: 4 (-5); that gained: 6 (+30). Page outcomes: ERROR -1, STALL +1.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 4,168 | 2,640 | 2,638 | -2 |
| IndexedDB | 5,853 | 5,504 | 5,503 | -1 |

**Directories that rose** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/css-borders | 4,906 | 4,358 | 4,375 | +17 |
| workers | 1,598 | 708 | 716 | +8 |
| webrtc-stats | 338 | 0 | 2 | +2 |
| xhr | 2,344 | 1,832 | 1,833 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 4 directories, the first 4)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| webcodecs | 2 | 1 |
| IndexedDB | 1 | 1 |
| css/css-borders | 1 | 1 |
| third_party/test262 | 1 | 1 |

**Tests that lost most** (the first 4 of 4)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /webcodecs/image-decoder.https.any.html | 12 | 10 | 47 |
| /IndexedDB/interleaved-cursors-large.any.html | 1 | 0 | 1 |
| /css/css-borders/border-radius-shorthand.html | 2 | 1 | 3 |
| /third_party/test262/test/language/expressions/async-generator/early-errors-expression-eval-in-formal-parameters.test262.strict.html | 1 | 0 | 1 |

**Commits between** (4)

- `15bbd9edd` CPU SVG raster: count path edges once, unboxed pixel loop, constant paint rows (issue 871)
- `3eb43998f` CPU SVG raster: leave out the test of a paint whose alpha is exactly 0 (issue 871)
- `58e31103e` CPU SVG raster: plain-code dash piece tests, pieces culled by pixel row (issue 871)
- `e4445d147` Paint rounded CSS backgrounds and bitmap content (#994)

