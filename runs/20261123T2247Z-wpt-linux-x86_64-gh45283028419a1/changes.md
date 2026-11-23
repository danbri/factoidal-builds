### Since the previous full run: -47 subtests (-0.0021 points)

Previous: `20261123T1113Z-wpt-linux-x86_64-gh45163124084a1`, core `97b52ad1e`, 92.6353%. This run: core `c6ab4a477`, 92.6332%; 11 commits between.
Tests that lost subtests: 10 (-52); that gained: 3 (+5). Page outcomes: OK +2, STALL -2.

**Directories that fell** (6; the first 6)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/css-pseudo | 903 | 505 | 468 | -37 |
| webcodecs | 3,974 | 2,613 | 2,608 | -5 |
| css/selectors | 6,266 | 5,723 | 5,719 | -4 |
| css/css-conditional | 3,298 | 2,238 | 2,236 | -2 |
| css/css-shadow | 377 | 242 | 241 | -1 |
| preload | 956 | 243 | 242 | -1 |

**Directories that rose** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/dom | 72,439 | 69,926 | 69,928 | +2 |
| css/css-grid | 16,018 | 11,273 | 11,274 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 6 directories, the first 6)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| css/css-pseudo | 39 | 1 |
| webcodecs | 5 | 1 |
| css/selectors | 4 | 4 |
| css/css-conditional | 2 | 2 |
| css/css-shadow | 1 | 1 |
| preload | 1 | 1 |

**Tests that lost most** (the first 10 of 10)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /css/css-pseudo/first-letter-allowed-properties.html | 44 | 5 | 45 |
| /webcodecs/image-decoder.https.any.html | 13 | 8 | 47 |
| /css/css-conditional/container-queries/pseudo-elements-004.html | 6 | 5 | 12 |
| /css/css-conditional/container-queries/pseudo-elements-007.html | 6 | 5 | 12 |
| /css/css-shadow/part/pseudo-elements-after-part.html | 29 | 28 | 44 |
| /css/selectors/old-tests/css3-modsel-39.xml | 1 | 0 | 1 |
| /css/selectors/old-tests/css3-modsel-39a.xml | 1 | 0 | 1 |
| /css/selectors/old-tests/css3-modsel-39b.xml | 1 | 0 | 1 |
| /css/selectors/old-tests/css3-modsel-39c.xml | 1 | 0 | 1 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |

**Commits between** (11)

- `4448a9b9f` Record the 2026-11-23 crypto deferrals: AES-192, P-384/P-521 key agreement; AES on emulators open
- `7b320d564` Rendering: ::first-letter (CSS Pseudo-Elements 4 §2.3), not yet measured
- `5aa6b123c` Rendering: ::first-letter not after a block child, not after a preserved line feed, not in cursive scripts
- `fd28e39ce` Rendering: ::first-letter keeps Arabic punctuation around a Latin letter
- `065b7d75c` Rendering: background-size by the default sizing algorithm, with the natural size of SVG images; not yet measured
- `6fad5a463` Foafnaut: SVG background images drawn again at their tile size when shown larger; ratio from width and height first
- `49cfdc05f` Foafnaut: SVG img pictures drawn again at the size they are shown
- `f9dd12465` Foafnaut: fix structure syntax in redrawVectorPictures
- `025c760c4` Foafnaut: redrawVectorPictures builds the picture with its constructor
- `933a7d006` Foafnaut: no SVG redraw for an image URL with a fragment
- `c6ab4a477` Foafnaut: a background image URL with a fragment takes the picture's size

