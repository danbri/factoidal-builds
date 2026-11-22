### Since the previous full run: +492 subtests (+0.0216 points)

Previous: `20261122T1731Z-wpt-macos-arm64-gh45049889894a1`, core `ef1710ff2`, 92.6208%. This run: core `4618bea0c`, 92.6424%; 13 commits between.
Tests that lost subtests: 5 (-5); that gained: 21 (+497). Page outcomes: CRASH +1, NO_RESULT +2, STALL -1, TIMEOUT -2.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/css-align | 5,473 | 4,453 | 4,452 | -1 |
| xhr | 2,344 | 1,833 | 1,832 | -1 |

**Directories that rose** (12; the first 12)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/cssom-view | 2,722 | 1,283 | 1,548 | +265 |
| css/css-flexbox | 4,933 | 3,799 | 3,872 | +73 |
| css/css-transitions | 3,446 | 2,715 | 2,783 | +68 |
| css/css-overflow | 1,215 | 726 | 783 | +57 |
| quirks | 6,984 | 6,612 | 6,624 | +12 |
| css/css-values | 10,451 | 6,226 | 6,234 | +8 |
| css/css-logical | 1,366 | 1,162 | 1,166 | +4 |
| css/css-ui | 2,423 | 2,236 | 2,238 | +2 |
| mathml | 4,321 | 1,575 | 1,577 | +2 |
| css/css-borders | 4,906 | 4,349 | 4,350 | +1 |
| third_party/test262 | 53,838 | 46,248 | 46,249 | +1 |
| webcodecs | 3,935 | 2,580 | 2,581 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 5 directories, the first 5)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| css/css-align | 1 | 1 |
| css/css-overflow | 1 | 1 |
| html/canvas | 1 | 1 |
| third_party/test262 | 1 | 1 |
| xhr | 1 | 1 |

**Tests that lost most** (the first 5 of 5)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /css/css-align/abspos/default-overflow-with-scroll.html | 2 | 1 | 6 |
| /css/css-overflow/overflow-rtl-scroll-left.html | 1 | 0 | 1 |
| /html/canvas/offscreen/manual/filter/offscreencanvas.filter.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/Array/property-cast-boolean-primitive.test262.html | 1 | 0 | 1 |
| /xhr/xhr-timeout-longtask.any.html | 1 | 0 | 1 |

**Commits between** (13)

- `a843a1ff0` Expose GDSL app integration in the Hub and repair CPU fallback
- `66ceef66c` fix(ci): verify released runtime inputs separately from current browser host
- `3260ca9e9` Verify versioned GDSL runtime requests and run app in compatible-release browser CI
- `431877952` Merge current main and retain both GDSL and reftest worknotes
- `e029e7fca` XML Encryption 1.1 writer: PBKDF2 (§5.4.2) and xenc11:DerivedKey (§5.4.3)
- `d2b25f591` Merge pull request #756: XML Encryption 1.1 writer, PBKDF2 and xenc11:DerivedKey
- `ff19ccd10` CSS: border widths in every length unit and thin, medium, thick
- `25539a265` Layout: line boxes use the metrics of the text's own font
- `0c8eeb990` Reftests: no "Partial page" note in the pictures
- `e7cc73d7f` Reftest causes record: items 1 to 3 done, with measurements (issue 747)
- `b9f6c92bd` Merge PR #746: reusable GDSL app and verified CPU fallback
- `bbcf55b00` Keep vertical-align from shifting out-of-flow text (#762)
- `4618bea0c` Measure element scroll extents towards the reachable edges (#765)

