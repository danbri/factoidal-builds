### Since the previous full run: -1,260 subtests (-0.0554 points)

Previous: `20261121T1400Z-wpt-linux-x86_64-gh44911673425a1`, core `adb6b6ebe`, 92.6173%. This run: core `3486f29c6`, 92.5619%; 6 commits between.
Tests that lost subtests: 4 (-1,284); that gained: 3 (+24). Page outcomes: CRASH -1, TIMEOUT +1.

**Directories that fell** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| selection/(root) | 33,918 | 33,664 | 32,388 | -1,276 |
| mixed-content | 2,281 | 1,319 | 1,315 | -4 |
| webcodecs | 3,935 | 2,581 | 2,578 | -3 |
| IndexedDB | 5,853 | 5,504 | 5,503 | -1 |

**Directories that rose** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| shadow-dom | 14,724 | 14,111 | 14,133 | +22 |
| css/cssom-view | 2,722 | 1,282 | 1,283 | +1 |
| html/semantics | 22,429 | 15,574 | 15,575 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 4 directories, the first 4)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| selection | 1,276 | 1 |
| mixed-content/gen | 4 | 1 |
| webcodecs | 3 | 1 |
| IndexedDB | 1 | 1 |

**Tests that lost most** (the first 4 of 4)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /selection/addRange-32.html | 1,276 | 0 | 1,276 |
| /mixed-content/gen/srcdoc-inherit.meta/unset/worker-import.https.html | 6 | 2 | 8 |
| /webcodecs/image-decoder.https.any.html | 14 | 11 | 47 |
| /IndexedDB/interleaved-cursors-large.any.html | 1 | 0 | 1 |

**Commits between** (6)

- `58aca70c6` GSSL: prove checked integer-key BGP matches indexed SPARQL semantics (#689)
- `5fcbdd95d` Respect visibility during pointer hit testing
- `5126fa20f` GSSL: canonical RDF u32 term codec with checked graph/binding round trips (#690)
- `87abb5bdb` GSSL: lossless SBM11 u64 term IDs as two WGSL u32 lanes (#692)
- `f81ca36c0` GSSL: certify request and SBM11 snapshot identity before accepting GPU readback (#693)
- `3486f29c6` GSSL: execute direct64 and dense32 GPU BGP behind snapshot leases (#694)

