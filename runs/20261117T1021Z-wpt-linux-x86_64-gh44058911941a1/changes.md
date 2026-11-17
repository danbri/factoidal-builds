### Since the previous full run: +123 subtests (+0.0054 points)

Previous: `20261117T0930Z-wpt-linux-x86_64-gh44052214075a1`, core `e360123cb`, 92.4580%. This run: core `16bbfba09`, 92.4634%; 4 commits between.
Tests that lost subtests: 2 (-3); that gained: 24 (+126). Page outcomes: CRASH +1, TIMEOUT -1.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 3,922 | 2,574 | 2,572 | -2 |
| fetch | 13,288 | 8,825 | 8,824 | -1 |

**Directories that rose** (9; the first 9)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html-aam | 891 | 810 | 851 | +41 |
| dpub-aam | 39 | 0 | 39 | +39 |
| svg-aam | 54 | 31 | 48 | +17 |
| wai-aria | 588 | 544 | 557 | +13 |
| accname | 509 | 423 | 432 | +9 |
| graphics-aria | 3 | 0 | 3 | +3 |
| css/css-display | 669 | 623 | 625 | +2 |
| core-aam | 205 | 7 | 8 | +1 |
| html/semantics | 22,381 | 15,191 | 15,192 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| webcodecs | 2 | 1 |
| fetch/metadata | 1 | 1 |

**Tests that lost most** (the first 2 of 2)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /webcodecs/image-decoder.https.any.html | 15 | 13 | 47 |
| /fetch/metadata/generated/element-img.https.sub.html | 18 | 17 | 45 |

**Commits between** (4)

- `3c741b1d2` Roles and names for the accessibility tests; accessibility properties for the test driver
- `ad2c6a351` Merge wip/a11y-engine (with main) into wip/a11y-wpt
- `8567870ad` Merge remote-tracking branch 'origin/main' into a11ywpt
- `16bbfba09` Merge pull request #579 from danbri/wip/a11y-wpt

