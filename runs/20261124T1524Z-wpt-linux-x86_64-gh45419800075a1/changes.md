### Since the previous full run: +0 subtests (+0.0000 points)

Previous: `20261124T1436Z-wpt-linux-x86_64-gh45413410548a1`, core `472993e36`, 92.6235%. This run: core `b5ff72304`, 92.6235%; 2 commits between.
Tests that lost subtests: 2 (-6); that gained: 6 (+6). Page outcomes: CRASH -1, OK -2, STALL +3.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 4,168 | 2,643 | 2,638 | -5 |
| html/semantics | 22,498 | 15,586 | 15,585 | -1 |

**Directories that rose** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| third_party/test262 | 53,838 | 46,252 | 46,258 | +6 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| webcodecs | 5 | 1 |
| html/semantics | 1 | 1 |

**Tests that lost most** (the first 2 of 2)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /webcodecs/image-decoder.https.any.html | 15 | 10 | 47 |
| /html/semantics/embedded-content/the-video-element/intrinsic_sizes.htm | 3 | 2 | 5 |

**Commits between** (2)

- `14fbe357d` Handle String split limit coercion order and zero limits (#899)
- `b5ff72304` Resolve responsive CSS sizing and border-box image limits (#893)

