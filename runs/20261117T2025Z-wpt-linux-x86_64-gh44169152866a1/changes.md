### Since the previous full run: +27 subtests (+0.0012 points)

Previous: `20261117T1937Z-wpt-linux-x86_64-gh44160584615a1`, core `3438c02d9`, 92.6306%. This run: core `080473762`, 92.6317%; 11 commits between.
Tests that lost subtests: 14 (-17); that gained: 14 (+44). Page outcomes: OK +1, STALL -4, TIMEOUT +3.

**Directories that fell** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/css-writing-modes | 421 | 222 | 219 | -3 |
| pointerevents | 2,749 | 1,586 | 1,584 | -2 |
| css/css-overflow | 1,215 | 726 | 725 | -1 |
| html/rendering | 11,705 | 10,083 | 10,082 | -1 |

**Directories that rose** (11; the first 11)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/css-flexbox | 4,933 | 3,790 | 3,798 | +8 |
| webcodecs | 3,922 | 2,568 | 2,575 | +7 |
| css/css-color | 12,760 | 12,360 | 12,364 | +4 |
| css/css-sizing | 6,743 | 5,098 | 5,101 | +3 |
| css/css-values | 10,428 | 6,209 | 6,212 | +3 |
| shadow-dom | 14,720 | 14,126 | 14,129 | +3 |
| css/cssom | 4,463 | 3,754 | 3,756 | +2 |
| IndexedDB | 5,853 | 5,503 | 5,504 | +1 |
| css/cssom-view | 2,714 | 1,277 | 1,278 | +1 |
| html/editing | 868 | 551 | 552 | +1 |
| html/semantics | 22,381 | 15,572 | 15,573 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 7 directories, the first 7)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| html/rendering | 5 | 5 |
| compat | 4 | 1 |
| css/css-writing-modes | 3 | 3 |
| pointerevents | 2 | 2 |
| css/css-flexbox | 1 | 1 |
| css/css-inline | 1 | 1 |
| css/css-overflow | 1 | 1 |

**Tests that lost most** (the first 14 of 14)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /compat/webkit-box-item-shrink-001.html | 8 | 4 | 20 |
| /css/css-flexbox/select-as-flex-item-with-overflow.html | 1 | 0 | 1 |
| /css/css-inline/baseline-source/baseline-source-last-textarea-001.tentative.html | 11 | 10 | 12 |
| /css/css-overflow/unicode-bidi-plaintext-scroll-direction.html | 1 | 0 | 8 |
| /css/css-writing-modes/forms/button-appearance-native-computed-style.html | 2 | 1 | 18 |
| /css/css-writing-modes/forms/file-input-computed-style.html | 1 | 0 | 5 |
| /css/css-writing-modes/forms/select-appearance-native-computed-style.html | 1 | 0 | 3 |
| /html/rendering/non-replaced-elements/the-fieldset-and-legend-elements/legend-align.html | 8 | 7 | 10 |
| /html/rendering/widgets/field-sizing-input-number.html | 3 | 2 | 9 |
| /html/rendering/widgets/field-sizing-select-contain-size.html | 1 | 0 | 2 |
| /html/rendering/widgets/placeholder-scroll.html | 1 | 0 | 2 |
| /html/rendering/widgets/select-wrap-no-spill.optional.html | 1 | 0 | 1 |
| /pointerevents/pointerevent_touch-action-inherit_child-auto-child-none_touch.html | 1 | 0 | 1 |
| /pointerevents/pointerevent_touch-action-inherit_child-pan-x-child-pan-y_touch.html | 1 | 0 | 1 |

**Commits between** (11)

- `9bc7b4a6c` Rendering: form controls show their text, undrawn mask icons drop their box, align and center hints, sub and sup raised
- `79b74437c` Rendering: text clipped to nothing for screen readers is not painted
- `643984098` Style: alignHints_plain states the align value through alignValue (simp rewrote the inline form)
- `a8be81a21` Style: String.ofList for the control text (as the rest of the module)
- `2b679b691` Style: finishEffects_layout in place of a theorem that did not parse
- `953a67613` Layout controlItems: parenthesise the placeholder colour (the if-else swallowed the next field)
- `f294513c3` Layout controlItems: name the grey and the position before the structure update (did not parse)
- `2d4e99869` Rendering tests: a button's glyphs use the control font size (13.333px); guard measured with lake build
- `5665aebbf` WebRepaint.sameShape: the seven new Computed fields (masked, shift, rise, centerBlocks, clip*) take part
- `7cf076a9e` Merge main into wip/look-sites: one alignHints (the parent-aware one), with main's th centring
- `080473762` Merge pull request #591 from danbri/wip/look-sites

