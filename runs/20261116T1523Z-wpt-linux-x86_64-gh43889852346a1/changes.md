### Since the previous full run: +4 subtests (+0.0002 points)

Previous: `20261116T1016Z-wpt-linux-x86_64-gh43847381345a1`, core `0391fe0d0`, 91.9774%. This run: core `ddf6be714`, 91.9776%; 12 commits between.
Tests that lost subtests: 3 (-6); that gained: 3 (+10). Page outcomes: OK -1, STALL +1.

**Directories that fell** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| shadow-dom | 14,720 | 14,129 | 14,126 | -3 |
| webcodecs | 3,922 | 2,578 | 2,576 | -2 |
| html/rendering | 11,705 | 8,792 | 8,791 | -1 |

**Directories that rose** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/semantics | 22,381 | 15,171 | 15,180 | +9 |
| fetch | 13,288 | 8,816 | 8,817 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 3 directories, the first 3)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| shadow-dom/declarative | 3 | 1 |
| webcodecs | 2 | 1 |
| html/rendering | 1 | 1 |

**Tests that lost most** (the first 3 of 3)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /shadow-dom/declarative/declarative-shadow-dom-repeats.html | 3 | 0 | 3 |
| /webcodecs/image-decoder.https.any.html | 19 | 17 | 47 |
| /html/rendering/widgets/placeholder-scroll.html | 1 | 0 | 2 |

**Commits between** (12)

- `cdb310373` Hub: Web platform lists Textnaut, start, demos, stress, settings, notebook, conformance; Hub copies of openly licensed pages open in place i
- `17c7b1bc9` Test results: an index page for the site toolbar's Test Results link (it answered 404)
- `19eac6182` Settings in every UI: Textnaut's s key opens a settings screen (engine build, page scripts, strictness); the Hub passes the system's dark mo
- `dae92ae22` Hub README: Hub copies, how they are made, served and added
- `3cc24f393` Chrome: a flat look by default (light and dark faces, rounded address field with a focus ring, vector line icons, settings button in a circl
- `14ba800e3` Web platform page: link the data and documents conformance page
- `86b7fea8f` Chrome: line icons 20 points and a little heavier (readable at 1x); copy licence line spacing
- `cce8aea38` Chrome: circles as 16-sided polygons, square caps and mitred joins (no curve to flatten; the flat look cost 1.5 to 3 times the classic chrom
- `6cfb23d66` Chrome: the gear is one filled shape with the hub as a hole; each icon's lines are one stroked path (at most two primitives an icon)
- `aa42acc12` Chrome: icon lines are filled quadrilaterals in one path (nonzero), not strokes
- `336905e13` Start page: a Books, texts and essays group and a Small tools group, 32 more plain sites (probed with Textnaut 0.1.4 native), 10 more Hub co
- `ddf6be714` scroll_layers_check: chrome rows apart; a sloped or round chrome edge sampled by the other rule (issue 1269) is counted as that expected fai

