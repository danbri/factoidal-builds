### Since the previous full run: +1,292 subtests (+0.0568 points)

Previous: `20261122T2149Z-wpt-linux-x86_64-gh45070955784a1`, core `3abafe8e4`, 92.5901%. This run: core `7444aac0e`, 92.6469%; 5 commits between.
Tests that lost subtests: 6 (-9); that gained: 21 (+1,301). Page outcomes: STALL -1, TIMEOUT +1.

**Directories that fell** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| shadow-dom | 14,724 | 14,133 | 14,130 | -3 |
| html/rendering | 11,717 | 10,093 | 10,091 | -2 |
| preload | 956 | 243 | 242 | -1 |

**Directories that rose** (6; the first 6)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| selection/(root) | 33,918 | 32,388 | 33,664 | +1,276 |
| css/css-anchor-position | 13,670 | 11,449 | 11,463 | +14 |
| css/cssom-view | 2,722 | 1,548 | 1,553 | +5 |
| css/css-overflow | 1,215 | 785 | 786 | +1 |
| css/css-scrollbars | 83 | 53 | 54 | +1 |
| fetch | 13,290 | 8,807 | 8,808 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 4 directories, the first 4)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| css/css-anchor-position | 3 | 3 |
| shadow-dom/untriaged | 3 | 1 |
| html/rendering | 2 | 1 |
| preload | 1 | 1 |

**Tests that lost most** (the first 6 of 6)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /shadow-dom/untriaged/user-interaction/editing/inheritance-of-content-editable-001.html | 3 | 0 | 3 |
| /html/rendering/non-replaced-elements/the-fieldset-and-legend-elements/legend-align.html | 7 | 5 | 10 |
| /css/css-anchor-position/anchor-name-in-shadow-002.html | 1 | 0 | 1 |
| /css/css-anchor-position/anchor-name-in-shadow.html | 2 | 1 | 2 |
| /css/css-anchor-position/anchor-name-shadow-lower-tree.html | 1 | 0 | 1 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |

**Commits between** (5)

- `9a678c388` Place normal-flow blocks against the correct RTL edge (#778)
- `d465ec781` Render video posters through the existing image pipeline (#779)
- `ceb8f3940` Paint viewport negative z-index below normal flow (#784)
- `25dd520ec` Keep transparent CSS borders in layout without painting them (#785)
- `7444aac0e` Apply repeated CSS imports in cascade order (#782)

