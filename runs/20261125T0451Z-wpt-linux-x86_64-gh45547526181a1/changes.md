### Since the previous full run: +66 subtests (+0.0029 points)

Previous: `20261125T0356Z-wpt-linux-x86_64-gh45539694747a1`, core `856332018`, 92.6309%. This run: core `4a0c174b7`, 92.6338%; 8 commits between.
Tests that lost subtests: 0 (-0); that gained: 4 (+66). Page outcomes: ERROR +1, OK +3, STALL -3, TIMEOUT -1.

**Directories that rose** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| sanitizer-api | 3,839 | 2,576 | 2,639 | +63 |
| IndexedDB | 5,853 | 5,503 | 5,504 | +1 |
| streams | 5,796 | 5,579 | 5,580 | +1 |
| webcodecs | 4,168 | 2,639 | 2,640 | +1 |

**Commits between** (8)

- `56e741b7e` tree_op reads and importNode no longer style the whole document (issue 871)
- `1f5957644` Foafnaut: report maxPieces, maxValueBytes, maxFallbacks, maxTracks and maxSheetBytes as limit hits (issue 865)
- `06859d927` Keep counters and list markers in box order through display contents (#999)
- `eec048b9d` Reuse pinned HTTPS connections through synchronous script startup (#1004)
- `1af5b0d8f` Paint the current text input value after edits (#1000)
- `44e1a39cf` Overlap web font loading with image and icon loading (#892)
- `e586b539d` Reuse approved HTTPS connections during web font loading (#1006)
- `4a0c174b7` Track the renamed CSS variable recursion in the compiled audit (#1007)

