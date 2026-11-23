### Since the previous full run: -45 subtests (-0.0020 points)

Previous: `20261123T0128Z-wpt-linux-x86_64-gh45092829658a1`, core `7eb6f33d5`, 92.6366%. This run: core `ffbca467f`, 92.6346%; 2 commits between.
Tests that lost subtests: 2 (-49); that gained: 1 (+4). Page outcomes: OK -2, STALL +2.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| resource-timing | 1,220 | 115 | 68 | -47 |
| html/dom | 72,439 | 69,928 | 69,926 | -2 |

**Directories that rose** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/css-transitions | 3,446 | 2,783 | 2,787 | +4 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| resource-timing | 47 | 1 |
| html/dom | 2 | 1 |

**Tests that lost most** (the first 2 of 2)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /resource-timing/idlharness.any.html | 47 | 0 | 79 |
| /html/dom/aria-element-reflection-disconnected.html | 2 | 0 | 2 |

**Commits between** (2)

- `dd99ee4df` Give each border side its own style and colour; draw dotted to ridge
- `ffbca467f` WebRepaint: compare and recolour borders side by side

