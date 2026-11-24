### Since the previous full run: +9 subtests (+0.0004 points)

Previous: `20261124T2119Z-wpt-linux-x86_64-gh45489157107a1`, core `9b554985b`, 92.6312%. This run: core `d63d0983f`, 92.6316%; 6 commits between.
Tests that lost subtests: 1 (-1); that gained: 6 (+10). Page outcomes: CRASH -1, OK +1.

**Directories that fell** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| xhr | 2,344 | 1,834 | 1,833 | -1 |

**Directories that rose** (5; the first 5)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 4,168 | 2,637 | 2,641 | +4 |
| editing/other | 16,742 | 13,797 | 13,799 | +2 |
| third_party/test262 | 53,838 | 46,275 | 46,277 | +2 |
| fetch | 13,290 | 8,807 | 8,808 | +1 |
| html/semantics | 22,498 | 15,588 | 15,589 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 1 directories, the first 1)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| xhr | 1 | 1 |

**Tests that lost most** (the first 1 of 1)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /xhr/xmlhttprequest-timeout-overridesexpires.html?timeout set to expiring value after load fires | 1 | 0 | 1 |

**Commits between** (6)

- `3e016df8a` Preserve small inputs in BubblePop expm1 and log1p
- `6ad62abbf` Activate focused disclosure summaries with Space
- `867f5658f` Read captured negative registry output without SIGPIPE
- `37f89212e` Merge pull request #959 from danbri/wip/dataflow-test-broken-pipe
- `2436a37f8` Merge pull request #956 from danbri/wip/details-keyboard-activation
- `d63d0983f` Merge pull request #953 from danbri/wip/bubblepop-small-math

