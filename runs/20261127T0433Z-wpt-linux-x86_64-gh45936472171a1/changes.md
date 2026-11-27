### Since the previous full run: +25 subtests (+0.0011 points)

Previous: `20261127T0236Z-wpt-linux-x86_64-gh45929225479a1`, core `2a5550213`, 92.7751%. This run: core `9a8ffacab`, 92.7762%; 43 commits between.
Tests that lost subtests: 4 (-4); that gained: 5 (+29). Page outcomes: unchanged.

**Directories that fell** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| fetch | 13,314 | 8,823 | 8,822 | -1 |
| preload | 956 | 243 | 242 | -1 |
| third_party/test262 | 53,838 | 46,417 | 46,416 | -1 |

**Directories that rose** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| selection/contenteditable | 252 | 128 | 146 | +18 |
| webaudio | 5,873 | 3,387 | 3,393 | +6 |
| css/css-sizing | 6,744 | 5,221 | 5,225 | +4 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 3 directories, the first 3)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| third_party/test262 | 2 | 2 |
| fetch/metadata | 1 | 1 |
| preload | 1 | 1 |

**Tests that lost most** (the first 4 of 4)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /fetch/metadata/generated/element-img.https.sub.html | 18 | 17 | 45 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |
| /third_party/test262/test/annexB/built-ins/String/prototype/fixed/length.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/assignment/white-space.test262.html | 1 | 0 | 1 |

**Commits between** (43)

- `81f34fbdf` SPARQL differential campaign, Factoidal against Oxigraph (issue 1184, P7)
- `6092c4580` differential-sparql.yml: quote a description that held a colon (the file did not parse)
- `ae4f4b6bf` SPARQL differential: accept any ORDER BY order that SPARQL 1.1 section 15.1 allows; fresh BIND variables; 5,000 cases
- `42b1acb09` Skills: differential campaign rule with its cost (test-suites); hazards 47 and 48 (a check line that does not stop a commit; a declaration r
- `2fb8bcb11` npm tests: start child processes the way the running runtime does (issue 1176)
- `8d6211422` SPARQL differential: keep a sample of the queries both engines refuse, with their errors
- `8ae21dffe` SPARQL differential: bracket every FILTER expression (FILTER !BOUND(?x) is not SPARQL; 140 of 5,000 generated queries were refused by both e
- `d9386c743` Claims register: reader-result-is-a-set (RDF.Source.parseDocument_set) for the six reader stages; 60 of 156 entry points now map to a stage 
- `eafe71438` Formal-verification review: section 6, state after the first night
- `9c3f84c72` CLAUDE.md, JIT record, plan, foafnaut skill: owner's rule of 2026-11-27, no V8 and no engine of another browser runs page code; stage E and 
- `e87a98783` XMPP PROXY+TLS test: one-write client that works on both runtimes; record runtime differences (issue 1176)
- `9ff7f976b` BubblePopJS: global names read through cached scope chains, no walk of the environments by name (issue 471, step 1)
- `4cc0e34b4` Decode SVG paint reference fragments before lookup
- `a11fa52a5` Cover percent-encoded stroke paint
- `384d1972a` Validate paint URL syntax before decoding fragment
- `d92e54953` Cover invalid paint URL tokens and encoded spaces
- `002544c1c` Accept CSS geometry dimensions on SVG rect
- `1c48eb7a8` Cover SVG rect CSS dimensions and percentages
- `5e5fecb4f` Validate only CSS rules matching the current SVG element
- `9e50d05ae` Cover unmatched CSS declarations in the cascade
- `9ab0adc49` Cover root and nested SVG rect geometry rules
- `eb8da8e91` Clarify SVG geometry property applicability
- `717e65aed` Cover CSS rectangle viewBox and zero-size geometry
- `107fa06e2` Test unmatched SVG CSS values without rejecting unrelated elements
- `9855201b9` Preserve SVG dimensions for max-content sizing
- `63237f5f1` Guard SVG max-content intrinsic dimensions
- `2adea3fd9` SVG paint fragment IDs: UTF-8 decode without BOM from L4Factoidal.WHATWG.Encoding, not a second decoder (review of PR 1153; issue 1191)
- `a4947f8ce` svg-tiny-pixels: per-file report of the run at b69bcd66d (Linux, lavapipe), before the border rule and the fonts
- `6a7265178` Hazard 49: tools/dataflow-inventory.py runs lake build; read a tool's docstring before running it on the laptop
- `cd6bc8398` Tor record section 21: browser wiring plan, decisions in Lean, Textnaut as testbed (owner, 2026-11-27)
- `939c92809` Design record: Lean big-integer timing in signing, and its relation to the AES rule
- `9b046432e` Bignum timing record: HACL* bignum scope, and four layers for checking constant time from Lean
- `9690023d2` Canvas raster and Web Audio: no float conversion through text in their loops (Particle Rex profile, issue 471)
- `b36fcd0a1` BubblePopJS: % on fractional operands rounds m/2^k directly (issue 471)
- `e56d8bdc1` csimp reach allow list: dyadicFast calls dyadic as its slow path (issue 471)
- `8f8985fa8` Render scores: svg-tiny-acceptance 304 accepted of 496 (animation drawn at 0 ms)
- `787b48a66` SVG animation: path values in absolute form, motion along path segments, invalid min/max ignored
- `95c90977a` Render scores: svg-tiny-pixels at a4947f8ce, frame border left out, no SFNT fonts
- `d38460c91` svg-tiny-pixels: give the engine the vendored OFL fonts for text that the SVG font does not draw (owner, 2026-11-27)
- `91ab713a7` PageFetch: Tor mode for page requests, decided in Lean (issue 1060)
- `810da94dd` Tor record 21a: four conditions before Tor mode is offered (no direct connection; owner, 2026-11-27)
- `5c53dedd9` secp256k1 over HACL* (RFC 6979, low-S, recovery id) with an opaque secret-key type and a Valgrind constant-time check
- `9a8ffacab` SVG raster: the fill of a dashed path uses the path's edge spans

