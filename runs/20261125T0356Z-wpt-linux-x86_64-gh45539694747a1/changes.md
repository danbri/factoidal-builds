### Since the previous full run: -35 subtests (-0.0015 points)

Previous: `20261125T0309Z-wpt-linux-x86_64-gh45538011347a1`, core `856332018`, 92.6324%. This run: core `856332018`, 92.6309% (the same commit: the difference is flakiness).
Tests that lost subtests: 3 (-65); that gained: 4 (+30). Page outcomes: CRASH -1, OK +1.

**Directories that fell** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| sanitizer-api | 3,839 | 2,639 | 2,576 | -63 |
| preload | 956 | 243 | 242 | -1 |
| streams | 5,796 | 5,580 | 5,579 | -1 |

**Directories that rose** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/dom | 72,463 | 69,902 | 69,929 | +27 |
| fetch | 13,290 | 8,806 | 8,807 | +1 |
| html/semantics | 22,498 | 15,587 | 15,588 | +1 |
| webcodecs | 4,168 | 2,638 | 2,639 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 3 directories, the first 3)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| sanitizer-api | 63 | 1 |
| preload | 1 | 1 |
| streams/piping | 1 | 1 |

**Tests that lost most** (the first 3 of 3)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /sanitizer-api/sanitizer-processing-instructions.html | 63 | 0 | 63 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |
| /streams/piping/general-addition.any.worker.html | 1 | 0 | 1 |

