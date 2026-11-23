### Since the previous full run: +113 subtests (+0.0050 points)

Previous: `20261122T2029Z-wpt-macos-arm64-gh45066559596a1`, core `4618bea0c`, 92.6424%. This run: core `7444aac0e`, 92.6474%; 22 commits between.
Tests that lost subtests: 8 (-57); that gained: 57 (+170). Page outcomes: CRASH -1, ERROR +3, NO_RESULT -2, OK -1, STALL +1.

**Directories that fell** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| streams | 5,796 | 5,580 | 5,532 | -48 |
| css/css-values | 10,451 | 6,234 | 6,231 | -3 |
| html/rendering | 11,717 | 10,093 | 10,091 | -2 |

**Directories that rose** (10; the first 10)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/css-grid | 16,018 | 11,158 | 11,273 | +115 |
| css/css-flexbox | 4,933 | 3,872 | 3,889 | +17 |
| css/css-anchor-position | 13,670 | 11,449 | 11,463 | +14 |
| css/css-inline | 869 | 637 | 642 | +5 |
| css/cssom-view | 2,722 | 1,548 | 1,553 | +5 |
| css/css-align | 5,473 | 4,452 | 4,456 | +4 |
| css/css-overflow | 1,215 | 783 | 786 | +3 |
| css/css-scrollbars | 83 | 53 | 54 | +1 |
| html/canvas | 6,273 | 3,718 | 3,719 | +1 |
| third_party/test262 | 53,838 | 46,249 | 46,250 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 4 directories, the first 4)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| streams/piping | 48 | 3 |
| css/css-values | 4 | 1 |
| css/css-anchor-position | 3 | 3 |
| html/rendering | 2 | 1 |

**Tests that lost most** (the first 8 of 8)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /streams/piping/error-propagation-forward.any.worker.html | 32 | 0 | 32 |
| /streams/piping/general.any.worker.html | 14 | 0 | 14 |
| /css/css-values/urls/fragment-only.html | 5 | 1 | 5 |
| /html/rendering/non-replaced-elements/the-fieldset-and-legend-elements/legend-align.html | 7 | 5 | 10 |
| /streams/piping/then-interception.any.worker.html | 2 | 0 | 2 |
| /css/css-anchor-position/anchor-name-in-shadow-002.html | 1 | 0 | 1 |
| /css/css-anchor-position/anchor-name-in-shadow.html | 2 | 1 | 2 |
| /css/css-anchor-position/anchor-name-shadow-lower-tree.html | 1 | 0 | 1 |

**Commits between** (22)

- `4bdb63768` Add checked Lean ASK attestations and a local RISC Zero receipt pipeline
- `1bf9c1b43` Bind exact runtime build inputs and add reproducible guest parity checks
- `3cf6ccb83` Expose bounded CPU proving profiles without changing the guest image
- `37a28c478` Merge main into checked ASK attestations
- `e3d6bad29` Render visible fallback glyphs for CSS control characters (#764)
- `0aae22807` Paint: images at their own size on whole pixels draw their pixels exactly
- `89ab7d931` Draw CSS background images (issue 704)
- `a512ab918` Reftest causes record: background images done, with measurements (issue 747)
- `e650d5bd9` Align items in right-to-left vertical grids (#770)
- `7fb81c709` Verify genuine ASK attestations through Groth16 and Solidity
- `000d811fa` Size grid items from their height and aspect ratio (#771)
- `342ca716e` Paint CSS table column and column-group colours (#769)
- `cf3cbc13a` Merge pull request #759: checked Lean ASK attestations
- `dfba1ee64` Open desktop pages at normal text size (#711)
- `631d0c1ee` Use grid order for horizontal container baselines (#773)
- `7e839e905` Apply background size and repeat to raster images (#772)
- `3abafe8e4` Accept and prove the cascade behavior of zero line height (#776)
- `9a678c388` Place normal-flow blocks against the correct RTL edge (#778)
- `d465ec781` Render video posters through the existing image pipeline (#779)
- `ceb8f3940` Paint viewport negative z-index below normal flow (#784)
- `25dd520ec` Keep transparent CSS borders in layout without painting them (#785)
- `7444aac0e` Apply repeated CSS imports in cascade order (#782)

