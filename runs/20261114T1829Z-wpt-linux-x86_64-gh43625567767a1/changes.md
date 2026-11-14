### Since the previous full run: +2,268 subtests (+0.0999 points)

Previous: `20261114T1734Z-wpt-linux-x86_64-gh43621794622a1`, core `c3d227a9f`, 91.6566%. This run: core `53326e401`, 91.7565%; 16 commits between.
Tests that lost subtests: 5 (-5); that gained: 181 (+2,273). Page outcomes: OK +2, STALL -1, TIMEOUT -1.

**Directories that fell** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| preload | 956 | 47 | 46 | -1 |

**Directories that rose** (13; the first 13)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/css-grid | 16,015 | 9,115 | 11,121 | +2,006 |
| css/css-text | 5,863 | 3,134 | 3,297 | +163 |
| css/css-sizing | 6,523 | 4,968 | 5,012 | +44 |
| css/CSS2 | 2,566 | 2,421 | 2,432 | +11 |
| css/css-flexbox | 4,813 | 3,671 | 3,681 | +10 |
| css/css-position | 1,553 | 1,335 | 1,345 | +10 |
| css/css-writing-modes | 421 | 209 | 218 | +9 |
| css/css-inline | 869 | 631 | 636 | +5 |
| css/css-values | 10,428 | 4,901 | 4,905 | +4 |
| css/css-contain | 499 | 305 | 307 | +2 |
| css/cssom | 4,463 | 3,604 | 3,606 | +2 |
| css/cssom-view | 2,696 | 1,189 | 1,191 | +2 |
| compat | 143 | 101 | 102 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 5 directories, the first 5)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| css/css-fonts | 1 | 1 |
| css/css-inline | 1 | 1 |
| css/css-tables | 1 | 1 |
| html/dom | 1 | 1 |
| preload | 1 | 1 |

**Tests that lost most** (the first 5 of 5)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /css/css-fonts/font-size-zero-ligatures.html | 1 | 0 | 4 |
| /css/css-inline/text-box-trim/text-box-on-non-root-inline-box.html | 1 | 0 | 4 |
| /css/css-tables/tentative/td-box-sizing-003.html | 5 | 4 | 11 |
| /html/dom/elements/global-attributes/id-name.html | 1 | 0 | 1 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |

**Commits between** (16)

- `27861e975` docs: dataflow inventory: Temporal joins the directories no entry names (65 of 91)
- `b24a33007` Animated values reach the frame a host paints: the layout field animated, carried from each script turn
- `44f3011af` @import: imported style sheets are fetched and read in place; a session hears of late sheets
- `1b0be2f57` The image of an img is chosen from srcset and picture, among the formats the engine decodes
- `46bade4dd` The window shows a page before its images are in, and draws it again with them
- `82f6359ad` A turn's answer gives the animated values of the session's last layout
- `2f2b194df` The window loads the QuickJS guest when a page first runs on it
- `d00e26040` The window's first compile of a page asks for no CPU probe
- `1692b7e4b` The loader reads a page's sheets and scripts six at a time, in document order
- `f62e2a738` fontFaces: no cascade when the page's rules name every face
- `03294d47e` Real pages record: animated values, @import, image sources, the time to a first frame, the runner's page font
- `8691b3265` The loader reads a page's scripts, images and icon while its sheets are read
- `81bbd5efa` The window makes the main-thread engine's first call while the page is fetched
- `89f9af642` Real pages record: the loader's concurrent reads, the main-thread engine's first call, the warm-up that was tried
- `7e88ef022` The window: images after the first frame only for a page that runs no script; the main-thread engine's first call during the first compile
- `53326e401` A page's own web fonts are the fonts of its text when no page font is held

