### Since the previous full run: +577 subtests (+0.0254 points)

Previous: `20261119T0259Z-wpt-linux-x86_64-gh44444459155a1`, core `1ba2ef928`, 92.5978%. This run: core `7311bbaa6`, 92.6231%; 4 commits between.
Tests that lost subtests: 2 (-2); that gained: 5 (+579). Page outcomes: CRASH +1, STALL -1.

**Directories that fell** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| web-locks | 517 | 449 | 448 | -1 |

**Directories that rose** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| dom/nodes | 16,227 | 14,929 | 15,487 | +558 |
| dom/(root) | 2,787 | 2,482 | 2,501 | +19 |
| shadow-dom | 14,724 | 14,132 | 14,133 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| third_party/test262 | 1 | 1 |
| web-locks | 1 | 1 |

**Tests that lost most** (the first 2 of 2)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /third_party/test262/test/built-ins/Function/prototype/toString/name.test262.html | 1 | 0 | 1 |
| /web-locks/non-secure-context.any.worker.html | 1 | 0 | 1 |

**Commits between** (4)

- `07195b1df` Processing instructions: attributes read from and written to their data
- `11e526878` PiAttributes: the executed escape, unescape and scan are loops, proved equal to the specification (fast_eq)
- `912b2a885` Validate PI pseudo-attributes and transport optional values losslessly
- `7311bbaa6` Merge pull request #619 from danbri/wip/piattrs-closeout

