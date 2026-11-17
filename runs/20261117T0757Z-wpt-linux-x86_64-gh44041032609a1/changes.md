### Since the previous full run: +217 subtests (+0.0096 points)

Previous: `20261117T0701Z-wpt-linux-x86_64-gh44035516460a1`, core `33992d9e7`, 92.4486%. This run: core `efd07bd22`, 92.4581%; 4 commits between.
Tests that lost subtests: 1 (-1); that gained: 46 (+218). Page outcomes: ERROR -15, STALL -2, TIMEOUT +17.

**Directories that rose** (15; the first 15)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/cssom-view | 2,714 | 1,195 | 1,275 | +80 |
| html/syntax | 8,984 | 8,625 | 8,679 | +54 |
| selection/(root) | 33,918 | 33,640 | 33,664 | +24 |
| html/browsers | 3,309 | 779 | 797 | +18 |
| intersection-observer | 440 | 215 | 231 | +16 |
| webcodecs | 3,922 | 2,569 | 2,574 | +5 |
| css/css-writing-modes | 421 | 218 | 222 | +4 |
| dom/events | 927 | 714 | 718 | +4 |
| webidl | 838 | 647 | 651 | +4 |
| css/css-scroll-anchoring | 98 | 8 | 10 | +2 |
| html/semantics | 22,381 | 15,190 | 15,192 | +2 |
| css/css-contain | 499 | 309 | 310 | +1 |
| css/css-tables | 951 | 533 | 534 | +1 |
| pointerevents | 2,749 | 1,585 | 1,586 | +1 |
| service-workers | 3,262 | 1,393 | 1,394 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 1 directories, the first 1)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| css/css-scroll-snap | 1 | 1 |

**Tests that lost most** (the first 1 of 1)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /css/css-scroll-snap/snap-events/scrollsnapchanging/scrollsnapchanging-on-user-root-scroll.tentative.html | 1 | 0 | 7 |

**Commits between** (4)

- `0d2c0a349` CSSOM View bindings: Screen, MediaQueryList(Event), the window's scroll and screen offsets as attributes, scrollingElement
- `d402cf5f9` Window operations scroll/scrollTo/scrollBy/moveTo/moveBy/resizeTo/resizeBy/matchMedia: enumerable own properties of the global, with their a
- `5d92ffb11` Merge remote-tracking branch 'origin/main' into cssomview
- `efd07bd22` Merge pull request #586 from danbri/wip/wptbulk-cssomview

