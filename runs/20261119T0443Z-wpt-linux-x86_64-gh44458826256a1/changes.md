### Since the previous full run: -60 subtests (-0.0026 points)

Previous: `20261119T0349Z-wpt-linux-x86_64-gh44451581401a1`, core `7311bbaa6`, 92.6231%. This run: core `4120db7d1`, 92.6205%; 2 commits between.
Tests that lost subtests: 1 (-63); that gained: 3 (+3). Page outcomes: STALL +1, TIMEOUT -1.

**Directories that fell** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| sanitizer-api | 3,816 | 2,625 | 2,562 | -63 |

**Directories that rose** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/semantics | 22,416 | 15,575 | 15,576 | +1 |
| service-workers | 3,268 | 1,392 | 1,393 | +1 |
| third_party/test262 | 53,838 | 46,249 | 46,250 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 1 directories, the first 1)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| sanitizer-api | 63 | 1 |

**Tests that lost most** (the first 1 of 1)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /sanitizer-api/sanitizer-processing-instructions.html | 63 | 0 | 63 |

**Commits between** (2)

- `c655f4727` Document the published full Linux browser download
- `4120db7d1` Merge pull request #624 from danbri/wip/linux-browser-release-docs

