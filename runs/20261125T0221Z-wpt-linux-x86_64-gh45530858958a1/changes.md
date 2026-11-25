### Since the previous full run: +19 subtests (+0.0008 points)

Previous: `20261125T0133Z-wpt-linux-x86_64-gh45526454559a1`, core `d38eaddb3`, 92.6330%. This run: core `6fe1473fc`, 92.6338%; 6 commits between.
Tests that lost subtests: 3 (-3); that gained: 16 (+22). Page outcomes: OK +1, STALL -1.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/css-text | 5,863 | 4,460 | 4,458 | -2 |
| webcodecs | 4,168 | 2,639 | 2,638 | -1 |

**Directories that rose** (9; the first 9)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| third_party/test262 | 53,838 | 46,280 | 46,287 | +7 |
| css/cssom-view | 2,722 | 1,560 | 1,565 | +5 |
| css/css-position | 1,605 | 1,362 | 1,364 | +2 |
| css/css-ruby | 109 | 61 | 63 | +2 |
| css/css-writing-modes | 421 | 229 | 231 | +2 |
| css/CSS2 | 2,566 | 2,464 | 2,465 | +1 |
| css/css-anchor-position | 13,670 | 11,544 | 11,545 | +1 |
| css/css-overflow | 1,215 | 791 | 792 | +1 |
| html/semantics | 22,498 | 15,588 | 15,589 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| css/css-text | 2 | 2 |
| webcodecs | 1 | 1 |

**Tests that lost most** (the first 3 of 3)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /css/css-text/overflow-wrap/overflow-wrap-anywhere-span-002.html | 1 | 0 | 1 |
| /css/css-text/overflow-wrap/overflow-wrap-break-word-span-002.html | 1 | 0 | 1 |
| /webcodecs/image-decoder.https.any.html | 11 | 10 | 47 |

**Commits between** (6)

- `005ca9bb6` Generate the fuel lemma for the shared Array and TypedArray at operation
- `04d672fdf` Process Object.fromEntries entries before advancing the iterator
- `102942a00` Keep CSS text runs intact across inline elements
- `ead665451` Merge pull request #987 from danbri/wip/array-at-fuel-mono
- `ad69cf2a7` Merge pull request #988 from danbri/wip/object-from-entries-iterator-order
- `6fe1473fc` Merge pull request #989 from danbri/wip/inline-text-boundary-wrap

