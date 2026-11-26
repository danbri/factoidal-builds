### Since the previous full run: +354 subtests (+0.0156 points)

Previous: `20261126T0052Z-wpt-linux-x86_64-gh45729185845a1`, core `2bf8a0f56`, 92.6471%. This run: core `8a782f5af`, 92.6627%; 55 commits between.
Tests that lost subtests: 5 (-11); that gained: 134 (+365). Page outcomes: CRASH +1, OK +8, STALL -4, TIMEOUT -5.

**Directories that fell** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| pointerevents | 2,780 | 1,588 | 1,585 | -3 |
| css/css-text | 5,863 | 4,458 | 4,456 | -2 |
| preload | 956 | 243 | 242 | -1 |

**Directories that rose** (25; the first 25)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/interaction | 842 | 342 | 397 | +55 |
| html/semantics | 22,523 | 15,711 | 15,752 | +41 |
| css/selectors | 6,266 | 5,737 | 5,775 | +38 |
| css/css-sizing | 6,744 | 5,190 | 5,221 | +31 |
| html/rendering | 11,729 | 10,121 | 10,150 | +29 |
| css/css-pseudo | 903 | 468 | 496 | +28 |
| shadow-dom | 14,726 | 14,133 | 14,154 | +21 |
| css/css-grid | 16,034 | 11,286 | 11,303 | +17 |
| css/css-multicol | 1,626 | 1,426 | 1,443 | +17 |
| css/css-position | 1,605 | 1,364 | 1,376 | +12 |
| css/css-flexbox | 4,933 | 3,897 | 3,907 | +10 |
| css/css-values | 10,473 | 6,260 | 6,269 | +9 |
| css/css-align | 5,473 | 4,457 | 4,465 | +8 |
| html/canvas | 6,289 | 3,723 | 3,731 | +8 |
| css/css-overflow | 1,215 | 792 | 799 | +7 |
| css/css-fonts | 8,740 | 7,857 | 7,863 | +6 |
| css/css-rhythm | 183 | 155 | 161 | +6 |
| css/css-cascade | 1,759 | 1,339 | 1,344 | +5 |
| css/CSS2 | 2,566 | 2,465 | 2,469 | +4 |
| third_party/test262 | 53,838 | 46,352 | 46,355 | +3 |
| compat | 143 | 102 | 103 | +1 |
| editing/run | 96,809 | 95,622 | 95,623 | +1 |
| html/editing | 869 | 552 | 553 | +1 |
| mathml | 4,329 | 1,577 | 1,578 | +1 |
| resize-observer | 135 | 81 | 82 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 5 directories, the first 5)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| css/css-flexbox | 4 | 1 |
| pointerevents | 3 | 1 |
| css/css-text | 2 | 1 |
| preload | 1 | 1 |
| third_party/test262 | 1 | 1 |

**Tests that lost most** (the first 5 of 5)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /css/css-flexbox/flex-base-size-ignores-min-max-width-002.html | 4 | 0 | 4 |
| /pointerevents/pointerevent_capture_mouse.html | 3 | 0 | 8 |
| /css/css-text/line-breaking/line-breaking-atomic-nowrap-001.html | 2 | 0 | 4 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |
| /third_party/test262/test/built-ins/RegExp/property-escapes/generated/Script_-_Balinese.test262.html | 1 | 0 | 1 |

**Commits between** (55)

- `e572b5e1e` Distinguish visible keyboard focus from ordinary focus
- `239a9eba0` Share the DOM element-state bound across the host and renderer
- `05b906f7a` Carry visible focus through the DOM state transport
- `b26f4a1ac` Close element-state replay proof after reducing Except.map
- `01cb82032` Size replaced aspect ratios in the selected box
- `795451733` Keep auto fallback ratios in content coordinates for blocks
- `3ea38de4d` Preserve authored dimensions on undecoded image placeholders
- `708f463fb` Keep canvas bitmap dimensions out of preferred CSS sizes
- `e2f0ee0ad` Keep focus indication through blank-area clicks and input type changes
- `405b990bd` Correct natural image dimensions for the selected source density
- `79478835a` Prove canvas hint projection without unfolding other replacements
- `d8dc3b49f` Decode percent-encoded data URLs for static images
- `0e3e942e4` Size responsive image boxes and paint from each selected density
- `17a9e3e56` Advance document focus on Tab and reverse on Shift+Tab
- `2b27cddb1` Transfer image size constraints using the source ratio after density rounding
- `b60d89398` Share undecoded image sizing code with the merged aspect ratio changes
- `88ef40aec` Check data URL decoding separately from image format validation
- `e05848eb8` Lay out text and inline separators at zero font size
- `b655b3a26` Document focus visibility alongside the current DOM state flags
- `bb5598bf9` Merge b655b3a26a835554dd3147cd6501a2fca1e46546 into d2d98b99e84431d094beae4c913608a9add1db60
- `acc055db2` Check responsive image natural dimensions on current main
- `930b90119` Check sequential document focus on current main
- `206025fa0` Validate focus modality on current core main
- `e13ef7303` Compile and link the URL byte decoder in the standalone SVG engine
- `fd443a1d5` Validate authored image placeholder sizing on current core main
- `f8948bc09` Integrate main and share the computed border-image update
- `9cb5a5487` Validate the tested responsive image and Tab changes in one release package
- `ba9fff6e0` Check repaired SVG image loading with measured main runtime budget
- `01b5ddd46` Check decoded SVG and responsive image sizing together on current main
- `ca4e730dd` Check SVG and responsive images on current main
- `42d67f393` Check authored placeholders, responsive image layout and SVG loading together
- `3306df8f7` Verify canvas bitmap dimensions and zero-size text together on main
- `06a376500` Package keyboard focus and image getters with landed text editing
- `3dbc5ebcb` BubblePopJS: Number::toString of fractions by Ryū on 64-bit words (issue 1076, work in progress)
- `0f91d8d63` BubblePopJS: fast toFixed, toPrecision, toExponential; shortest digits for integers from 2^53 (issue 1076, work in progress)
- `322224071` NumFmt: put the toExponential doc comment on expo (issue 1076)
- `798db2dbe` BubblePopJS: Number::toString by Ryū and 64-bit toFixed, toPrecision, toExponential (issue 1076)
- `eae24321b` NumFmt.fixedOf: zero with more than 19 fraction digits takes the exact path; differential test aborts on panic (issue 1076)
- `1f8106a89` Correct canvas bitmap sizing and zero-size text layout (#1102)
- `b18e8b00c` Canvas 2D: rectangle and polygon coverage with no Float boxed per pixel (issue 1098)
- `b57e4a146` Fix responsive image sizing, placeholders and percent-encoded SVG (#1107)
- `63aab0c83` BubblePopJS: Float64Array and Float32Array element writes as machine-word shifts, proved equal to the reference (issue 1098)
- `a9b6e4614` Vendor the lean-verify skill (hirosassa/lean-verify, MIT) for trial
- `9e3b317e9` Revert the BubblePopJS Float64/Float32 write commit 63aab0c83 (issue 1098)
- `edce62338` lean-verify provenance: run it with the pinned toolchain (ELAN_TOOLCHAIN); checks pass
- `6591b0a04` Foafnaut: held keys, page focus on commit, canvas font family (WIP, not built)
- `3cdd75151` Design record: held keys, page focus on commit, canvas font family (issues 1074, 1077, 1075)
- `108e973a3` HostKeys: key phase guards name the WebDriver raw keys
- `e0d8aacf1` particle_rex_test: focus on commit (issue 1077)
- `feed530df` particle_rex_test: canvas text with a page @font-face face (issue 1075)
- `73e1a1ef1` Fix Tab navigation, focus visibility and responsive image size getters (#1083)
- `67fd597bd` Concurrency record 2b: proofs about external code (checkers, certificates, verified crypto)
- `e341ad9a1` Hub: keys go to the page first; the scroll command is the default action (issue 1139)
- `2cedec9dc` Foafnaut Tor: stream isolation per partition, new identity, periodic state save, memory quota
- `8a782f5af` Foafnaut Tor worker: strict IP literal check, so no name can reach a resolver

