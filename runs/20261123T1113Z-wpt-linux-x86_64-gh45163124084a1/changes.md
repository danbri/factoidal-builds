### Since the previous full run: +8 subtests (+0.0004 points)

Previous: `20261123T0944Z-wpt-linux-x86_64-gh45149757055a1`, core `ffbca467f`, 92.6349%. This run: core `97b52ad1e`, 92.6353%; 8 commits between.
Tests that lost subtests: 2 (-2); that gained: 3 (+10). Page outcomes: CRASH -1, OK -2, STALL +2, TIMEOUT +1.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| fetch | 13,290 | 8,808 | 8,807 | -1 |
| webcodecs | 3,974 | 2,614 | 2,613 | -1 |

**Directories that rose** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/css-borders | 4,906 | 4,350 | 4,358 | +8 |
| css/css-text | 5,863 | 4,458 | 4,460 | +2 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| fetch/metadata | 1 | 1 |
| webcodecs | 1 | 1 |

**Tests that lost most** (the first 2 of 2)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /fetch/metadata/generated/element-img.https.sub.html | 19 | 18 | 45 |
| /webcodecs/image-decoder.https.any.html | 14 | 13 | 47 |

**Commits between** (8)

- `b1ff4ff6a` Read letter-spacing, word-spacing and text-indent
- `118fc9f73` Read background-clip; WebRepaint compares the new text and clip fields
- `63a06e585` background-clip is an HTML property for an embedded SVG root
- `abf65c8e3` Letter spacing per cluster, as a percentage of the font size; indent in intrinsic widths
- `a976a87ce` Rendering: spacing percentages inherit as percentages; background-clip lists; border width snapping
- `ce59a14a2` No letter-spacing on format and bidi controls or cursive scripts (CSS Text 3 §8.1)
- `2cfbc00ae` Foafnaut: run event handler content attributes on pages with no script element
- `97b52ad1e` Foafnaut: a render that names more images than the engine holds is drawn, not refused

