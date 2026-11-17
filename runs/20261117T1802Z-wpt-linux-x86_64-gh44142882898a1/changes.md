### Since the previous full run: +0 subtests (+0.0000 points)

Previous: `20261117T1703Z-wpt-linux-x86_64-gh44132781746a1`, core `a5f53231e`, 92.4773%. This run: core `489cd1a98`, 92.4773%; 12 commits between.
Tests that lost subtests: 1 (-1); that gained: 1 (+1). Page outcomes: OK -1, STALL +1.

**Directories that fell** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| fetch | 13,288 | 8,825 | 8,824 | -1 |

**Directories that rose** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/semantics | 22,381 | 15,478 | 15,479 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 1 directories, the first 1)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| fetch/metadata | 1 | 1 |

**Tests that lost most** (the first 1 of 1)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /fetch/metadata/generated/element-img.https.sub.html | 18 | 17 | 45 |

**Commits between** (12)

- `eb90b0d8c` Band compile: keep the layout text's head across bands of one layout
- `c03f39658` Scroll: a frame past the band waits for the band being prefetched for the same state
- `d25a50dbc` Grid: do not measure an item whose columns read no contribution
- `bf36d240c` SVG: read the round-off numbers of drawing programs and the clip-rule attribute
- `a39e8c4b8` Images: a new store decodes only the files no kept store decoded
- `50f81a332` SVG: a clipPath whose one path is a rectangle clips as a rect
- `5f3caaae8` SVG: the number guards decide the comparison
- `a48c68606` Real sites: page scripts and web fonts run on pages up to 16 MiB of HTML; stylesheets apply up to 8 MiB
- `42aefcb3e` WebDocument page answer: type annotations for the kept-page lambdas (the band-head reuse did not elaborate)
- `5c4e0bb34` Merge pull request #592 from danbri/wip/look-svg
- `88a39e246` Merge pull request #599 from danbri/wip/coord-limits
- `489cd1a98` Merge pull request #594 from danbri/wip/speed3-scroll

