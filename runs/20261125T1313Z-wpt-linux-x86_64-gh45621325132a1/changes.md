### Since the previous full run: +7 subtests (+0.0003 points)

Previous: `20261125T0547Z-wpt-linux-x86_64-gh45550312037a1`, core `dd387abb3`, 92.6333%. This run: core `e4445d147`, 92.6336%; 4 commits between.
Tests that lost subtests: 3 (-29); that gained: 6 (+36). Page outcomes: ERROR +1, OK +1, STALL -1, TIMEOUT -1.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/dom | 72,463 | 69,929 | 69,902 | -27 |
| html/semantics | 22,498 | 15,589 | 15,588 | -1 |

**Directories that rose** (5; the first 5)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/css-borders | 4,906 | 4,358 | 4,375 | +17 |
| mixed-content | 2,281 | 1,311 | 1,319 | +8 |
| webcodecs | 4,168 | 2,637 | 2,644 | +7 |
| service-workers | 3,267 | 1,390 | 1,392 | +2 |
| IndexedDB | 5,853 | 5,503 | 5,504 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 3 directories, the first 3)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| html/dom | 27 | 1 |
| css/css-borders | 1 | 1 |
| html/semantics | 1 | 1 |

**Tests that lost most** (the first 3 of 3)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /html/dom/aria-element-reflection.html | 27 | 0 | 27 |
| /css/css-borders/border-radius-shorthand.html | 2 | 1 | 3 |
| /html/semantics/embedded-content/the-img-element/list-of-available-images-does-not-coalesce-in-flight-requests.sub.tentative.html | 1 | 0 | 1 |

**Commits between** (4)

- `15bbd9edd` CPU SVG raster: count path edges once, unboxed pixel loop, constant paint rows (issue 871)
- `3eb43998f` CPU SVG raster: leave out the test of a paint whose alpha is exactly 0 (issue 871)
- `58e31103e` CPU SVG raster: plain-code dash piece tests, pieces culled by pixel row (issue 871)
- `e4445d147` Paint rounded CSS backgrounds and bitmap content (#994)

