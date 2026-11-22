### Since the previous full run: +341 subtests (+0.0150 points)

Previous: `20261122T1851Z-wpt-linux-x86_64-gh45057465947a1`, core `bbcf55b00`, 92.6249%. This run: core `4618bea0c`, 92.6399%; 1 commits between.
Tests that lost subtests: 5 (-56); that gained: 5 (+397). Page outcomes: CRASH -1, ERROR -1, OK -1, STALL +3.

**Directories that fell** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| resource-timing | 1,220 | 115 | 68 | -47 |
| webcodecs | 3,935 | 2,584 | 2,578 | -6 |
| css/css-align | 5,473 | 4,453 | 4,452 | -1 |
| fetch | 13,290 | 8,808 | 8,807 | -1 |

**Directories that rose** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/cssom-view | 2,722 | 1,283 | 1,548 | +265 |
| css/css-flexbox | 4,933 | 3,799 | 3,872 | +73 |
| css/css-overflow | 1,215 | 726 | 783 | +57 |
| preload | 956 | 242 | 243 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 5 directories, the first 5)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| resource-timing | 47 | 1 |
| webcodecs | 6 | 1 |
| css/css-align | 1 | 1 |
| css/css-overflow | 1 | 1 |
| fetch/metadata | 1 | 1 |

**Tests that lost most** (the first 5 of 5)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /resource-timing/idlharness.any.html | 47 | 0 | 79 |
| /webcodecs/image-decoder.https.any.html | 17 | 11 | 47 |
| /css/css-align/abspos/default-overflow-with-scroll.html | 2 | 1 | 6 |
| /css/css-overflow/overflow-rtl-scroll-left.html | 1 | 0 | 1 |
| /fetch/metadata/generated/element-img.https.sub.html | 19 | 18 | 45 |

**Commits between** (1)

- `4618bea0c` Measure element scroll extents towards the reachable edges (#765)

