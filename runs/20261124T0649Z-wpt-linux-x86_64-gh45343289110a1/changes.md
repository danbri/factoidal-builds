### Since the previous full run: +20 subtests (+0.0009 points)

Previous: `20261124T0426Z-wpt-linux-x86_64-gh45326348155a1`, core `c22de52e6`, 92.6357%. This run: core `cfc667991`, 92.6366%; 27 commits between.
Tests that lost subtests: 13 (-23); that gained: 29 (+43). Page outcomes: CRASH +1, TIMEOUT -1.

**Directories that fell** (5; the first 5)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 3,974 | 2,616 | 2,608 | -8 |
| css/css-contain | 499 | 310 | 307 | -3 |
| css/css-break | 787 | 590 | 588 | -2 |
| css/css-conditional | 3,298 | 2,236 | 2,235 | -1 |
| preload | 956 | 243 | 242 | -1 |

**Directories that rose** (14; the first 14)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/CSS2 | 2,566 | 2,444 | 2,464 | +20 |
| css/cssom | 4,465 | 3,757 | 3,759 | +2 |
| third_party/test262 | 53,838 | 46,250 | 46,252 | +2 |
| css/css-align | 5,473 | 4,456 | 4,457 | +1 |
| css/css-flexbox | 4,933 | 3,890 | 3,891 | +1 |
| css/css-fonts | 8,740 | 7,851 | 7,852 | +1 |
| css/css-multicol | 1,626 | 1,425 | 1,426 | +1 |
| css/css-overflow | 1,215 | 786 | 787 | +1 |
| css/css-position | 1,605 | 1,361 | 1,362 | +1 |
| css/css-scroll-snap | 864 | 501 | 502 | +1 |
| css/cssom-view | 2,722 | 1,557 | 1,558 | +1 |
| editing/other | 16,742 | 13,796 | 13,797 | +1 |
| html/semantics | 22,496 | 15,584 | 15,585 | +1 |
| intersection-observer | 449 | 236 | 237 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 8 directories, the first 8)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| webcodecs | 8 | 1 |
| css/css-contain | 4 | 2 |
| css/css-writing-modes | 4 | 3 |
| css/css-break | 2 | 2 |
| html/semantics | 2 | 2 |
| css/CSS2 | 1 | 1 |
| css/css-conditional | 1 | 1 |
| preload | 1 | 1 |

**Tests that lost most** (the first 13 of 13)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /webcodecs/image-decoder.https.any.html | 16 | 8 | 47 |
| /css/css-contain/contain-style-dynamic-001.html | 2 | 0 | 4 |
| /css/css-contain/content-visibility/content-visibility-style-containment-001.html | 5 | 3 | 8 |
| /css/css-writing-modes/orthogonal-parent-shrink-to-fit-001.html | 11 | 9 | 24 |
| /css/CSS2/normal-flow/block-in-inline-client-rects-001.html | 1 | 0 | 3 |
| /css/css-break/box-decoration-break-clone-block-in-inline-001.html | 3 | 2 | 5 |
| /css/css-break/offset-top-block-in-inline.html | 1 | 0 | 1 |
| /css/css-conditional/container-queries/container-type-containment.html | 1 | 0 | 4 |
| /css/css-writing-modes/orthogonal-parent-shrink-to-fit-001m.html | 1 | 0 | 1 |
| /css/css-writing-modes/orthogonal-parent-shrink-to-fit-001u.html | 1 | 0 | 1 |
| /html/semantics/embedded-content/the-img-element/list-of-available-images-does-not-coalesce-in-flight-requests.sub.tentative.html | 1 | 0 | 1 |
| /html/semantics/interactive-elements/the-dialog-element/modal-dialog-scroll-height.html | 1 | 0 | 1 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |

**Commits between** (27)

- `fe3c8c62a` Rendering: CSS counters (counter-reset, -increment, -set, counter(), counters()); not yet built
- `b3110704f` Rendering: counters build; apply_other covers the counter properties
- `c9bddc9f6` BubblePopJS: Number and BigInt toString(radix) write digits 16 to 35 as a to z (was '*'), and fractions; reftest-render REFTEST_DUMP_DIR
- `b610a2c38` Rendering: em and % in font-size are of the parent's size, not of the size the user agent gives the element (h1 {font-size: 4em} was 128 px)
- `a1fa36595` Rendering: a sized or painted block inside an inline keeps its box (line-wide atomic box); not yet built
- `d44740f14` Rendering: blockBreak ends a line only when it holds content; checks that a painted block inside a link is painted
- `b2be65aa6` Foafnaut: SVG redraw checks the cheap size tests before reading the file, and reads each background's natural size once per URL (62 of 90 sa
- `39dc19a9e` Foafnaut: strings a script gives the DOM are bounded at 16 MiB (was 64 KiB: Wikipedia's scripts stopped with DOM budget exceeded)
- `75ef4a665` Brotli: RFC 7932 decoder in Lean, with the dictionary, transforms and context table (WIP, tests next)
- `8ef8691a4` Brotli: read the tree-select bit only for NSYM 4; 307 Python-brotli vectors decode
- `b201144e6` Brotli: build-time tests (libbrotli vectors at quality 0, 5 and 11, dictionary and transform checks against google/brotli, refusals)
- `790947278` Woff2: WOFF2 to sfnt in Lean (header, directory, Brotli stream, glyf/loca and hmtx transforms); WIP, tests next
- `86fd526fa` tools/fonts/woff2_vectors.py: make WOFF2 files from third_party/fonts and compare the Lean reader's sfnt with fontTools
- `4541c634c` Woff2: build-time tests (Noto Sans subset as WOFF2 in three forms, byte-equal to google/woff2; UIntBase128, 255UInt16, triplets, refusals); 
- `ffabc2ec0` Fonts: read WOFF2 where WOFF 1.0 is read (Font.read, @font-face format woff2) [WIP: build running]
- `6b21d618b` Woff2Tests: SfntProfile.Font.read reads the three WOFF2 files; wiring builds (SfntProfile, FontFaceRuleTests, FontPolicyTests)
- `7b425e7b9` Woff2: sort the table directory with a loop, not Array.qsort (tail-recursion gate)
- `87d8089f3` Merge remote-tracking branch 'origin/wip/woff2' into wip/747-text-spacing
- `ee1714190` Rendering: reversed() counters start at minus the sum of their increments; a zero-height block inside an inline collapses through (no block 
- `5fa2b3c97` LabHygiene: formal extern baseline 27 to 32, the Prim.Bytes primitives that WOFF2's Brotli decoder reaches through Codec.Zstd
- `3ee4be580` Foafnaut: the list-item counter of HTML lists (ol start, reversed, li value); reversed start minus the last increment; issue 747
- `ab3232eb6` Foafnaut: picture maps made once, not again for each picture the layout asks for (BBC News: about 40% of layout time)
- `de76b30b0` Foafnaut: an undecorated inline wrapper gives its block children to the parent flow (GitHub's header in react-partial lost its flex layout)
- `af660821a` tools/limit-audit.py: list Foafnaut's resource limits and which report a hit (105, none yet); issue 865
- `e0b71c7e0` Foafnaut: report resource limits that a page reaches (WebAccept.LimitHit), first two: maxBackgroundImages, maxVectorRedraws; issue 865
- `1907daf5c` Foafnaut: report the @font-face limit (maxFaces, 64) when a page passes it; issue 865
- `cfc667991` Foafnaut: report boxes whose background image needs more than maxBackgroundTiles tiles (Layout.tileGrid shared by paint and report); issue 8

