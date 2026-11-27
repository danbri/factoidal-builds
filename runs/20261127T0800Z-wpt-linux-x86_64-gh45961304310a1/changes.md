### Since the previous full run: +560 subtests (+0.0246 points)

Previous: `20261127T0712Z-wpt-linux-x86_64-gh45955481145a1`, core `0a4c26613`, 92.7975%. This run: core `e3468d30a`, 92.8221%; 27 commits between.
Tests that lost subtests: 4 (-95); that gained: 2 (+655). Page outcomes: CRASH -1, OK -2, STALL +2, TIMEOUT +1.

**Directories that fell** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| sanitizer-api | 3,839 | 2,639 | 2,576 | -63 |
| streams | 5,796 | 5,580 | 5,550 | -30 |
| html/canvas | 6,311 | 3,731 | 3,730 | -1 |

**Directories that rose** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| shadow-dom | 14,726 | 13,500 | 14,154 | +654 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 4 directories, the first 4)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| sanitizer-api | 63 | 1 |
| streams/piping | 30 | 1 |
| html/canvas | 1 | 1 |
| third_party/test262 | 1 | 1 |

**Tests that lost most** (the first 4 of 4)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /sanitizer-api/sanitizer-processing-instructions.html | 63 | 0 | 63 |
| /streams/piping/close-propagation-forward.any.html | 30 | 0 | 30 |
| /html/canvas/offscreen/manual/filter/offscreencanvas.filter.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/Temporal/ZonedDateTime/compare/argument-propertybag-timezone-wrong-type.test262.html | 1 | 0 | 1 |

**Commits between** (27)

- `350f850d2` Beacon chain (Fulu): presets, SSZ codecs for all 59 ssz_static containers, Snappy reader, spec-test runner
- `2fe1c94a5` Beacon chain (Fulu): epoch processing, block processing, process_slots and state_transition, 33 theorems, runner for operations, epoch_proce
- `4f17a857f` Beacon chain: incremental roots for the large state vectors, pivot fast path proved equal, epoch scaling benchmark, CI workflow with ratchet
- `9898f6caa` Beacon chain: own Lake package formal/lean4/ethereum-beacon (the consensus package's lakefile and audits stay as they were); registry-sized 
- `5d783932f` Design record: independent beacon state transition (Fulu)
- `33600e6e4` Worknotes index: beacon record in date order
- `ea503d6ea` Beacon workflow: lakefile assertion checks for require blocks and link arguments
- `94dbd194d` EVM: BALANCE, EXTCODESIZE/COPY/HASH, BLOCKHASH, TLOAD/TSTORE and MCOPY in the world-aware dispatcher
- `12458e964` EVM evidence: re-pin the London claim root blob and witness closure count for the account-opcode module
- `e619b1431` Beacon runner: rewards, finality and random vector suites; delta-form rewards functions checked against the fused update; transition time me
- `8c0317042` EVM: CREATE and CREATE2 in the world-aware dispatcher (Shanghai to Osaka)
- `06c48e4f1` EVM CREATE/CREATE2: dispatcher theorems, guards and axiom inventory
- `91f384483` EVM CREATE/CREATE2: CI differential step, README, evidence pins
- `e306fbda9` EVM tests: use undefined opcode 0x0c, not the now-executable BLOCKHASH, as the unsupported-frame control in blob-call and transaction-list
- `479bdcb4a` EVM: SELFDESTRUCT (0xff) with EIP-6780 semantics in the world-aware dispatcher, and transaction-end deletion
- `3b4e0e3ec` EVM: contract-creation transactions through the shared CREATE path (Lean core)
- `2cc6f8aab` EVM creation transactions: JSON to null, created address in results, differential against EthereumJS runTx
- `c5cf9f3fa` EVM creation transactions: theorems, guards, axiom inventory, CI step, README, pins
- `1746b005e` EVM witness tests: mirror the 0x0c unsupported-frame control and re-pin the fixture preparation source
- `2ca91dd77` Beacon ratchet baseline from CI run 45930370360 (minimal 7954/7954, mainnet 929/929, real signature checks); measured numbers in the design 
- `2ae4cab3b` EVM list tests: keep the retained BLOCKHASH account bytes for the 30 bound requests; only the unsupported-frame list uses undefined opcode 0
- `1324c7706` EVM: one definition of the fork's active precompiles for the EIP-2929 initial access set
- `16fdd6ba4` Merge main 8787a5b7cd02
- `119bbf2bc` Merge main (precompiles PR #1193) into the instruction-set branch; re-pin evidence (189 sources, 51-module witness closure)
- `616014cfb` Merge main 98eb72ae0d1f
- `e6fed8c3f` Merge pull request #1197 from danbri/wip/eth-opcodes-20261127
- `e3468d30a` Merge pull request #1196 from danbri/wip/eth-beacon-20261127

