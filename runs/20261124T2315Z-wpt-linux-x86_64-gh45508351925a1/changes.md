### Since the previous full run: +5 subtests (+0.0002 points)

Previous: `20261124T2222Z-wpt-linux-x86_64-gh45496612893a1`, core `d63d0983f`, 92.6316%. This run: core `d7e315b58`, 92.6318%; 7 commits between.
Tests that lost subtests: 4 (-4); that gained: 5 (+9). Page outcomes: OK -1, STALL +1.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/semantics | 22,498 | 15,589 | 15,587 | -2 |
| fetch | 13,290 | 8,808 | 8,807 | -1 |

**Directories that rose** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 4,168 | 2,641 | 2,645 | +4 |
| infrastructure | 290 | 111 | 113 | +2 |
| html/rendering | 11,722 | 10,120 | 10,121 | +1 |
| xhr | 2,344 | 1,833 | 1,834 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 3 directories, the first 3)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| html/semantics | 2 | 2 |
| fetch/metadata | 1 | 1 |
| html/rendering | 1 | 1 |

**Tests that lost most** (the first 4 of 4)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /fetch/metadata/generated/element-img.https.sub.html | 19 | 18 | 45 |
| /html/rendering/widgets/button-layout/display-other.html | 2 | 1 | 18 |
| /html/semantics/embedded-content/the-img-element/list-of-available-images-does-not-coalesce-in-flight-requests.sub.tentative.html | 1 | 0 | 1 |
| /html/semantics/popovers/popover-attribute-all-elements.html | 1,083 | 1,082 | 1,101 |

**Commits between** (7)

- `94a0e0b3d` Render details disclosure glyphs as list markers
- `62976cab1` Include the added defaults in the user-agent rule count guard
- `0a03d1437` Fix disclosure display elaboration on current main
- `bc9f236d7` Integrate disclosure list markers with the desktop layout fixes
- `69b724d79` Integrate disclosure markers with nested inline-block layout
- `2b21677b2` Integrate disclosure markers with the HTML slot display fix
- `d7e315b58` Merge pull request #945 from danbri/wip/css-disclosure-markers

