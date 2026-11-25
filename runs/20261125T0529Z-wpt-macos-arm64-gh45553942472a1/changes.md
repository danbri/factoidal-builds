### Since the previous full run: +21 subtests (+0.0009 points)

Previous: `20261125T0009Z-wpt-macos-arm64-gh45515773668a1`, core `384c4b619`, 92.6332%. This run: core `e586b539d`, 92.6341%; 55 commits between.
Tests that lost subtests: 5 (-5); that gained: 20 (+26). Page outcomes: CRASH +1, OK -2, TIMEOUT +1.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/css-text | 5,863 | 4,460 | 4,458 | -2 |
| preload | 956 | 243 | 242 | -1 |

**Directories that rose** (9; the first 9)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| third_party/test262 | 53,838 | 46,276 | 46,285 | +9 |
| css/cssom-view | 2,722 | 1,560 | 1,565 | +5 |
| css/css-position | 1,605 | 1,362 | 1,364 | +2 |
| css/css-ruby | 109 | 61 | 63 | +2 |
| css/css-writing-modes | 421 | 229 | 231 | +2 |
| css/CSS2 | 2,566 | 2,464 | 2,465 | +1 |
| css/css-anchor-position | 13,670 | 11,544 | 11,545 | +1 |
| css/css-overflow | 1,215 | 791 | 792 | +1 |
| css/css-sizing | 6,743 | 5,138 | 5,139 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 3 directories, the first 3)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| css/css-text | 2 | 2 |
| third_party/test262 | 2 | 2 |
| preload | 1 | 1 |

**Tests that lost most** (the first 5 of 5)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /css/css-text/overflow-wrap/overflow-wrap-anywhere-span-002.html | 1 | 0 | 1 |
| /css/css-text/overflow-wrap/overflow-wrap-break-word-span-002.html | 1 | 0 | 1 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |
| /third_party/test262/test/built-ins/Temporal/ZonedDateTime/prototype/round/throws-without-parameter.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/statements/for/S12.6.3_A12_T2.test262.html | 1 | 0 | 1 |

**Commits between** (55)

- `0cf10082c` Size HTML buttons by their border boxes by default
- `6f8ca4d1b` Paint repeating CSS backgrounds with one bitmap record
- `01aac5cd2` Use a Lean identifier for the repeat flag
- `871da79e7` Read Array and TypedArray at indices after coercion
- `38168746d` Integrate HTML button sizing with the GOV.UK heading fix
- `2a69ebffd` Keep pointer link requests within the renderer transport limit
- `90856f584` wpt-reftests: exclude 5 css/WOFF2 tests with defective test data (issue 883)
- `4099e3dbe` Include repeat axes when comparing retained bitmap paints
- `e1dd6b894` Wikidata explanations hub page: add Parallax set-browsing tiers
- `f22156198` Merge pull request #971 from danbri/claude/wikidata-parallax
- `046e86e2b` Merge pull request #967 from danbri/wip/array-at-ordered-read
- `530319505` Hub: Wikidata queries as set browsing (Parallax view), one page per query
- `0fccf0b6e` Foafnaut: report web-font and @import limits (issue 865); restyle reasons and link sheets (issue 871)
- `4fd549461` Keep generated quotes with their nowrap words
- `3481cebb0` Integrate repeating backgrounds with current limit diagnostics
- `7b81d5bd1` Let headings balance below completed floats
- `00d053ce6` Merge pull request #963 from danbri/wip/html-button-border-box
- `23b95d44c` Preserve background image CSS-wide shorthand values
- `86d610b0e` Merge pull request #970 from danbri/wip/bounded-pointer-link-transport
- `d97a9405c` Record the bounded CSS import walker in the release audit
- `d54ee7157` Merge pull request #980 from danbri/wip/bounded-css-import-audit
- `4e8b173fd` Merge pull request #966 from danbri/wip/compact-css-image-repeat
- `762216329` Integrate the settled GOV.UK search control and balanced headings
- `8f560793c` Merge pull request #975 from danbri/wip/w3c-nowrap-quote-line-break
- `5cd7bef63` Use more of the raster budget for large SVG images
- `17242ba7f` Merge pull request #979 from danbri/wip/background-shorthand-wide-image
- `aa2c4b775` Merge pull request #974 from danbri/claude/wikidata-parallax-page
- `fc246f938` Add the Wikidata query explainer and set-browsing classifier
- `120c5bc89` Reuse element keys within a partial CSS restyle
- `005ca9bb6` Generate the fuel lemma for the shared Array and TypedArray at operation
- `c9c6f48bd` Font clusters: byte-to-character lookup in an array, not a tree map
- `894b4d8a3` Restyle after child writes: sheet signature, and :has()-safe child writes (issue 871)
- `11c6771da` Draw content: url() images in ::before and ::after (issue 874, part 1)
- `04d672fdf` Process Object.fromEntries entries before advancing the iterator
- `0defebb2c` Check SVG raster sizes at fractional divisors
- `d38eaddb3` Merge pull request #978 from danbri/wip/balance-below-floats
- `102942a00` Keep CSS text runs intact across inline elements
- `ead665451` Merge pull request #987 from danbri/wip/array-at-fuel-mono
- `ad69cf2a7` Merge pull request #988 from danbri/wip/object-from-entries-iterator-order
- `5de0dc09b` Open Foafnaut at the requested window size
- `6fe1473fc` Merge pull request #989 from danbri/wip/inline-text-boundary-wrap
- `94399281c` Merge pull request #993 from danbri/wip/foafnaut-initial-window-size
- `78276916b` Merge pull request #986 from danbri/wip/partial-restyle-element-keys
- `1b851ac72` Merge pull request #983 from danbri/wip/svg-image-budget-resolution
- `84b19a75a` Position outside list markers at the float-adjusted first line
- `853a7c275` Avoid loading the Wasm document engine in native workers
- `bcbda8cce` Merge pull request #998 from danbri/wip/native-worker-without-wasm
- `856332018` Merge pull request #997 from danbri/wip/float-aware-list-marker
- `56e741b7e` tree_op reads and importNode no longer style the whole document (issue 871)
- `1f5957644` Foafnaut: report maxPieces, maxValueBytes, maxFallbacks, maxTracks and maxSheetBytes as limit hits (issue 865)
- `06859d927` Keep counters and list markers in box order through display contents (#999)
- `eec048b9d` Reuse pinned HTTPS connections through synchronous script startup (#1004)
- `1af5b0d8f` Paint the current text input value after edits (#1000)
- `44e1a39cf` Overlap web font loading with image and icon loading (#892)
- `e586b539d` Reuse approved HTTPS connections during web font loading (#1006)

