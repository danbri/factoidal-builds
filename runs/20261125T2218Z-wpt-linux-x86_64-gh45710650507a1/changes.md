### Since the previous full run: +134 subtests (+0.0059 points)

Previous: `20261125T2106Z-wpt-linux-x86_64-gh45699880509a1`, core `dc102cae4`, 92.6402%. This run: core `acfa63c86`, 92.6461%; 6 commits between.
Tests that lost subtests: 2 (-2); that gained: 16 (+136). Page outcomes: OK -2, STALL +2.

**Directories that fell** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| fetch | 13,314 | 8,824 | 8,823 | -1 |

**Directories that rose** (5; the first 5)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/css-borders | 4,906 | 4,374 | 4,497 | +123 |
| css/css-sizing | 6,744 | 5,181 | 5,186 | +5 |
| css/css-cascade | 1,759 | 1,335 | 1,339 | +4 |
| css/css-values | 10,473 | 6,258 | 6,260 | +2 |
| html/semantics | 22,523 | 15,709 | 15,710 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| fetch/metadata | 1 | 1 |
| third_party/test262 | 1 | 1 |

**Tests that lost most** (the first 2 of 2)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /fetch/metadata/generated/element-img.https.sub.html | 19 | 18 | 45 |
| /third_party/test262/test/built-ins/RegExp/property-escapes/generated/Script_-_Linear_B.test262.html | 1 | 0 | 1 |

**Commits between** (6)

- `d2d98b99e` Size replaced aspect ratios in the selected box (#1094)
- `c9a112895` Foafnaut architecture briefing for an outside engineer: design rules, measured state, causes of slowness, where help pays off (issue 1031)
- `cbd84d30e` Read only complete WPT worker records while polling (#1115)
- `dd2a4e2dd` Fix the browser release checks for Particle Rex (#1113)
- `5d4a43662` Round-trip CSS border-radius corner values (#1099)
- `acfa63c86` Supply static image bytes in targeted WPT layout diagnostics (#1116)

