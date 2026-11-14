### Since the previous full run: +187 subtests (+0.0082 points)

Previous: `20261114T0825Z-wpt-linux-x86_64-gh43575698410a1`, core `6ecf053c7`, 85.7658%. This run: core `5cfcaf872`, 85.7741%; 15 commits between.
Tests that lost subtests: 52 (-1,135); that gained: 262 (+1,322). Page outcomes: CRASH +1, OK -2, STALL +1.

**Directories that fell** (6; the first 6)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| editing/run | 96,745 | 95,424 | 94,429 | -995 |
| css/css-align | 5,435 | 2,928 | 2,874 | -54 |
| html/rendering | 11,705 | 7,246 | 7,228 | -18 |
| css/css-ui | 2,416 | 1,450 | 1,448 | -2 |
| idle-detection | 93 | 1 | 0 | -1 |
| preload | 938 | 47 | 46 | -1 |

**Directories that rose** (20; the first 20)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/css-flexbox | 4,813 | 573 | 1,093 | +520 |
| css/css-anchor-position | 13,668 | 10,199 | 10,448 | +249 |
| css/css-grid | 16,015 | 2,846 | 3,081 | +235 |
| css/css-sizing | 6,523 | 2,077 | 2,160 | +83 |
| css/css-inline | 869 | 458 | 520 | +62 |
| css/cssom-view | 2,696 | 703 | 741 | +38 |
| css/css-position | 1,553 | 576 | 589 | +13 |
| css/css-contain | 499 | 169 | 181 | +12 |
| css/css-transforms | 5,513 | 680 | 691 | +11 |
| css/css-tables | 951 | 397 | 405 | +8 |
| shadow-dom | 14,707 | 14,108 | 14,116 | +8 |
| css/css-overflow | 1,209 | 476 | 480 | +4 |
| html/dom | 72,323 | 68,019 | 68,023 | +4 |
| css/css-break | 787 | 232 | 235 | +3 |
| css/css-values | 10,422 | 4,158 | 4,160 | +2 |
| svg/interact | 9,295 | 8,806 | 8,808 | +2 |
| css/css-conditional | 3,271 | 2,048 | 2,049 | +1 |
| editing/other | 16,742 | 12,020 | 12,021 | +1 |
| fetch | 13,288 | 4,486 | 4,487 | +1 |
| html/semantics | 22,364 | 12,956 | 12,957 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 16 directories, the first 16)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| editing/run | 995 | 1 |
| css/css-align | 62 | 20 |
| html/rendering | 22 | 4 |
| css/css-flexbox | 17 | 9 |
| css/css-position | 15 | 2 |
| css/css-sizing | 8 | 3 |
| css/css-grid | 3 | 2 |
| css/CSS2 | 2 | 2 |
| css/css-contain | 2 | 2 |
| css/css-transforms | 2 | 1 |
| css/css-ui | 2 | 1 |
| css/css-anchor-position | 1 | 1 |
| css/css-tables | 1 | 1 |
| css/cssom-view | 1 | 1 |
| idle-detection | 1 | 1 |
| preload | 1 | 1 |

**Tests that lost most** (the first 40 of 52)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /editing/run/justifycenter.html?1001-2000 | 995 | 0 | 1,000 |
| /html/rendering/non-replaced-elements/the-fieldset-and-legend-elements/legend-display.html | 52 | 36 | 80 |
| /css/css-align/abspos/safe-align-self-vrl.html | 12 | 0 | 24 |
| /css/css-position/position-absolute-in-inline-vertical-lr.html | 8 | 0 | 16 |
| /css/css-position/position-absolute-in-inline-dynamic.html | 8 | 1 | 9 |
| /css/css-align/abspos/safe-justify-self-htb.html | 6 | 0 | 24 |
| /css/css-align/abspos/safe-justify-self-vlr.html | 6 | 0 | 24 |
| /css/css-align/abspos/safe-justify-self-vrl.html | 6 | 0 | 24 |
| /css/css-flexbox/flexbox-ignores-first-letter.html | 12 | 6 | 12 |
| /html/rendering/non-replaced-elements/the-fieldset-and-legend-elements/legend-grid-flex-multicol.html | 5 | 1 | 5 |
| /css/css-flexbox/intrinsic-size/row-use-cases-001.html | 5 | 2 | 6 |
| /css/css-sizing/abspos-intrinsic-height-inset-percentage-child.html | 4 | 1 | 6 |
| /css/css-sizing/stretch/flex-basis-1.html | 4 | 1 | 5 |
| /css/css-align/abspos/align-self-default-overflow-htb-ltr-htb.html | 2 | 0 | 14 |
| /css/css-align/abspos/align-self-default-overflow-htb-ltr-vrl.html | 2 | 0 | 14 |
| /css/css-align/abspos/align-self-default-overflow-htb-rtl-htb.html | 2 | 0 | 14 |
| /css/css-align/abspos/align-self-default-overflow-htb-rtl-vrl.html | 2 | 0 | 14 |
| /css/css-align/abspos/align-self-default-overflow-vrl-ltr-htb.html | 2 | 0 | 14 |
| /css/css-align/abspos/align-self-default-overflow-vrl-ltr-vrl.html | 2 | 0 | 14 |
| /css/css-align/abspos/align-self-default-overflow-vrl-rtl-htb.html | 2 | 0 | 14 |
| /css/css-align/abspos/align-self-default-overflow-vrl-rtl-vrl.html | 2 | 0 | 14 |
| /css/css-align/abspos/justify-self-default-overflow-htb-ltr-htb.html | 2 | 0 | 14 |
| /css/css-align/abspos/justify-self-default-overflow-htb-ltr-vrl.html | 2 | 0 | 14 |
| /css/css-align/abspos/justify-self-default-overflow-htb-rtl-htb.html | 2 | 0 | 14 |
| /css/css-align/abspos/justify-self-default-overflow-htb-rtl-vrl.html | 2 | 0 | 14 |
| /css/css-align/abspos/justify-self-default-overflow-vrl-ltr-htb.html | 2 | 0 | 14 |
| /css/css-align/abspos/justify-self-default-overflow-vrl-ltr-vrl.html | 2 | 0 | 14 |
| /css/css-align/abspos/justify-self-default-overflow-vrl-rtl-htb.html | 2 | 0 | 14 |
| /css/css-align/abspos/justify-self-default-overflow-vrl-rtl-vrl.html | 2 | 0 | 14 |
| /css/css-flexbox/percentage-size-quirks-004.html | 3 | 1 | 4 |
| /css/css-grid/grid-lanes/grid-lanes-container-minimum-size-single-axis-scroll-container.html | 4 | 2 | 6 |
| /css/css-sizing/stretch/abspos-inline-containing-block.html | 2 | 0 | 2 |
| /css/css-transforms/transformed-table-section-containing-block.html | 2 | 0 | 2 |
| /css/css-ui/box-sizing-027.html | 2 | 0 | 2 |
| /css/CSS2/abspos/abspos-in-block-in-inline-in-relpos-inline-002.html | 1 | 0 | 2 |
| /css/CSS2/positioning/inline-static-position-001.html | 1 | 0 | 6 |
| /css/css-anchor-position/chained-anchor-scrolled.html | 1 | 0 | 1 |
| /css/css-contain/content-visibility/content-visibility-092.html | 1 | 0 | 1 |
| /css/css-contain/content-visibility/content-visibility-093.html | 1 | 0 | 1 |
| /css/css-flexbox/align-self-014.html | 1 | 0 | 1 |

**Commits between** (15)

- `292c20aac` Layout units: Int arithmetic of 1/64 px with an exact proportional split
- `a753bd4b0` Flex: resolving flexible lengths (CSS Flexbox 1 §9.7) on layout units, with theorems
- `2b59c1e4d` Flex: the exact-sum theorem of flexible lengths
- `d87cc1cdd` Flex: main-axis placement and cross-axis alignment with theorems
- `da8615510` Computed values of box alignment and flex, read through the property table
- `87793eae5` Layout interface: fragments, constraints and items; flex and alignment values in the cascade
- `1439aee47` Flex layout of a container's items through the formatting-context interface
- `63f6f1670` Flex containers are laid out: layoutTask dispatches on the inner display
- `da100926d` Flex: collecting items into lines, with the partition theorems
- `3e83373dd` Flex: multi-line rows (flex-wrap, wrap-reverse) and align-content
- `d6007cfb5` Positioning (relative, absolute, fixed), box-sizing and calc() lengths in layout
- `75631f8d8` offsetParent decided by the engine (CSSOM View §7), with a soundness theorem
- `5fbe34d49` Flex: the static position of an absolutely positioned child (§4.1)
- `e496c2f96` docs: design record of the layout interface, flex and positioning
- `5cfcaf872` Layout: loops for sums and a stable merge sort, for the tail-recursion gate

