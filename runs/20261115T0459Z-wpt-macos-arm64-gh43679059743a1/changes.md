### Since the previous full run: +201 subtests (+0.0089 points)

Previous: `20261115T0216Z-wpt-macos-arm64-gh43667008886a1`, core `8c96d3ec8`, 91.8373%. This run: core `3bf480d92`, 91.8461%; 1 commits between.
Tests that lost subtests: 3 (-4); that gained: 10 (+205). Page outcomes: ERROR -6, OK +6.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 3,922 | 2,574 | 2,572 | -2 |
| third_party/test262 | 53,833 | 43,374 | 43,373 | -1 |

**Directories that rose** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| streams | 5,796 | 5,381 | 5,580 | +199 |
| xhr | 2,344 | 1,810 | 1,814 | +4 |
| preload | 956 | 46 | 47 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| third_party/test262 | 2 | 2 |
| webcodecs | 2 | 1 |

**Tests that lost most** (the first 3 of 3)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /webcodecs/image-decoder.https.any.html | 15 | 13 | 47 |
| /third_party/test262/test/built-ins/Object/defineProperties/15.2.3.7-6-a-309.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/statements/class/elements/regular-definitions-static-private-fields.test262.html | 1 | 0 | 1 |

**Commits between** (1)

- `3bf480d92` XSLT result pages are HTML again: the xslt answer gives the result's syntax (html for the output methods html and text, WebXslt.resultSyntax

