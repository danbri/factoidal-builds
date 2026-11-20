### Since the previous full run: -62 subtests (-0.0027 points)

Previous: `20261119T2146Z-wpt-macos-arm64-gh44622133975a1`, core `aae1fda3d`, 92.6207%. This run: core `d0d956ffe`, 92.6180%; 29 commits between.
Tests that lost subtests: 9 (-68); that gained: 3 (+6). Page outcomes: ERROR +2, NO_RESULT +1, OK -5, STALL -3, TIMEOUT +5.

**Directories that fell** (5; the first 5)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| user-timing | 862 | 805 | 769 | -36 |
| webcodecs | 3,935 | 2,579 | 2,557 | -22 |
| webaudio | 5,873 | 714 | 709 | -5 |
| html/syntax | 9,013 | 8,685 | 8,682 | -3 |
| third_party/test262 | 53,838 | 46,250 | 46,249 | -1 |

**Directories that rose** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/webappapis | 3,675 | 3,034 | 3,038 | +4 |
| xhr | 2,344 | 1,832 | 1,833 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 5 directories, the first 5)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| user-timing | 36 | 1 |
| webcodecs | 23 | 2 |
| webaudio/the-audio-api | 5 | 2 |
| html/syntax | 3 | 3 |
| third_party/test262 | 1 | 1 |

**Tests that lost most** (the first 9 of 9)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /user-timing/idlharness.any.worker.html | 36 | 0 | 36 |
| /webcodecs/audio-data.any.worker.html | 22 | 0 | 22 |
| /webaudio/the-audio-api/the-dynamicscompressornode-interface/dynamicscompressor-basic.html | 4 | 0 | 13 |
| /html/syntax/speculative-parsing/generated/page-load/link-rel-stylesheet-disabled.tentative.html | 1 | 0 | 1 |
| /html/syntax/speculative-parsing/generated/page-load/script-src-defer.tentative.html | 1 | 0 | 1 |
| /html/syntax/speculative-parsing/generated/page-load/svg-script-src.tentative.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/AsyncIteratorPrototype/Symbol.asyncIterator/prop-desc.test262.html | 1 | 0 | 1 |
| /webaudio/the-audio-api/the-channelmergernode-interface/ctor-channelmerger.html | 1 | 0 | 5 |
| /webcodecs/encoded-audio-chunk.any.worker.html | 1 | 0 | 2 |

**Commits between** (29)

- `f8f3c6e3d` Add an explicit Run control to the Paralliverse editor
- `7ea1dd760` Make browser acceptance cleanup bounded and run premerge in CI
- `7005bfeed` Merge pull request #639: Paralliverse editor Run control
- `28b36295e` Paralliverse: check ordered task replies against CPU pack and SBM11 scans
- `1d9ff69de` Cover interior SBM11 metadata selections in ordered task collection
- `4956af6cc` Exercise reversed task delivery on a decoded interior PRB1 selection
- `d2a900c5a` Record checked partition examples and exact application imports
- `e4c78ebee` Add typed Paralliverse programs and compositional CPU proof candidates
- `ecafd292a` Exercise typed Paralliverse programs and check all refinement roots
- `a1a5378af` Close CPU refinement goals reported by Lean
- `42bd0be16` Use explicit interpreter equations in the affine proof
- `e49a6ce3d` Make closed word primitives explicit for dependent elaboration
- `de3de4053` Recheck program proofs when transitive Lean dependencies change
- `d2f52e0d6` Give executable word guards concrete boundary types
- `d94517762` Record the exact compiled typed-program theorem evidence
- `752829fef` Start typed GPU selection and bounded Studio proof checks
- `b538ad69c` Check exact word-map shader bytes and invocation semantics
- `893a070c8` Add Lean-owned Studio parsing, plans and framed GPU proof candidates
- `92871a599` Connect the Studio UI and direct GPU buffers to Lean-owned plans
- `6c5e9036e` Compile Studio reports and build real Wasm and GPU demo acceptance
- `d499e3be2` Exercise Studio interaction and require its freshly compiled runtime
- `97c2c10d8` Record proved GPU lowering and scope ancestor assets to unchanged consumers
- `ad76d6043` Bootstrap the verified Wasm runtime and compile developer guide examples
- `4c83287a8` Animate a finite signal sequence through acknowledged GPU readbacks
- `ac601b4e4` Restore shared experiments in place and initialise GPU backends on demand
- `0e4552f1b` Record checked Studio evidence and test explicit WebGPU unavailability
- `62be4ceb6` Keep GPU loss terminal during initialisation and result publication
- `6b9a2b4dc` Include the device-loss regression outside the sparse checkout patterns
- `d0d956ffe` Merge pull request #648 from danbri/wip/paralliverse-studio

