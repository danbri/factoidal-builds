### Since the previous full run: -4 subtests (-0.0002 points)

Previous: `20261126T1338Z-wpt-linux-x86_64-gh45825534915a1`, core `4a81bddce`, 92.6551%. This run: core `4a81bddce`, 92.6550% (the same commit: the difference is flakiness).
Tests that lost subtests: 2 (-7); that gained: 3 (+3). Page outcomes: CRASH +1, STALL -2, TIMEOUT +1.

**Directories that fell** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| referrer-policy | 8,815 | 5,754 | 5,748 | -6 |

**Directories that rose** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| fetch | 13,314 | 8,822 | 8,823 | +1 |
| preload | 956 | 242 | 243 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| referrer-policy/4K | 6 | 1 |
| third_party/test262 | 1 | 1 |

**Tests that lost most** (the first 2 of 2)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /referrer-policy/4K/gen/top.http-rp/no-referrer-when-downgrade/fetch.http.html | 12 | 6 | 12 |
| /third_party/test262/test/built-ins/global/10.2.1.1.3-4-27.test262.html | 1 | 0 | 1 |

