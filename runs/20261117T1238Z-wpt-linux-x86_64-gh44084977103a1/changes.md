### Since the previous full run: +49 subtests (+0.0022 points)

Previous: `20261117T1021Z-wpt-linux-x86_64-gh44058911941a1`, core `16bbfba09`, 92.4634%. This run: core `c91b7d21d`, 92.4656%; 2 commits between.
Tests that lost subtests: 2 (-2); that gained: 3 (+51). Page outcomes: OK +1, STALL -2, TIMEOUT +1.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/semantics | 22,381 | 15,192 | 15,191 | -1 |
| xhr | 2,344 | 1,821 | 1,820 | -1 |

**Directories that rose** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| resource-timing | 1,207 | 68 | 115 | +47 |
| shadow-dom | 14,720 | 14,126 | 14,129 | +3 |
| fetch | 13,288 | 8,824 | 8,825 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| html/semantics | 1 | 1 |
| xhr | 1 | 1 |

**Tests that lost most** (the first 2 of 2)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /html/semantics/embedded-content/the-img-element/list-of-available-images-does-not-coalesce-in-flight-requests.sub.tentative.html | 1 | 0 | 1 |
| /xhr/xmlhttprequest-timeout-simple.html?load fires normally | 1 | 0 | 1 |

**Commits between** (2)

- `e5ab9084b` gpu_pacing_test: the early-ask rate bound allows for the time the ask really came at (macOS runner timers overshoot: 0.081 > 0.08 failed the
- `c91b7d21d` Merge pull request #587 from danbri/wip/gpu-pacing-flake

