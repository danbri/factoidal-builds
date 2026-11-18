### Since the previous full run: +48 subtests (+0.0021 points)

Previous: `20261118T1642Z-wpt-linux-x86_64-gh44350286733a1`, core `080473762`, 92.5954%. This run: core `34d08979c`, 92.5975%; 3 commits between.
Tests that lost subtests: 3 (-10); that gained: 5 (+58). Page outcomes: CRASH +1, OK +1, STALL -2.

**Directories that fell** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 3,926 | 2,580 | 2,571 | -9 |

**Directories that rose** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/css-syntax | 444 | 352 | 391 | +39 |
| css/selectors | 6,266 | 5,707 | 5,723 | +16 |
| preload | 956 | 242 | 243 | +1 |
| third_party/test262 | 53,838 | 46,248 | 46,249 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| webcodecs | 9 | 2 |
| third_party/test262 | 1 | 1 |

**Tests that lost most** (the first 3 of 3)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /webcodecs/image-decoder.https.any.html | 17 | 10 | 47 |
| /webcodecs/videoFrame-alpha.any.html | 2 | 0 | 2 |
| /third_party/test262/test/built-ins/Object/create/15.2.3.5-4-236.test262.html | 1 | 0 | 1 |

**Commits between** (3)

- `5d73c43c2` Fix An+B whitespace validation and negative offset serialisation
- `e4241ac32` Use the whitespace hypothesis before unfolding its predicate
- `34d08979c` Merge pull request #602: fix An+B whitespace and negative offsets

