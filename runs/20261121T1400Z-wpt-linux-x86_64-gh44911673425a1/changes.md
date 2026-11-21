### Since the previous full run: +1,252 subtests (+0.0551 points)

Previous: `20261121T0844Z-wpt-linux-x86_64-gh44886264032a1`, core `d0d956ffe`, 92.5623%. This run: core `adb6b6ebe`, 92.6173%; 10 commits between.
Tests that lost subtests: 3 (-24); that gained: 1 (+1,276). Page outcomes: OK -2, STALL +2.

**Directories that fell** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| shadow-dom | 14,724 | 14,133 | 14,111 | -22 |
| html/semantics | 22,429 | 15,575 | 15,574 | -1 |
| webcodecs | 3,935 | 2,582 | 2,581 | -1 |

**Directories that rose** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| selection/(root) | 33,918 | 32,388 | 33,664 | +1,276 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 3 directories, the first 3)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| shadow-dom/declarative | 22 | 1 |
| html/semantics | 1 | 1 |
| webcodecs | 1 | 1 |

**Tests that lost most** (the first 3 of 3)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /shadow-dom/declarative/declarative-shadow-dom-basic.html | 22 | 0 | 22 |
| /html/semantics/embedded-content/the-img-element/list-of-available-images-does-not-coalesce-in-flight-requests.sub.tentative.html | 1 | 0 | 1 |
| /webcodecs/image-decoder.https.any.html | 15 | 14 | 47 |

**Commits between** (10)

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

