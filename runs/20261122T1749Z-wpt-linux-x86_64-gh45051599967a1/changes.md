### Since the previous full run: -1,181 subtests (-0.0520 points)

Previous: `20261122T1547Z-wpt-linux-x86_64-gh45040205550a1`, core `2eddda1e1`, 92.6183%. This run: core `b9f6c92bd`, 92.5664%; 15 commits between.
Tests that lost subtests: 4 (-1,281); that gained: 16 (+100). Page outcomes: CRASH -1, STALL +1.

**Directories that fell** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| selection/(root) | 33,918 | 33,664 | 32,388 | -1,276 |
| webcodecs | 3,935 | 2,581 | 2,578 | -3 |
| mixed-content | 2,281 | 1,319 | 1,318 | -1 |
| preload | 956 | 243 | 242 | -1 |

**Directories that rose** (10; the first 10)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/css-transitions | 3,446 | 2,715 | 2,783 | +68 |
| quirks | 6,984 | 6,612 | 6,624 | +12 |
| css/css-values | 10,451 | 6,226 | 6,234 | +8 |
| css/css-logical | 1,366 | 1,162 | 1,166 | +4 |
| css/css-ui | 2,423 | 2,236 | 2,238 | +2 |
| mathml | 4,321 | 1,575 | 1,577 | +2 |
| IndexedDB | 5,853 | 5,503 | 5,504 | +1 |
| css/css-borders | 4,906 | 4,349 | 4,350 | +1 |
| css/css-fonts | 8,740 | 7,850 | 7,851 | +1 |
| css/cssom | 4,465 | 3,756 | 3,757 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 4 directories, the first 4)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| selection | 1,276 | 1 |
| webcodecs | 3 | 1 |
| mixed-content/gen | 1 | 1 |
| preload | 1 | 1 |

**Tests that lost most** (the first 4 of 4)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /selection/addRange-32.html | 1,276 | 0 | 1,276 |
| /webcodecs/image-decoder.https.any.html | 14 | 11 | 47 |
| /mixed-content/gen/iframe-inherit.http-rp/opt-in/worker-import.https.html | 6 | 5 | 8 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |

**Commits between** (15)

- `a843a1ff0` Expose GDSL app integration in the Hub and repair CPU fallback
- `66ceef66c` fix(ci): verify released runtime inputs separately from current browser host
- `3260ca9e9` Verify versioned GDSL runtime requests and run app in compatible-release browser CI
- `431877952` Merge current main and retain both GDSL and reftest worknotes
- `05a5f192d` Foafnaut: draw monospace text with Liberation Mono
- `e8f5552b4` CSS: a quoted generic family name is a family name
- `a11b4bce7` Reftests: draw serif and monospace text with the window's faces
- `ef1710ff2` Foafnaut skill: the Linux native build needs libc++-dev and libc++abi-dev
- `e029e7fca` XML Encryption 1.1 writer: PBKDF2 (§5.4.2) and xenc11:DerivedKey (§5.4.3)
- `d2b25f591` Merge pull request #756: XML Encryption 1.1 writer, PBKDF2 and xenc11:DerivedKey
- `ff19ccd10` CSS: border widths in every length unit and thin, medium, thick
- `25539a265` Layout: line boxes use the metrics of the text's own font
- `0c8eeb990` Reftests: no "Partial page" note in the pictures
- `e7cc73d7f` Reftest causes record: items 1 to 3 done, with measurements (issue 747)
- `b9f6c92bd` Merge PR #746: reusable GDSL app and verified CPU fallback

