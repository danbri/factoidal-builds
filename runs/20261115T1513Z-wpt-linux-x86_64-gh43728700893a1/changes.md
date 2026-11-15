### Since the previous full run: -2 subtests (-0.0001 points)

Previous: `20261115T1100Z-wpt-linux-x86_64-gh43706769829a1`, core `2f3e888e2`, 91.8475%. This run: core `cc73af028`, 91.8474%; 3 commits between.
Tests that lost subtests: 2 (-2); that gained: 0 (+0). Page outcomes: OK -1, STALL +2, TIMEOUT -1.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| preload | 956 | 243 | 242 | -1 |
| webcodecs | 3,922 | 2,579 | 2,578 | -1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| preload | 1 | 1 |
| webcodecs | 1 | 1 |

**Tests that lost most** (the first 2 of 2)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |
| /webcodecs/image-decoder.https.any.html | 20 | 19 | 47 |

**Commits between** (3)

- `109319318` textnaut 0.1.3: pin the Wasm engine of 2f3e888e2 (build-2f3e888e2d0e-foafnaut-web; the ff075ad5a asset was re-uploaded by a rebuild and no l
- `a00f54025` test.sh: run every check and list all failures at the end (exit 1 if any); --fail-fast stops at the first; per-check times; summary to GITHU
- `cc73af028` showcase_gaps_test: issue 369 is closed (an empty block inside an inline-block is painted: one more primitive), so the test asserts it; test

