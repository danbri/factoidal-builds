### Since the previous full run: +8 subtests (+0.0004 points)

Previous: `20261119T0614Z-wpt-linux-x86_64-gh44470691435a1`, core `182c86e47`, 92.6251%. This run: core `c9b4e0735`, 92.6255%; 47 commits between.
Tests that lost subtests: 1 (-1); that gained: 3 (+9). Page outcomes: CRASH +1, OK +2, STALL -2, TIMEOUT -1.

**Directories that fell** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/semantics | 22,416 | 15,575 | 15,574 | -1 |

**Directories that rose** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 3,926 | 2,573 | 2,580 | +7 |
| IndexedDB | 5,853 | 5,503 | 5,504 | +1 |
| third_party/test262 | 53,838 | 46,249 | 46,250 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 1 directories, the first 1)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| html/semantics | 1 | 1 |

**Tests that lost most** (the first 1 of 1)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /html/semantics/embedded-content/the-img-element/list-of-available-images-does-not-coalesce-in-flight-requests.sub.tentative.html | 1 | 0 | 1 |

**Commits between** (47)

- `3b4dc94db` Add static packing model and focused Lean compiler check
- `b045acbf2` State and prove the staged scatter readback equivalence
- `771bcf5d6` Merge remote-tracking branch 'origin/main' into wip/604-static-pack-spec
- `08568f7c8` Check scan bounds and use one Lean compiler worker
- `7b1d7bebf` Bound Lean worker stack reservations in the focused proof check
- `7ab850bd1` Remove unused simp argument and require all packing theorem reports
- `9a7307ae3` Add checked admission, memory frame and independent CPU reference
- `271a31613` Name the static packing library and CPU runner Paralliverse
- `4333ebca8` Introduce typed Paralliverse stages with explicit completed buffers
- `ad506fb4a` Normalize burst address in Paralliverse scan proof
- `88c9f86e7` Prove staged scatter laws and add bounded Lean Hub CPU entry
- `04b06d0bc` Complete Paralliverse schedule equivalence and exercise the Hub CPU protocol
- `2916fae5a` Discharge scan prefix length inequalities explicitly
- `8eea01fe2` Relate accepted packets and guarded finite-buffer count instructions
- `5652c7def` Collect independent packet and target proof diagnostics in one check
- `9b01b0380` Resolve packet acceptance and finite-dispatch proof obligations
- `7b9811f45` Build the isolated Paralliverse Hub CPU runtime with checked provenance
- `2cdd1538e` Add the gated Paralliverse Hub page and byte-only worker
- `503c1ef28` Add accepted source-bank bounds and explicit bounded loop instructions
- `53d97bc51` Prove finite serial scan effects and introduce indexed scatter instructions
- `911db7f55` Repair finite scan and scatter proof elaboration
- `164103c03` Make finite buffer proof rewrites explicit
- `a1b5eb8c5` Prove a continuation evaluator before compiler replacement
- `6551a4184` Carry the sum refinement through program readback
- `1fd6aa735` Compose accepted packets with the physical scatter lane
- `ba28f72b5` Supply the complete Lean package setup record
- `2e120b566` Prove the loop expression continuation machine
- `88bf00bd3` Keep branch proof checks running through PR conflicts
- `6ef8ea2a9` Prove nested statement scheduling with explicit continuations
- `836688696` Compose arbitrary padded scatter grids with exact finite readback
- `1cddd7f9e` Connect the finite pipeline and independently parsed count shader
- `e25a6a97d` Expose finite packet lets before composing stage executions
- `2f364a38b` Paralliverse: specify and check concrete WGSL scan text
- `76c1ec9ea` Relate scan terminal array size through its initial state
- `70e0f304a` Merge remote-tracking branch 'origin/main' into wip/604-static-pack-spec
- `688bac00a` Refresh generated component directory inventory for Paralliverse
- `c2e9dfb8c` Relate concrete scatter shader text to executed store traces
- `beae37824` Split scatter lexical certificate and repair checked trace derivation
- `ae9c130fa` Check direct Stage equivalence and bound concrete Scatter proof memory
- `6d12a9efe` Connect shader text, store interleavings and Lean source exports
- `db3aa913b` Wire realtime CPU and GPU comparison and repair checked adapters
- `6a1fd7842` Run real WebGPU transport against fresh Lean fixtures
- `ac55b595d` Recognise the checked Stage replacement and prepare browser acceptance
- `1fde31f24` Merge remote-tracking branch 'origin/main' into wip/604-static-pack-spec
- `fc84170a4` Recheck generic store proofs when their source changes
- `a458a3fa4` Accept verified Wasm bytes in the Paralliverse module loader
- `c9b4e0735` Merge pull request #607 from danbri/wip/604-static-pack-spec

