### Since the previous full run: +5 subtests (+0.0002 points)

Previous: `20261122T1022Z-wpt-linux-x86_64-gh45010423815a1`, core `298f7b187`, 92.6182%. This run: core `9a0e966fb`, 92.6184%; 155 commits between.
Tests that lost subtests: 1 (-1); that gained: 1 (+6). Page outcomes: CRASH +1, STALL -1.

**Directories that fell** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| IndexedDB | 5,853 | 5,504 | 5,503 | -1 |

**Directories that rose** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 3,935 | 2,578 | 2,584 | +6 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 1 directories, the first 1)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| IndexedDB | 1 | 1 |

**Tests that lost most** (the first 1 of 1)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /IndexedDB/interleaved-cursors-large.any.html | 1 | 0 | 1 |

**Commits between** (155)

- `e62a2c661` GDSL: add typed Lean-native PVGraph builder over canonical JSON admission
- `9d82f02e0` Add compile-time Lean PVGraph builders and JSONL cross-language fixtures
- `1347bf49c` Cross-check Lean authored PVGraph documents with JS and S-expression frontends
- `5b776bb24` CI: compile Lean-native PVGraph builder and diff exact dataflow across frontends
- `40de081ec` CI: compile Lean-native PVGraph builder and diff exact dataflow across frontends
- `7d321842d` Document Lean as third PVGraph authoring notation with exact admission boundary
- `52582d1f5` Fix native Lean fixture runner qualified PVGraph admission/evaluation references
- `d844d79d4` Correct Lean namespace opening in PVGraph authoring example
- `2f9ef813d` Normalize JS null-prototype outputs before comparing with Lean JSON output
- `de0083151` Align automatic Lean PVGraph output IDs with JS constructor
- `580525dcc` Exercise generated PVGraph node IDs through Lean admission and evaluation
- `8a56deb28` Verify Lean and JS automatic PVGraph IDs against shared fixture
- `49eba6788` Fix Lean reserved prefix keyword in PVGraph ID generator
- `ac9bc4f02` Expose Lean PVGraph builder-state serialization for Wasm API
- `80cd9819f` Add Lean-owned PVGraph build/admit/evaluate operations for the Wasm ABI
- `487c1569f` Route PVGraph build/admit/evaluate through full Lean Wasm dispatcher
- `001159d1f` Reflect PVGraph Wasm operations as full-engine-only in core dispatch
- `4232e671e` Add thin JS PVGraph binding that delegates all construction to Lean Wasm
- `70471a806` Export new PVGraph Lean/Wasm binding without breaking legacy builder
- `51607916c` Type the Lean/Wasm-backed PVGraph host binding
- `53517b1ec` Test JS PVGraph binding delegates construction and evaluation to Wasm
- `5b182ad4c` CI-compile PVGraph Wasm operations and test thin JS binding
- `588f59bea` Clarify GDSL architecture: Lean/Wasm API is authoritative; JS is only a binding
- `4cafed89c` Marshal typed-word inputs across PVGraph Wasm JSON ABI
- `fac84b8ac` Guard actual Lean/Wasm PVGraph evaluation results at compile time
- `8ca098eb0` Fix required options ordering in Wasm PVGraph TypeScript declarations
- `234ff4d5d` Make examples declarative Lean/Wasm builder calls without JS semantics
- `5b930257a` Remove independent JavaScript PVGraph public API
- `170004f73` Remove independent JavaScript PVGraph public API
- `8a5d99ac4` Remove independent JavaScript PVGraph public API
- `2ba08a19f` Run PVGraph Hub admission and CPU exclusively through Lean/Wasm
- `1d3dac909` Make Hub present Lean/Wasm PVGraph only, with no JS fallback
- `7010ead67` Rewrite GDSL spec around public Lean/Wasm API; remove unused implementation history
- `b34be32be` Document only Lean/Wasm PVGraph API in package README
- `36ec37d8c` Delete independent JavaScript PVGraph implementation and tests
- `9b5fe90e5` Delete independent JavaScript PVGraph implementation and tests
- `177a29db6` Delete independent JavaScript PVGraph implementation and tests
- `90aeb31e0` Delete independent JavaScript PVGraph implementation and tests
- `fc0cf7e77` Delete independent JavaScript PVGraph implementation and tests
- `5d4fcddc6` Delete independent JavaScript PVGraph implementation and tests
- `18906e4e6` Delete independent JavaScript PVGraph implementation and tests
- `2025cc4b2` Delete independent JavaScript PVGraph implementation and tests
- `1352515b9` Delete independent JavaScript PVGraph implementation and tests
- `7741bd234` Test Lean/Wasm-only PVGraph Hub and fail if JS implementation returns
- `a3b09a484` Replace JS differential CI with Lean/Wasm PVGraph compilation and authority tests
- `569e0382b` Gate Lean/Wasm-only GDSL Hub and remove obsolete JS runtime files
- `b34799d25` Remove JS PVGraph GPU/device CI; keep Lean authority and low-level GPU tests separate
- `7a457a4ed` Remove obsolete GDSL runtime/history discussion; document Lean PVGraph and device boundary
- `af55e8c88` Correct Hub index to advertise only Lean/Wasm PVGraph semantics
- `6f5802bef` Test current GDSL spec, not a historical GSSL draft
- `398fb83d7` Check current GDSL spec in low-level GPU diagnostic CI
- `fde5c49ab` Remove superseded GSSL draft rather than retaining unused implementation history
- `963d24373` Include Lean PVGraph Wasm source in l4wasm library target
- `8ca8d9475` Use the exported Factoidal browser subpath in PVGraph examples
- `3e3f85311` Use the exported Factoidal browser subpath in PVGraph examples
- `ce2913f77` Require every domain example to construct through Lean/Wasm rather than JS
- `84c685ac0` Fix Lean PVGraph builder syntax error blocking all formal CI
- `0742ec7d2` Factor actual Lean PVGraph evaluator for whole-program GPU refinement theorem
- `0e9736efa` Prove restricted GPU kernel model refines actual Lean PVGraph evaluation
- `f95310317` Gate GPU-model refinement theorems in Lean and audit their axioms
- `9cb6e4dfc` Eta-expand Lean primitive with optional argument for PVGraph refinement
- `bbce318f7` Eta-expand optional constant in GPU evaluator refinement theorem
- `0e281a194` Ratchet entrypoint inventory to Lean/Wasm-only PVGraph API
- `c9385c54f` Discharge dependent GPU model equality proof without unsafe rewrite
- `c0b14156c` Connect PVGraph to existing proof-carrying Factoidal Dataflow Stage contract
- `3f7308367` Centralize GPU opcode selection in Lean and expose decode theorem
- `46010f272` Implement Lean-owned GPU plan and fixed WGSL for admitted parallel PVGraph fragment
- `475cc124c` Require input-port signature without partial head!
- `8f56b68e1` Expand Lean reference buffer bound for GPU benchmarkable workloads
- `4b7de8fd1` Expose Lean GPU lowering through Wasm dispatch
- `7be6bb850` Expose certified-L ean GPU plan operation in full engine
- `9bce4ebff` Reflect GPU plan operation as full-only Lean/Wasm API
- `b99e5e0c8` Register GPU plan Lean module in Wasm build roots
- `8a90b6386` Provide bounded full-output GPU readback separate from diagnostic inspection
- `4bc0682b7` Execute Lean-generated PVGraph GPU plans on resident WebGPU buffers with Lean fallback
- `40ba7e824` Expose Lean-planned PVGraph GPU accelerator with Lean CPU fallback
- `27e33c582` Type the Lean-planned PVGraph GPU acceleration and fallback result
- `61288754c` Classify GPU plan and host executor in original entry-point governance
- `1facf641c` Test public GDSL API includes only Lean-backed GPU host executor
- `ea8bd3648` Compile GPU plan, Dataflow adapter and inspect proof dependencies

