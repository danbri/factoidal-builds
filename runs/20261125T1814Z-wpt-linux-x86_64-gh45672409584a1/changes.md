### Since the previous full run: +44 subtests (+0.0019 points)

Previous: `20261125T1755Z-wpt-linux-x86_64-gh45668698254a1`, core `76f307e51`, 92.6340%. This run: core `af74c4f5d`, 92.6359%; 1 commits between.
Tests that lost subtests: 1 (-1); that gained: 4 (+45). Page outcomes: OK +5, STALL -4, TIMEOUT -1.

**Directories that fell** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| fetch | 13,314 | 8,823 | 8,822 | -1 |

**Directories that rose** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/dom | 72,476 | 69,888 | 69,929 | +41 |
| webcodecs | 4,138 | 2,720 | 2,722 | +2 |
| html/semantics | 22,523 | 15,616 | 15,617 | +1 |
| third_party/test262 | 53,838 | 46,342 | 46,343 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 1 directories, the first 1)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| fetch/metadata | 1 | 1 |

**Tests that lost most** (the first 1 of 1)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /fetch/metadata/generated/element-img.https.sub.html | 18 | 17 | 45 |

**Commits between** (1)

- `af74c4f5d` Foafnaut Tor: Deno worker transport with TLS in the module (unreviewed, opt-in)

