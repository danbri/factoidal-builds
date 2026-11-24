### Since the previous full run: -302 subtests (-0.0133 points)

Previous: `20261123T0423Z-wpt-macos-arm64-gh45111558705a1`, core `ffbca467f`, 92.6373%. This run: core `c6ab4a477`, 92.6241%; 19 commits between.
Tests that lost subtests: 12 (-320); that gained: 9 (+18). Page outcomes: ERROR +3, NO_RESULT -2, OK +1, STALL -2.

**Directories that fell** (5; the first 5)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| streams | 5,796 | 5,580 | 5,307 | -273 |
| css/css-pseudo | 903 | 505 | 468 | -37 |
| css/selectors | 6,266 | 5,723 | 5,719 | -4 |
| css/css-conditional | 3,298 | 2,238 | 2,236 | -2 |
| css/css-shadow | 377 | 242 | 241 | -1 |

**Directories that rose** (6; the first 6)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/css-borders | 4,906 | 4,350 | 4,358 | +8 |
| css/css-text | 5,863 | 4,458 | 4,460 | +2 |
| webcodecs | 3,974 | 2,608 | 2,610 | +2 |
| IndexedDB | 5,853 | 5,503 | 5,504 | +1 |
| css/css-grid | 16,018 | 11,273 | 11,274 | +1 |
| preload | 956 | 242 | 243 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 8 directories, the first 8)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| streams | 218 | 1 |
| streams/readable-streams | 50 | 1 |
| css/css-pseudo | 39 | 1 |
| streams/piping | 5 | 1 |
| css/selectors | 4 | 4 |
| css/css-conditional | 2 | 2 |
| css/css-shadow | 1 | 1 |
| third_party/test262 | 1 | 1 |

**Tests that lost most** (the first 12 of 12)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /streams/idlharness.any.sharedworker.html | 218 | 0 | 228 |
| /streams/readable-streams/from.any.worker.html | 50 | 0 | 50 |
| /css/css-pseudo/first-letter-allowed-properties.html | 44 | 5 | 45 |
| /streams/piping/flow-control.any.sharedworker.html | 5 | 0 | 5 |
| /css/css-conditional/container-queries/pseudo-elements-004.html | 6 | 5 | 12 |
| /css/css-conditional/container-queries/pseudo-elements-007.html | 6 | 5 | 12 |
| /css/css-shadow/part/pseudo-elements-after-part.html | 29 | 28 | 44 |
| /css/selectors/old-tests/css3-modsel-39.xml | 1 | 0 | 1 |
| /css/selectors/old-tests/css3-modsel-39a.xml | 1 | 0 | 1 |
| /css/selectors/old-tests/css3-modsel-39b.xml | 1 | 0 | 1 |
| /css/selectors/old-tests/css3-modsel-39c.xml | 1 | 0 | 1 |
| /third_party/test262/test/language/identifiers/val-new.test262.html | 1 | 0 | 1 |

**Commits between** (19)

- `b1ff4ff6a` Read letter-spacing, word-spacing and text-indent
- `118fc9f73` Read background-clip; WebRepaint compares the new text and clip fields
- `63a06e585` background-clip is an HTML property for an embedded SVG root
- `abf65c8e3` Letter spacing per cluster, as a percentage of the font size; indent in intrinsic widths
- `a976a87ce` Rendering: spacing percentages inherit as percentages; background-clip lists; border width snapping
- `ce59a14a2` No letter-spacing on format and bidi controls or cursive scripts (CSS Text 3 §8.1)
- `2cfbc00ae` Foafnaut: run event handler content attributes on pages with no script element
- `97b52ad1e` Foafnaut: a render that names more images than the engine holds is drawn, not refused
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

