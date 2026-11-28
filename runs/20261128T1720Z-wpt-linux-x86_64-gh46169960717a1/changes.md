### Since the previous full run: +6 subtests (+0.0003 points)

Previous: `20261128T1622Z-wpt-linux-x86_64-gh46164843294a1`, core `bd0d78dd1`, 92.8191%. This run: core `92fc7ebec`, 92.8194%; 2 commits between.
Tests that lost subtests: 3 (-6); that gained: 3 (+12). Page outcomes: CRASH -1, OK -1, TIMEOUT +2.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/syntax | 9,013 | 8,685 | 8,684 | -1 |
| svg/interact | 9,304 | 8,860 | 8,859 | -1 |

**Directories that rose** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| referrer-policy | 8,815 | 5,744 | 5,750 | +6 |
| preload | 956 | 242 | 243 | +1 |
| third_party/test262 | 53,838 | 46,417 | 46,418 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 3 directories, the first 3)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| referrer-policy/gen | 4 | 1 |
| html/syntax | 1 | 1 |
| svg/interact | 1 | 1 |

**Tests that lost most** (the first 3 of 3)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /referrer-policy/gen/srcdoc.meta/unsafe-url/svg-a-tag.http.html | 4 | 0 | 4 |
| /html/syntax/speculative-parsing/generated/page-load/link-rel-stylesheet-disabled.tentative.html | 1 | 0 | 1 |
| /svg/interact/script-content.svg | 1 | 0 | 1 |

**Commits between** (2)

- `59f9aad51` Exercise Foafnaut native engine sessions from Rust (#1233)
- `92fc7ebec` Merge pull request #1244 from danbri/wip/1233-native-desktop

