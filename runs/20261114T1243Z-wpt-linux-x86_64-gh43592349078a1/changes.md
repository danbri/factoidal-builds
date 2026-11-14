### Since the previous full run: +2,976 subtests (+0.1311 points)

Previous: `20261114T1154Z-wpt-linux-x86_64-gh43589970966a1`, core `2c2dc8f7d`, 90.0525%. This run: core `ca652ad26`, 90.1836%; 45 commits between.
Tests that lost subtests: 35 (-309); that gained: 333 (+3,285). Page outcomes: CRASH +1, OK +1, STALL -1, TIMEOUT -1.

**Directories that fell** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/css-fonts | 8,683 | 7,189 | 7,093 | -96 |
| fetch | 13,288 | 7,427 | 7,425 | -2 |
| infrastructure | 285 | 80 | 79 | -1 |
| preload | 938 | 47 | 46 | -1 |

**Directories that rose** (13; the first 13)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/css-grid | 16,015 | 5,608 | 8,436 | +2,828 |
| IndexedDB | 5,853 | 4,966 | 5,049 | +83 |
| html/rendering | 11,705 | 7,282 | 7,354 | +72 |
| css/css-contain | 499 | 251 | 297 | +46 |
| html/infrastructure | 1,664 | 757 | 777 | +20 |
| html/webappapis | 3,665 | 2,624 | 2,633 | +9 |
| webmessaging | 304 | 147 | 153 | +6 |
| css/css-sizing | 6,523 | 4,861 | 4,864 | +3 |
| html/editing | 868 | 511 | 514 | +3 |
| css/css-align | 5,435 | 3,456 | 3,458 | +2 |
| html/dom | 72,323 | 68,477 | 68,479 | +2 |
| css/css-flexbox | 4,813 | 3,576 | 3,577 | +1 |
| third_party/test262 | 53,833 | 38,062 | 38,063 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 8 directories, the first 8)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| css/css-grid | 203 | 27 |
| css/css-fonts | 96 | 1 |
| css/css-sizing | 4 | 2 |
| fetch/metadata | 2 | 1 |
| html/semantics | 1 | 1 |
| infrastructure/testdriver | 1 | 1 |
| preload | 1 | 1 |
| third_party/test262 | 1 | 1 |

**Tests that lost most** (the first 35 of 35)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /css/css-fonts/animations/system-fonts.html | 348 | 252 | 588 |
| /css/css-grid/grid-definition/grid-inline-template-columns-rows-resolved-values-001.tentative.html | 36 | 9 | 76 |
| /css/css-grid/grid-definition/grid-template-columns-rows-resolved-values-001.tentative.html | 36 | 9 | 76 |
| /css/css-grid/alignment/grid-align-baseline-flex-002.html | 24 | 0 | 48 |
| /css/css-grid/grid-items/grid-items-minimum-width-vertical-lr-002.html | 14 | 0 | 44 |
| /css/css-grid/grid-items/grid-items-minimum-width-vertical-rl-002.html | 14 | 0 | 44 |
| /css/css-grid/alignment/grid-align-baseline-line-clamp-002.tentative.html | 12 | 0 | 24 |
| /css/css-grid/alignment/grid-align-baseline-line-clamp-003.tentative.html | 12 | 0 | 24 |
| /css/css-grid/alignment/grid-align-baseline-flex-004.html | 8 | 0 | 16 |
| /css/css-grid/alignment/grid-align-baseline-grid-002.html | 6 | 0 | 12 |
| /css/css-grid/alignment/grid-align-baseline-grid-003.html | 6 | 0 | 12 |
| /css/css-grid/alignment/grid-align-baseline-multicol-002.html | 6 | 0 | 12 |
| /css/css-grid/alignment/grid-align-baseline-multicol-003.html | 6 | 0 | 12 |
| /css/css-grid/alignment/grid-align-baseline-overflow-002.html | 7 | 2 | 12 |
| /css/css-grid/alignment/grid-align-baseline-overflow-003.html | 7 | 2 | 12 |
| /css/css-grid/alignment/grid-align-baseline-vertical-mixed.html | 5 | 1 | 11 |
| /css/css-grid/alignment/grid-align-baseline-vertical.html | 5 | 1 | 11 |
| /css/css-grid/alignment/grid-self-alignment-safe-overflow.html | 4 | 0 | 6 |
| /css/css-grid/grid-model/grid-container-ignores-first-letter-001.html | 12 | 9 | 12 |
| /css/css-grid/grid-model/grid-container-ignores-first-line-001.html | 12 | 9 | 12 |
| /css/css-grid/alignment/grid-align-baseline-fieldset-002.html | 2 | 0 | 4 |
| /css/css-grid/alignment/grid-align-baseline-fieldset-003.html | 2 | 0 | 4 |
| /css/css-grid/alignment/grid-align-baseline-table-002.html | 2 | 0 | 4 |
| /css/css-grid/alignment/grid-align-baseline-table-003.html | 2 | 0 | 4 |
| /css/css-grid/layout-algorithm/grid-intrinsic-tracks-item-with-border-001.html | 4 | 2 | 4 |
| /css/css-sizing/stretch/stretch-alias-min-inline-size-001.tentative.html | 12 | 10 | 46 |
| /css/css-sizing/stretch/stretch-min-inline-size-001.html | 12 | 10 | 46 |
| /fetch/metadata/worker.https.sub.html | 2 | 0 | 5 |
| /css/css-grid/alignment/grid-align-baseline-001.html | 1 | 0 | 6 |
| /css/css-grid/alignment/grid-align-baseline-002.html | 1 | 0 | 6 |
| /css/css-grid/subgrid/subgrid-baseline-007.html | 2 | 1 | 12 |
| /html/semantics/scripting-1/the-noscript-element/non-html-noscript.html | 1 | 0 | 1 |
| /infrastructure/testdriver/delete_all_cookies.html | 2 | 1 | 2 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |
| /third_party/test262/test/language/expressions/class/elements/syntax/early-errors/grammar-privatename-whitespace-error-static-field.test262.html | 1 | 0 | 1 |

**Commits between** (45)

- `ef8b0d869` wpt-score.py tree: a wdspec name brings webdriver/tests/support/ and the package files above it (__init__.py, conftest.py, pytest.ini)
- `8aaf92458` Grid: placement, track sizing, explicit grid and alignment as pure modules (CSS Grid 2 §7, §8.5, §11, §12)
- `fd6ce6dcb` Grid: computed values of the grid properties through the property table (GridStyle)
- `65e9402ee` Grid layout of a container's items through the formatting-context interface
- `077fc9649` Grid: resolved grid-template-columns/rows are the used track sizes (§7.2.6)
- `d849056db` Design record: CSS Grid Layout
- `9ae4d4f41` Grid: an absolutely positioned box whose containing block is a grid container is placed in the grid area its lines name (CSS Grid 2 §9.1)
- `e6e0745a3` Grid: self-start and self-end align an item by its own direction (CSS Box Alignment 3 §4.1)
- `5f7a1e560` Grid: percentage rows of a container with no definite height are resolved against the height they gave it (§7.2.1)
- `57fc1c471` Grid: baseline alignment of items in their rows (§11.6); fragments carry their first baseline
- `fc97893af` Grid: a percentage row gap of a container with no definite height is resolved against the height it gave the container (CSS Box Alignment 3 
- `5fe0a5a03` Design record: grid's positioned boxes, baselines and percentage rows
- `94231db8c` Engine build: GridResolved is linked (a root of the core module list)
- `cc4413285` Grid placement: the slot found is the earliest free one (firstFreeCol_earliest, firstFreeRow_earliest, fitInRow_earliest)
- `ca5c6556b` Grid placement: placing the placed areas again gives the same areas (placeAll_idem)
- `19ed1137a` Design record: placement's earliest-slot and idempotence theorems
- `4395ca134` Grid: an absolutely positioned child that names grid lines has the start of its grid area as its static position (§9.1, §9.2)
- `307967e35` Grid: the static position of an absolutely positioned child is the start of its containing block, auto lines included (the padding box)
- `959c5f7d1` Grid: only an absolutely positioned child takes its grid area's start as static position (not a fixed one)
- `8e3b8a642` Grid: a subgrid stretches in its subgridded axes (CSS Grid 2 §9: subgrid box alignment)
- `3c3fb63eb` Grid: an item stretched in rows of fixed size is laid out once at its final height (a nested flex or grid container is not measured and laid
- `d79f54058` Grid: an auto-repeated track whose max is below its min counts as its min (§7.2.3.2), with fixedSize_ge_min
- `2d4025ce5` Grid: baseline alignment only in a horizontal writing mode; build script lists GridLayoutTests and GridResolved after the rebase on main
- `67529e03a` network_gaps_test.ts: the issue 374 test runs a page on the engine and checks which network globals its script sees with the network off and
- `187bf90c8` Images held reduced within the document's pixel budget; SVG files as img
- `373e23e0c` Fixtures: original pages for the constructs that made live pages look wrong
- `ff7399995` Hosts: a document's images, tab icon, web fonts and linked sheets go through the engine's subresource steps
- `6d4618522` A supplied sheet whose link a script removed is left out; the page is drawn
- `837abc4e4` Window: the sheets and images of elements that scripts make or change are fetched
- `5ddb08047` Rendering.FontSynthesis: font-weight and font-style values, and the synthesized bold and oblique faces
- `a4ddc7af1` The image store of a page is made once before its scripts start
- `ba04c5ac6` SVG image files: a picture of at most 65,536 pixels; the record of the day's later findings
- `99999ee47` Inline SVG reads past an alt attribute
- `a2d94aec4` noscript is not rendered
- `2d9919cf6` The hidden attribute: the element is not rendered
- `45c72e760` A closed details shows its summary only; details, summary, hgroup and search are blocks
- `05f31d2b2` closedDetailsContent: the rule of a closed details as a function, with theorems
- `6b5ec4ef3` A details element's summary is looked for among its first 64 children
- `65291792d` docs: real pages record: what is not rendered, and the bounds of page-driven work
- `41e5cf27c` font-weight and font-style in the layout cascade; bold and oblique text is drawn
- `bf18a3952` Inline SVG with a percentage height is sized: the height is auto (CSS 2.1 10.5)
- `e3c926661` font-weight and font-style stay out of htmlProperties
- `a76e2eaa8` Layout: the glyph paint's structure instances on one line
- `f4e774b16` BubblePopJS: Number.prototype methods refuse a Date (thisNumberValue); IndexedDB serialises a Date before the primitive wrappers
- `ca652ad26` IndexedDB and Cookie Store event handler attributes: accessors named 'get onX'/'set onX', brand-checked

