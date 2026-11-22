### Since the previous full run: +141 subtests (+0.0062 points)

Previous: `20261122T2035Z-wpt-linux-x86_64-gh45064795120a1`, core `a512ab918`, 92.5839%. This run: core `3abafe8e4`, 92.5901%; 13 commits between.
Tests that lost subtests: 1 (-2); that gained: 35 (+143). Page outcomes: OK +1, TIMEOUT -1.

**Directories that fell** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 3,935 | 2,583 | 2,581 | -2 |

**Directories that rose** (5; the first 5)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/css-grid | 16,018 | 11,158 | 11,273 | +115 |
| css/css-flexbox | 4,933 | 3,872 | 3,889 | +17 |
| css/css-inline | 869 | 637 | 642 | +5 |
| css/css-align | 5,473 | 4,452 | 4,456 | +4 |
| css/css-overflow | 1,215 | 783 | 785 | +2 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 1 directories, the first 1)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| webcodecs | 2 | 1 |

**Tests that lost most** (the first 1 of 1)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /webcodecs/image-decoder.https.any.html | 16 | 14 | 47 |

**Commits between** (13)

- `4bdb63768` Add checked Lean ASK attestations and a local RISC Zero receipt pipeline
- `1bf9c1b43` Bind exact runtime build inputs and add reproducible guest parity checks
- `3cf6ccb83` Expose bounded CPU proving profiles without changing the guest image
- `37a28c478` Merge main into checked ASK attestations
- `e650d5bd9` Align items in right-to-left vertical grids (#770)
- `7fb81c709` Verify genuine ASK attestations through Groth16 and Solidity
- `000d811fa` Size grid items from their height and aspect ratio (#771)
- `342ca716e` Paint CSS table column and column-group colours (#769)
- `cf3cbc13a` Merge pull request #759: checked Lean ASK attestations
- `dfba1ee64` Open desktop pages at normal text size (#711)
- `631d0c1ee` Use grid order for horizontal container baselines (#773)
- `7e839e905` Apply background size and repeat to raster images (#772)
- `3abafe8e4` Accept and prove the cascade behavior of zero line height (#776)

