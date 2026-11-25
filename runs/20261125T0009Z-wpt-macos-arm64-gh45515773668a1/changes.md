### Since the previous full run: -2 subtests (-0.0001 points)

Previous: `20261124T2315Z-wpt-macos-arm64-gh45508351925a1`, core `d7e315b58`, 92.6333%. This run: core `384c4b619`, 92.6332%; 6 commits between.
Tests that lost subtests: 2 (-2); that gained: 0 (+0). Page outcomes: NO_RESULT -1, OK -1, STALL +1, TIMEOUT +1.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| third_party/test262 | 53,838 | 46,277 | 46,276 | -1 |
| webcodecs | 4,168 | 2,642 | 2,641 | -1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| third_party/test262 | 1 | 1 |
| webcodecs | 1 | 1 |

**Tests that lost most** (the first 2 of 2)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /third_party/test262/test/language/statements/for-await-of/async-gen-decl-dstr-obj-id-init-assignment-undef.test262.html | 1 | 0 | 1 |
| /webcodecs/image-decoder.https.any.html | 14 | 13 | 47 |

**Commits between** (6)

- `65b705213` Balance short text runs using their ordinary soft wrap opportunities
- `5891acdee` Guard hover repaint against changed line balancing
- `e17ec447b` Build the HTML image lookup before entering layout
- `c919dc1cb` Integrate balanced heading wrapping with the disclosure layout
- `79feaf006` Merge pull request #958 from danbri/wip/balanced-heading-wrap
- `384c4b619` Merge pull request #964 from danbri/wip/eager-html-picture-map

