### Since the previous full run: +95 subtests (+0.0042 points)

Previous: `20261124T1847Z-wpt-macos-arm64-gh45462830318a1`, core `0ac58b427`, 92.6291%. This run: core `d7e315b58`, 92.6333%; 68 commits between.
Tests that lost subtests: 3 (-3); that gained: 48 (+98). Page outcomes: ERROR -2, OK +2, STALL -2, TIMEOUT +2.

**Directories that rose** (19; the first 19)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| svg/path | 540 | 62 | 90 | +28 |
| third_party/test262 | 53,838 | 46,258 | 46,277 | +19 |
| webaudio | 5,873 | 701 | 714 | +13 |
| css/css-writing-modes | 421 | 223 | 229 | +6 |
| css/css-flexbox | 4,933 | 3,893 | 3,897 | +4 |
| workers | 1,598 | 712 | 716 | +4 |
| html/rendering | 11,722 | 10,118 | 10,121 | +3 |
| css/css-shadow | 377 | 241 | 243 | +2 |
| css/css-values | 10,473 | 6,255 | 6,257 | +2 |
| editing/other | 16,742 | 13,797 | 13,799 | +2 |
| infrastructure | 290 | 111 | 113 | +2 |
| svg/text | 347 | 66 | 68 | +2 |
| webrtc-stats | 338 | 0 | 2 | +2 |
| css/selectors | 6,266 | 5,719 | 5,720 | +1 |
| html/dom | 72,463 | 69,928 | 69,929 | +1 |
| html/semantics | 22,498 | 15,587 | 15,588 | +1 |
| preload | 956 | 242 | 243 | +1 |
| svg/shapes | 18 | 1 | 2 | +1 |
| svg/styling | 421 | 180 | 181 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| html/semantics | 2 | 2 |
| html/rendering | 1 | 1 |

**Tests that lost most** (the first 3 of 3)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /html/rendering/widgets/button-layout/display-other.html | 2 | 1 | 18 |
| /html/semantics/embedded-content/the-img-element/list-of-available-images-does-not-coalesce-in-flight-requests.sub.tentative.html | 1 | 0 | 1 |
| /html/semantics/popovers/popover-attribute-all-elements.html | 1,083 | 1,082 | 1,101 |

**Commits between** (68)

- `663a60a73` Pass embedded SVG paint through the document author cascade
- `63f74e538` Add the bounded WebP container and VP8L prefix readers (#914)
- `074a3e51f` Preserve inline SVG carrying category and icon metadata (#907)
- `a1cabc364` Decode bounded lossy WebP key-frame controls and partitions (#921)
- `1763d4a0b` Decode bounded VP8L entropy planes (#922)
- `dd7ba4fe5` Decode lossless WebP through the shared browser image path
- `c8ba916ea` Add a Hub page of rule-based explanations for the MLP Wikidata queries
- `ba81433bc` Merge pull request #926 from danbri/claude/wikidata-query-explanations
- `7757db5a4` Decode VP8 keyframe entropy updates and intra prediction records
- `90a4d8b5a` Build the lossless WebP dependency in all Foafnaut engines
- `9549f2873` Present Wikidata result views as a QLever gallery (#929)
- `fbab3a554` Decode and fold VP8 keyframe residual coefficient blocks
- `c09ad8b4f` Read VP8 arithmetic input only when the next decision needs it
- `7517927eb` Serve credited Commons thumbnails in the Wikidata gallery (#930)
- `c89d60d58` Invalidate SVG scenes when author paint declarations change
- `e50365525` Reconstruct signed VP8 residual samples with integer inverse transforms
- `5052a26af` Version the Wikidata gallery assets together (#933)
- `0c75227a1` Reconstruct unfiltered VP8 luma and chroma planes
- `d7784637b` Prove WHT zero preservation through the vector map
- `71a7067fc` Load Wikidata previews on scroll and check parser capabilities (#935)
- `5ad0d209b` Deblock reconstructed VP8 luma and chroma planes
- `e80da8fa1` Convert filtered VP8 planes to straight RGBA
- `8992c2eb3` Decode and paint both static WebP formats in Foafnaut
- `d63fc25a9` Resolve SVG descendants without replacing outer viewport dimensions
- `51701d034` Page host: an attribute write is seen as one that changes the rules only when the written element is a style or link element; before, the wh
- `70ce18105` Page host: a child write is seen as one that changes the rules only when the added or removed nodes hold a style or link element, or the par
- `bbac00eea` testharness-run: load the sheets that the page's sheets import (page-load.mjs loadImports) and give them as imported to fontFaces and to the
- `317dd59ac` Use constant stack for Wikidata rewrite scans
- `5f518d128` Link WebP decoders into standalone SVG Wasm
- `c8fc9549d` Merge current main into the Wikidata stack audit repair
- `5f110dd3a` Match conditional host selectors in shadow stylesheets
- `2728ac6fe` Merge current main into the GOV.UK SVG cascade repair
- `270c8d56b` Keep styled slot nodes in the flat layout tree
- `0be94b4bf` Paint inline-block transforms without growing line measurements
- `6a4306170` Verify browser WebP with the Linux release audit repair
- `3d77f3c97` Fix Math rounding and signed zeros, and add missing constants
- `6dd48af7e` Check the retained slot in the flat tree fixture
- `4e82ebcc1` Align Lean record fields in the inline layout repair
- `89d53d30c` Merge pull request #941 from danbri/wip/wikidata-tail-audit
- `94a0e0b3d` Render details disclosure glyphs as list markers
- `cbe56c453` Draw the default address bar in the held Liberation Mono face
- `62976cab1` Include the added defaults in the user-agent rule count guard
- `fb63b548f` Include the added defaults in the user-agent rule count guard
- `7af027dbe` Merge pull request #919 from danbri/wip/embedded-svg-author-cascade
- `0b9497bd2` Integrate static WebP with the embedded SVG cascade
- `f8cf8cb5a` Compile the initial desktop page at presentation time
- `60f82460d` Integrate BubblePop Math fixes with the repair to the release audit
- `0a03d1437` Fix disclosure display elaboration on current main
- `41022c1f7` Merge pull request #943 from danbri/wip/css-inline-block-transform
- `b815d75e8` Integrate Liberation Mono address chrome with current main
- `ed5b99109` Lay out block descendants through nested inline-blocks
- `d5d23ce67` Merge pull request #949 from danbri/wip/desktop-first-compile
- `3e016df8a` Preserve small inputs in BubblePop expm1 and log1p
- `f64af0c06` Limit default slot display to HTML elements
- `bc9f236d7` Integrate disclosure list markers with the desktop layout fixes
- `6ad62abbf` Activate focused disclosure summaries with Space
- `e0653fe70` Merge pull request #948 from danbri/wip/liberation-mono-address-bar
- `918935f9b` Merge pull request #940 from danbri/wip/static-webp-browser
- `408f7760d` Merge pull request #944 from danbri/wip/bubblepop-math-rounding
- `05ec0b29c` Merge pull request #951 from danbri/wip/nested-inline-block-layout
- `69b724d79` Integrate disclosure markers with nested inline-block layout
- `9b554985b` Merge pull request #942 from danbri/wip/css-conditional-shadow-host
- `867f5658f` Read captured negative registry output without SIGPIPE
- `2b21677b2` Integrate disclosure markers with the HTML slot display fix
- `37f89212e` Merge pull request #959 from danbri/wip/dataflow-test-broken-pipe
- `2436a37f8` Merge pull request #956 from danbri/wip/details-keyboard-activation
- `d63d0983f` Merge pull request #953 from danbri/wip/bubblepop-small-math
- `d7e315b58` Merge pull request #945 from danbri/wip/css-disclosure-markers

