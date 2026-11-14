### Since the previous full run: +213,458 subtests (+9.4059 points)

Previous: `20261114T0213Z-wpt-macos-arm64-gh43544901505a1`, core `25c3a4510`, 74.0349%. This run: core `19fb349c1`, 83.4407%; 54 commits between.
Tests that lost subtests: 299 (-1,353); that gained: 10,335 (+214,811). Page outcomes: CRASH +4, ERROR -2217, NO_RESULT -186, OK +3831, SKIP engine -859, SKIP other +843, TIMEOUT -1416.

**Directories that fell** (5; the first 5)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| upgrade-insecure-requests | 982 | 349 | 236 | -113 |
| mixed-content | 2,281 | 1,187 | 1,126 | -61 |
| css/css-env | 76 | 31 | 22 | -9 |
| workers | 1,598 | 376 | 367 | -9 |
| html/cross-origin-embedder-policy | 596 | 91 | 89 | -2 |

**Directories that rose** (301; the first 40)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| editing/run | 96,745 | 6,076 | 95,374 | +89,298 |
| css/css-typed-om | 13,449 | 16 | 11,848 | +11,832 |
| css/css-color | 12,752 | 1,345 | 11,476 | +10,131 |
| shadow-dom | 14,707 | 8,569 | 14,070 | +5,501 |
| css/css-anchor-position | 13,668 | 4,857 | 10,188 | +5,331 |
| third_party/test262 | 53,833 | 30,345 | 35,340 | +4,995 |
| html/semantics | 22,364 | 3,197 | 7,823 | +4,626 |
| html/dom | 72,323 | 61,753 | 65,948 | +4,195 |
| css/css-shapes | 7,527 | 1,690 | 5,413 | +3,723 |
| css/css-values | 10,422 | 861 | 4,155 | +3,294 |
| css/css-fonts | 8,683 | 1,232 | 4,434 | +3,202 |
| custom-elements | 4,404 | 23 | 3,185 | +3,162 |
| css/css-images | 3,601 | 681 | 3,104 | +2,423 |
| css/css-grid | 16,015 | 520 | 2,846 | +2,326 |
| referrer-policy | 8,815 | 1,238 | 3,564 | +2,326 |
| css/css-align | 5,435 | 754 | 2,928 | +2,174 |
| css/selectors | 6,266 | 675 | 2,830 | +2,155 |
| editing/other | 16,742 | 78 | 2,203 | +2,125 |
| css/css-masking | 6,398 | 127 | 2,247 | +2,120 |
| quirks | 6,984 | 5 | 2,123 | +2,118 |
| css/cssom | 4,463 | 815 | 2,855 | +2,040 |
| html/syntax | 8,984 | 3,333 | 5,284 | +1,951 |
| css/css-backgrounds | 6,236 | 242 | 2,126 | +1,884 |
| mimesniff | 3,886 | 744 | 2,624 | +1,880 |
| fetch | 13,288 | 2,544 | 4,354 | +1,810 |
| dom/(root) | 2,759 | 117 | 1,864 | +1,747 |
| svg/interact | 9,295 | 5,275 | 6,860 | +1,585 |
| css/css-text | 5,863 | 1,653 | 3,154 | +1,501 |
| css/motion | 4,959 | 105 | 1,453 | +1,348 |
| css/css-ui | 2,416 | 165 | 1,445 | +1,280 |
| css/css-sizing | 6,523 | 844 | 2,077 | +1,233 |
| webstorage | 1,291 | 3 | 1,228 | +1,225 |
| css/CSS2 | 2,566 | 650 | 1,826 | +1,176 |
| svg/(root) | 1,754 | 44 | 1,211 | +1,167 |
| css/css-gaps | 4,157 | 350 | 1,322 | +972 |
| css/filter-effects | 3,007 | 116 | 918 | +802 |
| css/css-view-transitions | 1,445 | 21 | 786 | +765 |
| svg/types | 1,136 | 151 | 893 | +742 |
| html/webappapis | 3,665 | 1,189 | 1,893 | +704 |
| css/css-multicol | 1,619 | 42 | 701 | +659 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 49 directories, the first 40)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| css/css-color | 212 | 3 |
| css/css-box | 187 | 2 |
| css/css-values | 170 | 17 |
| third_party/test262 | 129 | 129 |
| mixed-content/gen | 113 | 33 |
| upgrade-insecure-requests/gen | 113 | 24 |
| css/css-align | 103 | 3 |
| css/css-gaps | 44 | 3 |
| css/css-grid | 44 | 3 |
| fetch/api | 26 | 4 |
| workers | 18 | 1 |
| css/css-text | 17 | 7 |
| css/css-env | 13 | 2 |
| css/filter-effects | 13 | 1 |
| html/rendering | 13 | 4 |
| css/css-overflow | 12 | 3 |
| css/css-ui | 12 | 7 |
| custom-elements/registries | 12 | 5 |
| css/css-font-loading | 11 | 1 |
| css/css-backgrounds | 10 | 2 |
| css/css-borders | 9 | 5 |
| css/css-link-params | 9 | 2 |
| css/CSS2 | 6 | 1 |
| encoding | 5 | 2 |
| css/cssom-view | 4 | 1 |
| fetch/range | 4 | 2 |
| css/css-display | 3 | 1 |
| css/css-lists | 3 | 3 |
| css/css-mixins | 3 | 1 |
| css/css-overscroll-behavior | 3 | 1 |
| css/css-scroll-snap | 3 | 2 |
| css/cssom | 3 | 2 |
| forced-colors-mode | 3 | 1 |
| html/semantics | 3 | 3 |
| css/css-fonts | 2 | 2 |
| css/css-multicol | 2 | 2 |
| css/css-ruby | 2 | 2 |
| css/css-variables | 2 | 1 |
| html/cross-origin-embedder-policy | 2 | 1 |
| css/compositing | 1 | 1 |

**Tests that lost most** (the first 40 of 299)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /css/css-color/parsing/color-valid-color-layers-function.html | 160 | 0 | 170 |
| /css/css-box/animation/padding-interpolation.html | 108 | 14 | 144 |
| /css/css-box/animation/margin-interpolation.html | 108 | 15 | 144 |
| /css/css-values/attr-all-types.html | 150 | 111 | 175 |
| /css/css-align/self-alignment/place-self-shorthand-006.html | 156 | 120 | 195 |
| /css/css-color/parsing/alpha-color-parsing-valid.html | 37 | 1 | 45 |
| /css/css-align/content-distribution/place-content-shorthand-006.html | 134 | 100 | 156 |
| /css/css-align/default-alignment/place-items-shorthand-006.html | 132 | 99 | 168 |
| /css/css-values/random-serialize.tentative.html | 30 | 1 | 71 |
| /css/css-gaps/parsing/gap-decorations-rule-shorthand-valid.html | 63 | 35 | 75 |
| /css/css-grid/parsing/grid-template-columns-repeat-intrinsic-valid.tentative.html | 21 | 0 | 21 |
| /css/css-grid/parsing/grid-template-rows-repeat-intrinsic-valid.tentative.html | 21 | 0 | 21 |
| /css/css-values/random-item-valid.html | 21 | 1 | 21 |
| /workers/importscripts_mime_local.any.worker.html | 18 | 0 | 48 |
| /css/css-color/parsing/color-valid-contrast-color-function.html | 16 | 0 | 17 |
| /css/css-values/urls/url-request-modifiers-serialize.sub.html | 17 | 1 | 23 |
| /css/css-values/random-item-serialize.html | 15 | 1 | 15 |
| /css/filter-effects/parsing/filter-parsing-valid.html | 78 | 65 | 87 |
| /css/css-env/syntax.tentative.html | 14 | 2 | 25 |
| /css/css-values/tree-counting/calc-sibling-function-parsing.html | 25 | 13 | 47 |
| /css/css-font-loading/fontfaceset-load-css-wide-keywords.html | 12 | 1 | 24 |
| /css/css-values/ident-function-parsing.html | 15 | 4 | 19 |
| /css/css-gaps/parsing/gap-decorations-rule-shorthand-from-longhands.tentative.html | 12 | 2 | 16 |
| /css/css-values/attr-argument-grammar.html | 18 | 9 | 18 |
| /css/css-backgrounds/parsing/background-image-valid.html | 11 | 3 | 15 |
| /css/css-text/parsing/hanging-punctuation-valid.html | 18 | 10 | 18 |
| /fetch/api/response/response-stream-disturbed-5.any.html | 8 | 0 | 12 |
| /fetch/api/response/response-stream-disturbed-5.any.worker.html | 8 | 0 | 12 |
| /html/rendering/non-replaced-elements/the-fieldset-and-legend-elements/fieldset-default-style.html | 16 | 8 | 18 |
| /css/css-overflow/parsing/line-clamp-valid.html | 11 | 4 | 25 |
| /css/CSS2/visufx/animation/visibility-interpolation.html | 75 | 69 | 134 |
| /css/css-gaps/parsing/gap-decorations-bidirectional-shorthands.html | 7 | 1 | 14 |
| /css/css-link-params/link-parameters-valid.html | 6 | 0 | 6 |
| /mixed-content/gen/iframe-inherit.http-rp/opt-in/link-css-tag.https.html | 6 | 0 | 8 |
| /mixed-content/gen/iframe-inherit.http-rp/opt-in/object-tag.https.html | 6 | 0 | 8 |
| /mixed-content/gen/iframe-inherit.http-rp/opt-in/picture-tag.https.html | 6 | 0 | 8 |
| /mixed-content/gen/iframe-inherit.meta/unset/link-css-tag.https.html | 6 | 0 | 8 |
| /mixed-content/gen/iframe-inherit.meta/unset/picture-tag.https.html | 6 | 0 | 8 |
| /mixed-content/gen/srcdoc-inherit.http-rp/opt-in/link-css-tag.https.html | 6 | 0 | 8 |
| /mixed-content/gen/srcdoc-inherit.http-rp/opt-in/picture-tag.https.html | 6 | 0 | 8 |

**Commits between** (54)

- `7ba0e14dd` skills/wpt-runs: main on Linux every 20 minutes; a Linux row is the score while no macOS row exists
- `e1f37e4d3` Editing: execCommand and the queryCommand methods, inline formatting commands
- `fa4b3c77a` Editing: block commands and the delete and insert commands
- `e97afa1f9` Editing: #guard tests from the WPT cases; delete strips emptied wrappers first; insertParagraph keeps inline formatting on an empty line
- `1eff10a3a` Editing: the input event of execCommand; focus() of an editing host moves the selection into it
- `724110003` docs: design record of the editing commands (execCommand)
- `6f8437b19` skills/wpt-runs: 12 Linux shards, branch checks at most 8 runners, the engine build starts the full run
- `b4f54419f` BubblePopJS: String position arguments, sticky match cost, Proxy construct; named access on the Window; Web IDL interface members
- `1693e86e9` Web Storage: localStorage and sessionStorage, partitioned by origin, in memory
- `f8102f1ce` SVG documents: a .svg URL is read as XML and its script elements run
- `d33fefdd6` SVG: the paint 'transparent'; text takes pointer events on its character cells
- `23be8924a` Theorems: JSON.parse and the strict parser, refused WebCrypto algorithms, CORS wildcard
- `11e8494cd` Fetch API objects: Headers, Request and Response by the standard; MIME types in Lean
- `74eba3e24` Frames: postMessage to a frame's own window; document.open, write and close
- `18b6f128d` WPT runner: load a page's web fonts for its layout, as the browser host does
- `cffa307da` Blob URLs: URL.createObjectURL and revokeObjectURL, each URL its origin's; SVG element style
- `427d1a941` Desktop host: the layout a page's scripts read has the page's images and failed sheets
- `22d715960` Referrer Policy and CSP source lists as proved decision functions (not yet called)
- `6b442d48e` create_node: the kind-15 dispatch in a function of its own (call_writes_within reads call's cases)
- `1d85b2264` Custom elements (HTML 4.13); ARIA and popover rows of the reflection table; HTMLElement for plain and custom names
- `541284703` Scripts that a script inserts run (HTML 4.12.1); Document.dir and legacy colours; .xml documents are XML
- `7214ec580` HTML elements of XML documents have their HTML interfaces
- `081a5c5d2` IDL attributes that reflect elements: the ARIA element attributes, popoverTargetElement, commandForElement
- `f5260f342` Form controls: collections, select and option, textarea, labels, text selection, typed values, constraint validation
- `4dcafd76d` wpt-score run: start a runner again after any early exit, not only a non-zero one
- `6fd8dde22` FileReader: readAsText, readAsArrayBuffer, readAsBinaryString, readAsDataURL, abort
- `4a21c53a7` Frames: a navigation to a blob: URL is answered in the engine
- `826f6300f` Blob URLs: Range requests
- `866c01fe2` Worker scripts: X-Content-Type-Options: nosniff is decided in Lean
- `48890fb1e` docs: networking, storage and SVG record (first measured round)
- `13360fc45` SVG DOM: the element interfaces and the reflected values of SVG 2 section 4
- `edfea549f` SVG DOM: interface members are enumerable; no helper on SVGTransform's prototype
- `a60341f00` document.cookie: a script-only cookie jar in Lean (Net/Cookies, web_api ops 96 and 97)
- `9374d90fe` docs: cookies and the SVG DOM in the networking and SVG record
- `eba95b9e5` CSS values: tokenizer, exact numerics with calc(), value definition syntax matcher, property data
- `5672621db` CSS values in the engine: style declaration block, CSS.supports and computed values from one property table
- `596e9bbcc` CSS values: omissible commas, grammar-cased function names, display short forms, keyword canonical forms; no derived Repr on nested types
- `35e541b1c` CSSOM style sheets: rules of a sheet text, insertRule, deleteRule, selectorText, rule style
- `88c3b195d` CSS values: stack use bounded by nesting, not by input length
- `a19fcbc9c` CSS values: <position> with its canonical and computed forms; the font shorthand
- `611479d9e` CSS Typed OM: typed values, numeric types and arithmetic, style property maps
- `45c91b7ec` Computed value of one property: one table pass, and only the inline declarations that can set it are parsed
- `40f8a9f6e` getComputedStyle: a declared absolute margin, padding or size limit is answered through the property table (calc() and all units)
- `4187b562c` CSS math functions: sin, cos, tan, asin, acos, atan, atan2, pow, sqrt, hypot, log, exp as rational approximations; pi and e
- `d63abb093` CSS values: the table indexed once, grammars read once; table corrections from the WPT parsing corpus
- `a51006529` BubblePopJS: ES modules (parse, link, evaluate)
- `012491efd` Module scripts: fetch graphs in CORS mode, run them after classic scripts (BubblePopJS)
- `8aa80425d` Page scripts: a classic script that does not parse reports its SyntaxError at the window
- `087ea4b78` Module scripts: the document tests expect a page with a module script to be accepted
- `20cfe4dbc` BubblePopJS: for await (async iteration statements) and %AsyncFromSyncIteratorPrototype%
- `8f1c642e7` BubblePopJS: the property key of a String value is never a private name's or a Symbol's key
- `8225cbf92` BubblePopJS: thenable jobs, async generators, Annex B block functions, super targets, dense-array limit
- `6090a8a40` Named properties of the Window: the host sets the engine's slot through a built-in
- `19fb349c1` docs: WPT plan progress table: 72.4%, 74.0%, 77.5% full runs

