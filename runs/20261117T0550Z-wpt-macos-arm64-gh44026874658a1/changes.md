### Since the previous full run: +4,311 subtests (+0.1897 points)

Previous: `20261117T0205Z-wpt-macos-arm64-gh43999731411a1`, core `bc4261b99`, 92.0180%. This run: core `fbd899f39`, 92.2078%; 58 commits between.
Tests that lost subtests: 36 (-131); that gained: 116 (+4,442). Page outcomes: ERROR -7, NO_RESULT -3, OK +21, TIMEOUT -11.

**Directories that fell** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| referrer-policy | 8,815 | 5,002 | 4,914 | -88 |
| webcodecs | 3,922 | 2,584 | 2,574 | -10 |
| preload | 956 | 243 | 242 | -1 |

**Directories that rose** (22; the first 22)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| wasm/core | 188,396 | 185,597 | 188,177 | +2,580 |
| html/rendering | 11,705 | 8,793 | 10,054 | +1,261 |
| html/dom | 72,400 | 69,541 | 69,727 | +186 |
| streams | 5,796 | 5,489 | 5,580 | +91 |
| selection/(root) | 33,918 | 33,581 | 33,664 | +83 |
| html/semantics | 22,381 | 15,118 | 15,188 | +70 |
| urlpattern | 3,266 | 2,994 | 3,030 | +36 |
| xhr | 2,344 | 1,787 | 1,820 | +33 |
| css/css-sizing | 6,743 | 5,080 | 5,098 | +18 |
| html/canvas | 6,251 | 3,686 | 3,698 | +12 |
| mixed-content | 2,281 | 1,309 | 1,319 | +10 |
| css/css-position | 1,605 | 1,362 | 1,371 | +9 |
| svg/painting | 672 | 418 | 424 | +6 |
| css/css-cascade | 1,759 | 1,322 | 1,326 | +4 |
| fetch | 13,288 | 8,808 | 8,811 | +3 |
| css/cssom | 4,463 | 3,606 | 3,608 | +2 |
| css/css-nesting | 126 | 39 | 40 | +1 |
| css/css-variables | 594 | 425 | 426 | +1 |
| html/browsers | 3,309 | 767 | 768 | +1 |
| intersection-observer | 440 | 212 | 213 | +1 |
| pointerevents | 2,749 | 1,584 | 1,585 | +1 |
| selection/textcontrols | 78 | 25 | 26 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 7 directories, the first 7)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| referrer-policy/gen | 56 | 15 |
| referrer-policy/4K | 20 | 6 |
| referrer-policy/4K+1 | 20 | 6 |
| referrer-policy/4K-1 | 20 | 6 |
| webcodecs | 10 | 1 |
| css/css-sizing | 4 | 1 |
| preload | 1 | 1 |

**Tests that lost most** (the first 36 of 36)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /webcodecs/image-decoder.https.any.html | 25 | 15 | 47 |
| /referrer-policy/4K+1/gen/top.http-rp/no-referrer-when-downgrade/script-tag.http.html | 12 | 6 | 12 |
| /referrer-policy/4K+1/gen/top.http-rp/unsafe-url/script-tag.http.html | 12 | 6 | 12 |
| /referrer-policy/4K-1/gen/top.http-rp/no-referrer-when-downgrade/script-tag.http.html | 12 | 6 | 12 |
| /referrer-policy/4K-1/gen/top.http-rp/unsafe-url/script-tag.http.html | 12 | 6 | 12 |
| /referrer-policy/4K/gen/top.http-rp/no-referrer-when-downgrade/script-tag.http.html | 12 | 6 | 12 |
| /referrer-policy/4K/gen/top.http-rp/unsafe-url/script-tag.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/top.http-rp/origin-when-cross-origin/fetch.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/top.http-rp/origin/xhr.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/top.meta/always/script-tag.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/top.meta/origin-when-cross-origin/fetch.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/top.meta/origin-when-crossorigin/xhr.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/top.meta/unset/script-tag.http.html | 12 | 6 | 12 |
| /css/css-sizing/contain-intrinsic-size/contain-intrinsic-size-logical-003.html | 4 | 0 | 48 |
| /referrer-policy/gen/top.meta/origin-when-crossorigin/a-tag.http.html | 3 | 0 | 4 |
| /referrer-policy/gen/top.meta/strict-origin-when-cross-origin/svg-a-tag.http.html | 3 | 0 | 4 |
| /referrer-policy/4K+1/gen/top.http-rp/strict-origin-when-cross-origin/fetch.http.html | 2 | 0 | 2 |
| /referrer-policy/4K+1/gen/top.meta/origin-when-cross-origin/fetch.http.html | 2 | 0 | 2 |
| /referrer-policy/4K+1/gen/top.meta/same-origin/script-tag.http.html | 2 | 0 | 2 |
| /referrer-policy/4K+1/gen/top.meta/unset/fetch.http.html | 2 | 0 | 2 |
| /referrer-policy/4K-1/gen/top.http-rp/strict-origin-when-cross-origin/fetch.http.html | 2 | 0 | 2 |
| /referrer-policy/4K-1/gen/top.meta/origin-when-cross-origin/fetch.http.html | 2 | 0 | 2 |
| /referrer-policy/4K-1/gen/top.meta/same-origin/script-tag.http.html | 2 | 0 | 2 |
| /referrer-policy/4K-1/gen/top.meta/unset/fetch.http.html | 2 | 0 | 2 |
| /referrer-policy/4K/gen/top.http-rp/strict-origin-when-cross-origin/fetch.http.html | 2 | 0 | 2 |
| /referrer-policy/4K/gen/top.meta/origin-when-cross-origin/fetch.http.html | 2 | 0 | 2 |
| /referrer-policy/4K/gen/top.meta/same-origin/script-tag.http.html | 2 | 0 | 2 |
| /referrer-policy/4K/gen/top.meta/unset/fetch.http.html | 2 | 0 | 2 |
| /referrer-policy/gen/req.attr/no-referrer-when-downgrade/a-tag.http.html | 2 | 0 | 4 |
| /referrer-policy/gen/req.attr/strict-origin-when-cross-origin/iframe-tag.http.html | 2 | 0 | 12 |
| /referrer-policy/gen/req.attr/strict-origin/svg-a-tag.http.html | 2 | 0 | 4 |
| /referrer-policy/gen/top.http-rp/no-referrer/iframe-tag.http.html | 2 | 0 | 12 |
| /referrer-policy/gen/top.http-rp/origin/a-tag.http.html | 2 | 0 | 4 |
| /referrer-policy/gen/top.http-rp/strict-origin/svg-a-tag.http.html | 2 | 0 | 4 |
| /referrer-policy/gen/top.meta/no-referrer/iframe-tag.http.html | 2 | 0 | 12 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |

**Commits between** (58)

- `f58e1aa33` OWL 2 profiles: EL, QL and RL checkers over the structural specification, with the RL grammar proved
- `55c8a8970` OWL profiles: one-element intersections, QL follows the production for irreflexive, functional-style fallback, bounded nesting
- `87aa471eb` docs: OWL 2 profile identification record (method, theorems, result, each failing unit, the other OWL populations)
- `b4a930462` ledger: OWL 2 profile identification row
- `a2075c9aa` StructureFromRdf: a restriction predicate on an IRI subject is an error, not passed over
- `e70f1b626` lean-scoreboard: jobs for XPath 4.0, XQuery 4.0, XSLT 4.0, XSD 1.1, RELAX NG, XInclude and Canonical XML
- `ffbc8dad0` spec-suites: the XML family runners as recorded suites (XPath 4.0, XQuery 4.0, XSLT 4.0, XSD 1.1, RELAX NG, XInclude, Canonical XML); QT4 ro
- `623a8febe` wpt-runs skill: the lean-xml group of release-tests
- `bb6b44e57` SHACL 1.2 node expressions: the two sht:Validate tests of constraints/ run with l4shacl's reader and validator (the probe's main moves to Ha
- `aa2c5c0e1` ShaclProbe: an importable module of the Harness library; its entry is ShaclProbe.run (a namespaced main clashed with the executables' main)
- `a8876ef1e` URL parser as the standard's state machine (step/run), with a proved bound of 3n + 16 rounds
- `365fd53d3` URLPattern: compile regular expressions with the v flag, as the Standard does
- `369ebcf9e` URL parser: run is irreducible, so proofs about callers of parseUrl do not unfold the machine
- `27d198efe` Merge remote-tracking branch 'origin/main' into wip/url-theorems
- `1fb815fc7` Merge remote-tracking branch 'origin/main' into wip/qt4
- `58ce03cab` Lean memory-management overhead: analysis record, idiom and steering microbenchmarks, opt-in ThinLTO of the native engine with the runtime's
- `5190c6042` XSLT: transform keeps its four parameters; the source URI goes through transformAt
- `586076f2f` Layout: iframe and video as replaced boxes of the default object size
- `696f967ab` Merge pull request #525 from danbri/wip/url-theorems
- `762867872` WasmVM: memory64 and table64 (64-bit address types)
- `522989677` Images: an image/svg+xml answer is an image, with the natural size of its root
- `f2471c70c` Canvas 2D: WebIDL name and length of the context's and Path2D's methods
- `d124a0677` CSSOM: insertRule and deleteRule cost the rule, not the sheet
- `2c19b65c1` Hints: hspace and vspace percentages; the border hint above the UA input border
- `d6a30bc16` Style: the user agent's unicode-bidi rules of HTML 15.3.5
- `e8106755c` Hub: an XSLT result keeps its syntax on the page, so books-xslt4.xml shows
- `57a3b1e8d` QT4 rows per family: the XQuery run reads all fourteen qt4tests families, the parser adds a row per family (l4qt4) or test directory (l4xslt
- `1217260fb` foafnaut launcher: newest main build by lookup over all release pages; clearer modes (0.37.1)
- `0b85737bb` BubblePopJS: the undo log's logging branch as a call (noteObjOn, noteEnvOn), not inlined at each heap write
- `58cd50d46` BubblePopJS: direct typed-array reads and writes for the two- and four-byte integer types
- `4dafdd6bf` lean-scoreboard: the long XML jobs list each failing and unsupported case with its reason (--list-fails, --verbose)
- `1f9e8f178` BubblePopJS: big property maps and the indexed environment record are read with no Option cell
- `88172d982` BubblePopJS: updateObj specialised for its function; liveLen inlined; element size by a match
- `f3d4ce31a` BubblePopJS regular expressions: the search over start positions as a recursion (execFast)
- `77027f06a` Merge remote-tracking branch 'origin/main' into wip/wptbulk
- `9a61ea409` sizes: a media type is not a media condition; calc(0) is a zero length in a media feature
- `723688f19` lean-scoreboard: QT4 test sets capped at 180 s, not 60 (a slow set that finishes is not counted as failures)
- `094a8d872` Merge pull request #559 from danbri/wip/leanmem
- `5a8f810b7` binary-budget.json: leanjs on macOS arm64 11,868,032 -> 11,483,024 B (the undo log's logging branch as a call)
- `aaf06eacc` Merge pull request #561 from danbri/wip/latestfix
- `96d02bfdf` Style: computedFrom keeps its doc comment (uaUnicodeBidi went between them)
- `517f9f793` Style: replacedHints keeps its doc comment (hintEdge went between them)
- `199f0b2e6` img decode(): a new request rejects the old request's decode promises
- `3aed835e0` Merge remote-tracking branch 'origin/main' into wip/qt4
- `55b421545` Merge main into wip/bbc-cssom (PR 560)
- `47802c23c` Merge pull request #562 from danbri/wip/wptbulk
- `bf492b8ab` foafnaut launcher: at most 10 release pages; a refused later page is a note (0.37.2)
- `71121d2e1` Merge pull request #566 from danbri/wip/latestfix2
- `4969f19c8` Merge pull request #564 from danbri/wip/hotpath-a
- `20d6c545f` Merge pull request #560 from danbri/wip/bbc-cssom
- `2d551f032` Merge pull request #563 from danbri/wip/wpthtml-canvasidl
- `ebd360f25` Merge pull request #569 from danbri/wip/wpthtml-bidi
- `a09db6329` Merge pull request #570 from danbri/wip/wpthtml-hints
- `78d1baca0` Merge pull request #568 from danbri/wip/wpthtml-svgimg
- `6d4f88c0a` Merge pull request #567 from danbri/wip/wpthtml
- `41bc8588e` Merge pull request #520 from danbri/wip/owl-conformance
- `aeeb46c7e` skills/ci-runner: the Mac release poll's fallback triggers; fresh lag in the alert
- `fbd899f39` Merge pull request #578 from danbri/wip/macalways2-docs

