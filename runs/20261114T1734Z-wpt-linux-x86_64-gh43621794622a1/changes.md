### Since the previous full run: +3,296 subtests (+0.1452 points)

Previous: `20261114T1500Z-wpt-linux-x86_64-gh43606148152a1`, core `64af7ef92`, 91.5114%. This run: core `c3d227a9f`, 91.6566%; 36 commits between.
Tests that lost subtests: 16 (-44); that gained: 200 (+3,340). Page outcomes: ERROR +1, OK +164, STALL +1, TIMEOUT -166.

**Directories that fell** (5; the first 5)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| quirks | 6,984 | 6,623 | 6,612 | -11 |
| webcodecs | 3,922 | 2,584 | 2,575 | -9 |
| html/semantics | 22,381 | 15,031 | 15,024 | -7 |
| css/css-conditional | 3,298 | 2,243 | 2,239 | -4 |
| custom-elements | 4,410 | 3,439 | 3,438 | -1 |

**Directories that rose** (35; the first 35)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/css-transitions | 3,439 | 1,412 | 2,707 | +1,295 |
| web-animations | 4,256 | 3,704 | 3,934 | +230 |
| touch-events | 987 | 723 | 951 | +228 |
| css/css-position | 1,553 | 1,158 | 1,335 | +177 |
| css/css-transforms | 5,513 | 5,120 | 5,289 | +169 |
| css/css-values | 10,428 | 4,753 | 4,901 | +148 |
| css/css-backgrounds | 6,236 | 5,752 | 5,899 | +147 |
| css/css-gaps | 4,157 | 3,970 | 4,098 | +128 |
| css/css-masking | 6,398 | 5,971 | 6,092 | +121 |
| css/css-sizing | 6,523 | 4,858 | 4,968 | +110 |
| css/CSS2 | 2,566 | 2,333 | 2,421 | +88 |
| css/css-logical | 1,366 | 1,078 | 1,162 | +84 |
| css/cssom | 4,463 | 3,528 | 3,604 | +76 |
| css/css-animations | 1,442 | 1,020 | 1,082 | +62 |
| css/css-fonts | 8,683 | 7,406 | 7,455 | +49 |
| css/css-text | 5,863 | 3,098 | 3,134 | +36 |
| html/rendering | 11,705 | 8,306 | 8,334 | +28 |
| css/css-properties-values-api | 1,394 | 940 | 967 | +27 |
| dom/events | 927 | 686 | 712 | +26 |
| css/css-multicol | 1,619 | 1,388 | 1,404 | +16 |
| css/filter-effects | 3,007 | 2,838 | 2,854 | +16 |
| css/css-variables | 594 | 413 | 425 | +12 |
| css/cssom-view | 2,696 | 1,178 | 1,189 | +11 |
| css/css-shapes | 7,527 | 7,189 | 7,198 | +9 |
| css/motion | 4,959 | 4,788 | 4,796 | +8 |
| scroll-animations | 2,167 | 921 | 929 | +8 |
| css/css-cascade | 1,759 | 1,318 | 1,322 | +4 |
| css/css-contain | 499 | 302 | 305 | +3 |
| css/css-ui | 2,416 | 2,225 | 2,228 | +3 |
| css/css-box | 982 | 918 | 920 | +2 |
| css/css-overscroll-behavior | 109 | 71 | 73 | +2 |
| css/css-viewport | 784 | 643 | 645 | +2 |
| css/css-anchor-position | 13,668 | 10,894 | 10,895 | +1 |
| intersection-observer | 440 | 208 | 209 | +1 |
| preload | 956 | 46 | 47 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 9 directories, the first 9)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| quirks/unitless-length | 11 | 3 |
| webcodecs | 9 | 1 |
| html/rendering | 7 | 3 |
| html/semantics | 7 | 2 |
| css/css-conditional | 4 | 2 |
| css/css-box | 2 | 1 |
| css/css-transitions | 2 | 2 |
| custom-elements/reactions | 1 | 1 |
| web-animations/interfaces | 1 | 1 |

**Tests that lost most** (the first 16 of 16)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /quirks/unitless-length/quirks.html | 1,407 | 1,398 | 1,590 |
| /webcodecs/image-decoder.https.any.html | 25 | 16 | 47 |
| /html/semantics/embedded-content/the-img-element/relevant-mutations.html | 78 | 72 | 113 |
| /html/rendering/non-replaced-elements/the-fieldset-and-legend-elements/legend.html | 48 | 44 | 56 |
| /css/css-box/animation/padding-left-composition.html | 40 | 38 | 40 |
| /css/css-conditional/container-queries/container-units-basic.html | 2 | 0 | 2 |
| /css/css-conditional/container-queries/container-units-content-box.html | 2 | 0 | 2 |
| /html/rendering/non-replaced-elements/the-fieldset-and-legend-elements/fieldset-default-style.html | 5 | 3 | 18 |
| /css/css-transitions/events-007.html | 1 | 0 | 1 |
| /css/css-transitions/non-rendered-element-001.html | 1 | 0 | 4 |
| /custom-elements/reactions/Animation.html | 2 | 1 | 3 |
| /html/rendering/non-replaced-elements/the-hr-element-0/hr.html | 5 | 4 | 18 |
| /html/semantics/embedded-content/the-img-element/list-of-available-images-does-not-coalesce-in-flight-requests.sub.tentative.html | 1 | 0 | 1 |
| /quirks/unitless-length/limited-quirks.html | 1,570 | 1,569 | 1,581 |
| /quirks/unitless-length/no-quirks.html | 1,570 | 1,569 | 1,581 |
| /web-animations/interfaces/Animatable/animate-no-browsing-context.html | 2 | 1 | 4 |

**Commits between** (36)

- `d48b559ee` tail-recursion allow list: the WebNN GPU tests' call-list helper (literal lists of a dozen calls)
- `123c6f343` docs: WPT plan progress table: the full runs of ca652ad26 (90.2%) and d8b9b0f8c (90.8%)
- `4c767fa1d` docs: WPT plan progress table: the full run of b323da1b0 (91.0%)
- `330f5958b` Grid modules import no Std (they use none of it): the Wasm engine links only parts of Std, and whole Std was an undefined initialize_Std at 
- `91cfa888f` The referrer source is DOM op 173: op 210 is the tenth computed property
- `93080b029` node_query ranges: Page.domOpRange names the ops Hosts.Dom.domOp answers (100 to 199) and the referrer source op (173); theorems domOpRange_
- `1b27ec4b4` Pointer capture is node_query op 42 (Page.pointerCaptureOp): op 220 is the twentieth computed property, so getComputedStyle(el).borderRightW
- `bf5afffb1` Animation values: radii of basic shapes are not below 0; currentcolor interpolates as the element's colour; normal and baseline as the lengt
- `bb3f017c6` Animations: a page holds at most 65,536 animations and effects; at the bound constructors answer QuotaExceededError and style starts none (p
- `4d940f640` Animation frames: the engine's part is the first callback of its frame; its callback number is not the workers' wake timer's
- `de62fdab1` Animation values: a side that is 0 takes the other value's type; transform-origin with a missing z
- `8f3cf7f45` Animation values: the blur of drop-shadow is not below 0 and a colour left out is currentcolor; background-size, mask-size and stroke-dashar
- `a3987c618` Web Animations: a range offset of an animation's options with a font-relative length is a TypeError
- `c80834769` Transitions: the before-change value of a longhand whose transition ran to its end is the end value, so it does not start again from its las
- `a3855bd89` Animations: a frame in which only the time moved makes no style change
- `fbd9d28ae` Design record: the measured checks of the animation engine
- `d44949653` Gap rule lists: two lists with an auto repeat combine when as many items stand before and after it
- `daf2fc2f6` Resolved transform-origin and perspective-origin: the percentages of a box whose size is not a length are of the laid out box
- `545ba7fe3` Animated font-size: keywords, percentages and em compute against the parent's font size
- `ecdb21360` Ended transitions are kept by element: a read and a removal are of one element's entries
- `e36df29d1` A class write styles the parent's subtree again, not the document
- `7195421e7` A page that listens for animation or transition events gets its style change in the frame
- `617806da9` Shapes that do not interpolate do not add; transform-origin keywords are percentages
- `6d00efa74` A style change looks at the written elements only; acts that wait keep the frame
- `2f20d71ad` The :has() scan of the class-write path counts a resolved :has() compound
- `568365b51` Generated content: the layout's styles hold the animated values
- `561ff93ef` The listen import marks a page that listens for animation or transition events
- `e35b1ce3c` docs: animations record: the listen import, animated values with generated content
- `7b7a6e194` One cascade for a layout: the layout answers the styles it was made with
- `2909ab19e` Style change: two equal computed style texts are not read apart
- `d86853ae1` docs: animations record: cascades per layout read
- `34589a7fe` Replaced animations and commitStyles() from the effect stack
- `04fdf5c5c` A style change that ends the page's last animation keeps the cancelled state
- `310fdb0d2` A script animation's value starts no transition; the engine reads computed line-height and insets
- `143c3d38d` The script session's view makes an element's matches once a measure
- `c3d227a9f` docs: animations record: the checks of the second batch

