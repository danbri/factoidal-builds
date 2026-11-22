### Since the previous full run: +2,102 subtests (+0.0925 points)

Previous: `20261122T1133Z-wpt-macos-arm64-gh45017894805a1`, core `9a0e966fb`, 92.5283%. This run: core `ef1710ff2`, 92.6208%; 14 commits between.
Tests that lost subtests: 3 (-3); that gained: 8 (+2,105). Page outcomes: ERROR -4, NO_RESULT -3, OK +5, STALL +1, TIMEOUT +1.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/canvas | 6,273 | 3,719 | 3,718 | -1 |
| third_party/test262 | 53,838 | 46,249 | 46,248 | -1 |

**Directories that rose** (6; the first 6)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webgl | 4,284 | 2,164 | 4,259 | +2,095 |
| web-animations | 4,256 | 3,948 | 3,952 | +4 |
| websockets | 2,389 | 1,258 | 1,260 | +2 |
| css/css-fonts | 8,740 | 7,850 | 7,851 | +1 |
| css/cssom | 4,465 | 3,756 | 3,757 | +1 |
| xhr | 2,344 | 1,832 | 1,833 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| third_party/test262 | 2 | 2 |
| html/canvas | 1 | 1 |

**Tests that lost most** (the first 3 of 3)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /html/canvas/offscreen/transformations/2d.transformation.scale.negative.worker.html | 1 | 0 | 1 |
| /third_party/test262/test/language/statements/class/async-gen-method/yield-promise-reject-next-yield-star-async-iterator.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/statements/while/let-block-with-newline.test262.html | 1 | 0 | 1 |

**Commits between** (14)

- `9c4db521e` XML Encryption 1.1: PBKDF2 key derivation in key agreement (track B item 5, part 2)
- `4ca1c7669` Give the full SPARQL proof closure its cold-build budget
- `42b8fb017` Allow the cold SPARQL proof closure to finish (#735)
- `693c83827` Merge pull request #733 from danbri/claude/spec-b-xmlenc-pbkdf2
- `d2d29abfe` Print the required mixed query plan axiom report
- `e06668509` Emit the checked mixed query plan axiom report (#738)
- `6462a41c7` XML Encryption 1.1: xenc11:DerivedKey and octet decryption (track B item 5, part 3)
- `9d435f273` Merge pull request #742 from danbri/claude/spec-b-xmlenc-derivedkey
- `5ad780d0e` Record the causes of Foafnaut's CSS and SVG reftest failures (issue 747)
- `2eddda1e1` Reftest causes record: add the 2026-11-22 CSS reftest score (issue 747)
- `05a5f192d` Foafnaut: draw monospace text with Liberation Mono
- `e8f5552b4` CSS: a quoted generic family name is a family name
- `a11b4bce7` Reftests: draw serif and monospace text with the window's faces
- `ef1710ff2` Foafnaut skill: the Linux native build needs libc++-dev and libc++abi-dev

