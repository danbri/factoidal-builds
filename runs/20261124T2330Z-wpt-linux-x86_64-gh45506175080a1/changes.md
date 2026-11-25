### Since the previous full run: -2 subtests (-0.0001 points)

Previous: `20261124T2222Z-wpt-linux-x86_64-gh45496612893a1`, core `d63d0983f`, 92.6316%. This run: core `f22156198`, 92.6315%; 16 commits between.
Tests that lost subtests: 6 (-8); that gained: 5 (+6). Page outcomes: NO_RESULT +1, OK -1, STALL +1, TIMEOUT -1.

**Directories that fell** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 4,168 | 2,641 | 2,638 | -3 |
| fetch | 13,290 | 8,808 | 8,807 | -1 |
| html/semantics | 22,498 | 15,589 | 15,588 | -1 |
| preload | 956 | 243 | 242 | -1 |

**Directories that rose** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| infrastructure | 290 | 111 | 113 | +2 |
| html/rendering | 11,722 | 10,120 | 10,121 | +1 |
| xhr | 2,344 | 1,833 | 1,834 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 5 directories, the first 5)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| webcodecs | 3 | 1 |
| html/semantics | 2 | 2 |
| fetch/metadata | 1 | 1 |
| html/rendering | 1 | 1 |
| preload | 1 | 1 |

**Tests that lost most** (the first 6 of 6)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /webcodecs/image-decoder.https.any.html | 13 | 10 | 47 |
| /fetch/metadata/generated/element-img.https.sub.html | 19 | 18 | 45 |
| /html/rendering/widgets/button-layout/display-other.html | 2 | 1 | 18 |
| /html/semantics/embedded-content/the-img-element/list-of-available-images-does-not-coalesce-in-flight-requests.sub.tentative.html | 1 | 0 | 1 |
| /html/semantics/popovers/popover-attribute-all-elements.html | 1,083 | 1,082 | 1,101 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |

**Commits between** (16)

- `94a0e0b3d` Render details disclosure glyphs as list markers
- `62976cab1` Include the added defaults in the user-agent rule count guard
- `0a03d1437` Fix disclosure display elaboration on current main
- `bc9f236d7` Integrate disclosure list markers with the desktop layout fixes
- `69b724d79` Integrate disclosure markers with nested inline-block layout
- `65b705213` Balance short text runs using their ordinary soft wrap opportunities
- `2b21677b2` Integrate disclosure markers with the HTML slot display fix
- `5891acdee` Guard hover repaint against changed line balancing
- `d7e315b58` Merge pull request #945 from danbri/wip/css-disclosure-markers
- `e17ec447b` Build the HTML image lookup before entering layout
- `c919dc1cb` Integrate balanced heading wrapping with the disclosure layout
- `79feaf006` Merge pull request #958 from danbri/wip/balanced-heading-wrap
- `384c4b619` Merge pull request #964 from danbri/wip/eager-html-picture-map
- `90856f584` wpt-reftests: exclude 5 css/WOFF2 tests with defective test data (issue 883)
- `e1dd6b894` Wikidata explanations hub page: add Parallax set-browsing tiers
- `f22156198` Merge pull request #971 from danbri/claude/wikidata-parallax

