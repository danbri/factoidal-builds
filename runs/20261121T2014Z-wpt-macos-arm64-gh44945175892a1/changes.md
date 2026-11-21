### Since the previous full run: +64 subtests (+0.0028 points)

Previous: `20261120T2130Z-wpt-macos-arm64-gh44820925828a1`, core `d0d956ffe`, 92.6180%. This run: core `9dcfb0515`, 92.6208%; 19 commits between.
Tests that lost subtests: 4 (-7); that gained: 11 (+71). Page outcomes: ERROR -1, NO_RESULT -1, OK +4, STALL +1, TIMEOUT -3.

**Directories that fell** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/webappapis | 3,675 | 3,038 | 3,034 | -4 |
| websockets | 2,389 | 1,260 | 1,259 | -1 |
| xhr | 2,344 | 1,833 | 1,832 | -1 |

**Directories that rose** (5; the first 5)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| user-timing | 862 | 769 | 805 | +36 |
| webcodecs | 3,935 | 2,557 | 2,582 | +25 |
| webaudio | 5,873 | 709 | 714 | +5 |
| html/syntax | 9,013 | 8,682 | 8,685 | +3 |
| css/cssom-view | 2,722 | 1,282 | 1,283 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 4 directories, the first 4)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| html/webappapis | 4 | 1 |
| third_party/test262 | 1 | 1 |
| websockets | 1 | 1 |
| xhr | 1 | 1 |

**Tests that lost most** (the first 4 of 4)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /html/webappapis/dynamic-markup-insertion/opening-the-input-stream/abort-refresh-immediate.window.html | 4 | 0 | 6 |
| /third_party/test262/test/language/statements/for-await-of/async-gen-dstr-var-obj-ptrn-id-init-fn-name-fn.test262.html | 1 | 0 | 1 |
| /websockets/Create-nonAscii-protocol-string.any.worker.html?wpt_flags=h2 | 1 | 0 | 1 |
| /xhr/xhr-timeout-longtask.any.worker.html | 1 | 0 | 1 |

**Commits between** (19)

- `d2f20faf8` Paralliverse: navigate actual CPU vs GPU steps and track four application worlds (#667)
- `dd56f0e7e` Paralliverse BGP Studio: lexical RDF, larger Lean/Wasm queries and separate GPU ID packing (#671)
- `11a88e7cd` Paralleliverse Studio: real CPU/GPU BGP joins and gentle public rename
- `a5bd5f296` Add EVM bytecode to WebAssembly SPARQL demo (#677)
- `3a1a30101` Publish interactive Ethereum EVM-to-WASM SPARQL demos in Hub (#682)
- `520f15475` Introduce GSSL composition foundation (#684)
- `581b4998a` Specify and prove SPARQL GSSL fast-path boundary (#686)
- `68fce2258` GSSL: scoped equality-coded joins and SPARQL proof-carrying candidate boundary (#687)
- `b9b6d96cc` Paralliverse: proof-backed integer BGP backend and actual device differential harness (#675)
- `adb6b6ebe` GSSL: guard finite RDF codebooks with engine-term equality (#688)
- `58aca70c6` GSSL: prove checked integer-key BGP matches indexed SPARQL semantics (#689)
- `5fcbdd95d` Respect visibility during pointer hit testing
- `5126fa20f` GSSL: canonical RDF u32 term codec with checked graph/binding round trips (#690)
- `87abb5bdb` GSSL: lossless SBM11 u64 term IDs as two WGSL u32 lanes (#692)
- `f81ca36c0` GSSL: certify request and SBM11 snapshot identity before accepting GPU readback (#693)
- `3486f29c6` GSSL: execute direct64 and dense32 GPU BGP behind snapshot leases (#694)
- `76502cc52` GSSL: test GPU BGP using genuine Lean-generated SBM11 term IDs (#695)
- `342effcbd` GSSL: general-purpose GPU-resident compute sessions, inspection and worklet boundary (#697)
- `9dcfb0515` GSSL 0.1 spec and public exploratory GPU-resident Hub workbench (#703)

