### Since the previous full run: +66 subtests (+0.0029 points)

Previous: `20261124T1905Z-wpt-linux-x86_64-gh45466341341a1`, core `bbac00eea`, 92.6283%. This run: core `9b554985b`, 92.6312%; 42 commits between.
Tests that lost subtests: 2 (-2); that gained: 39 (+68). Page outcomes: unchanged.

**Directories that fell** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 4,168 | 2,638 | 2,637 | -1 |

**Directories that rose** (14; the first 14)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| svg/path | 540 | 62 | 90 | +28 |
| third_party/test262 | 53,838 | 46,258 | 46,275 | +17 |
| css/css-writing-modes | 421 | 223 | 229 | +6 |
| css/css-shadow | 377 | 241 | 243 | +2 |
| css/css-values | 10,473 | 6,255 | 6,257 | +2 |
| html/rendering | 11,722 | 10,118 | 10,120 | +2 |
| html/semantics | 22,498 | 15,586 | 15,588 | +2 |
| svg/text | 347 | 66 | 68 | +2 |
| css/selectors | 6,266 | 5,719 | 5,720 | +1 |
| fetch | 13,290 | 8,806 | 8,807 | +1 |
| html/dom | 72,463 | 69,901 | 69,902 | +1 |
| preload | 956 | 242 | 243 | +1 |
| svg/shapes | 18 | 1 | 2 | +1 |
| svg/styling | 421 | 180 | 181 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| html/semantics | 1 | 1 |
| webcodecs | 1 | 1 |

**Tests that lost most** (the first 2 of 2)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /html/semantics/embedded-content/the-video-element/intrinsic_sizes.htm | 3 | 2 | 5 |
| /webcodecs/image-decoder.https.any.html | 10 | 9 | 47 |

**Commits between** (42)

- `663a60a73` Pass embedded SVG paint through the document author cascade
- `dd7ba4fe5` Decode lossless WebP through the shared browser image path
- `7757db5a4` Decode VP8 keyframe entropy updates and intra prediction records
- `90a4d8b5a` Build the lossless WebP dependency in all Foafnaut engines
- `fbab3a554` Decode and fold VP8 keyframe residual coefficient blocks
- `c09ad8b4f` Read VP8 arithmetic input only when the next decision needs it
- `c89d60d58` Invalidate SVG scenes when author paint declarations change
- `e50365525` Reconstruct signed VP8 residual samples with integer inverse transforms
- `0c75227a1` Reconstruct unfiltered VP8 luma and chroma planes
- `d7784637b` Prove WHT zero preservation through the vector map
- `5ad0d209b` Deblock reconstructed VP8 luma and chroma planes
- `e80da8fa1` Convert filtered VP8 planes to straight RGBA
- `8992c2eb3` Decode and paint both static WebP formats in Foafnaut
- `d63fc25a9` Resolve SVG descendants without replacing outer viewport dimensions
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
- `cbe56c453` Draw the default address bar in the held Liberation Mono face
- `fb63b548f` Include the added defaults in the user-agent rule count guard
- `7af027dbe` Merge pull request #919 from danbri/wip/embedded-svg-author-cascade
- `0b9497bd2` Integrate static WebP with the embedded SVG cascade
- `f8cf8cb5a` Compile the initial desktop page at presentation time
- `60f82460d` Integrate BubblePop Math fixes with the repair to the release audit
- `41022c1f7` Merge pull request #943 from danbri/wip/css-inline-block-transform
- `b815d75e8` Integrate Liberation Mono address chrome with current main
- `ed5b99109` Lay out block descendants through nested inline-blocks
- `d5d23ce67` Merge pull request #949 from danbri/wip/desktop-first-compile
- `f64af0c06` Limit default slot display to HTML elements
- `e0653fe70` Merge pull request #948 from danbri/wip/liberation-mono-address-bar
- `918935f9b` Merge pull request #940 from danbri/wip/static-webp-browser
- `408f7760d` Merge pull request #944 from danbri/wip/bubblepop-math-rounding
- `05ec0b29c` Merge pull request #951 from danbri/wip/nested-inline-block-layout
- `9b554985b` Merge pull request #942 from danbri/wip/css-conditional-shadow-host

