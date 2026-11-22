### Since the previous full run: -2,103 subtests (-0.0925 points)

Previous: `20261121T2014Z-wpt-macos-arm64-gh44945175892a1`, core `9dcfb0515`, 92.6208%. This run: core `9a0e966fb`, 92.5283%; 164 commits between.
Tests that lost subtests: 8 (-2,105); that gained: 2 (+2). Page outcomes: ERROR +3, NO_RESULT +3, OK -6, STALL +1, TIMEOUT -1.

**Directories that fell** (5; the first 5)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webgl | 4,284 | 4,259 | 2,164 | -2,095 |
| web-animations | 4,256 | 3,952 | 3,948 | -4 |
| webcodecs | 3,935 | 2,582 | 2,580 | -2 |
| preload | 956 | 243 | 242 | -1 |
| websockets | 2,389 | 1,259 | 1,258 | -1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 7 directories, the first 7)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| webgl | 2,095 | 1 |
| web-animations/animation-model | 4 | 1 |
| webcodecs | 2 | 2 |
| preload | 1 | 1 |
| third_party/test262 | 1 | 1 |
| websockets/security | 1 | 1 |
| websockets/stream | 1 | 1 |

**Tests that lost most** (the first 8 of 8)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /webgl/idlharness.any.worker.html | 2,095 | 0 | 2,099 |
| /web-animations/animation-model/combining-effects/clamping-001.tentative.html | 4 | 0 | 12 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |
| /third_party/test262/test/language/statements/for-await-of/iterator-close-non-throw-get-method-non-callable.test262.html | 1 | 0 | 1 |
| /webcodecs/image-decoder-image-orientation-none.https.html | 2 | 1 | 16 |
| /webcodecs/image-decoder.https.any.html | 15 | 14 | 47 |
| /websockets/security/002.html?wss | 1 | 0 | 1 |
| /websockets/stream/tentative/close.any.worker.html?wpt_flags=h2 | 1 | 0 | 27 |

**Commits between** (164)

- `fda3bf0a5` GDSL 0.2: one typed dataflow graph, JS and S-expression syntax across every domain (#705)
- `7f3bcf9ab` PVGraph: require native Lean admission for GPU dataflow execution and verify real JSON semantics (#708)
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
- `bc936a32c` Add a local EPUB 3 reading view and pure Lean API (#714)
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
- `d929fac2a` Build and link the EPUB reader in Foafnaut (#718)
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
- `7192fb7c3` Record GDSL PVGraph release entry points (#710)
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
- `57872a9b3` Keep the Foafnaut import audit on the shared root list (#719)
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

