### Since the previous full run: +1 subtests (+0.0000 points)

Previous: `20261124T2330Z-wpt-linux-x86_64-gh45506175080a1`, core `f22156198`, 92.6315%. This run: core `4e8b173fd`, 92.6316%; 15 commits between.
Tests that lost subtests: 3 (-4); that gained: 5 (+5). Page outcomes: CRASH +1, NO_RESULT -1, OK -1, TIMEOUT +1.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 4,168 | 2,638 | 2,636 | -2 |
| IndexedDB | 5,853 | 5,504 | 5,503 | -1 |

**Directories that rose** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| third_party/test262 | 53,838 | 46,277 | 46,280 | +3 |
| css/css-sizing | 6,743 | 5,138 | 5,139 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 3 directories, the first 3)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| webcodecs | 2 | 1 |
| IndexedDB | 1 | 1 |
| html/semantics | 1 | 1 |

**Tests that lost most** (the first 3 of 3)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /webcodecs/image-decoder.https.any.html | 10 | 8 | 47 |
| /IndexedDB/interleaved-cursors-large.any.html | 1 | 0 | 1 |
| /html/semantics/embedded-content/the-video-element/intrinsic_sizes.htm | 3 | 2 | 5 |

**Commits between** (15)

- `0cf10082c` Size HTML buttons by their border boxes by default
- `6f8ca4d1b` Paint repeating CSS backgrounds with one bitmap record
- `01aac5cd2` Use a Lean identifier for the repeat flag
- `871da79e7` Read Array and TypedArray at indices after coercion
- `38168746d` Integrate HTML button sizing with the GOV.UK heading fix
- `2a69ebffd` Keep pointer link requests within the renderer transport limit
- `4099e3dbe` Include repeat axes when comparing retained bitmap paints
- `046e86e2b` Merge pull request #967 from danbri/wip/array-at-ordered-read
- `0fccf0b6e` Foafnaut: report web-font and @import limits (issue 865); restyle reasons and link sheets (issue 871)
- `3481cebb0` Integrate repeating backgrounds with current limit diagnostics
- `00d053ce6` Merge pull request #963 from danbri/wip/html-button-border-box
- `86d610b0e` Merge pull request #970 from danbri/wip/bounded-pointer-link-transport
- `d97a9405c` Record the bounded CSS import walker in the release audit
- `d54ee7157` Merge pull request #980 from danbri/wip/bounded-css-import-audit
- `4e8b173fd` Merge pull request #966 from danbri/wip/compact-css-image-repeat

