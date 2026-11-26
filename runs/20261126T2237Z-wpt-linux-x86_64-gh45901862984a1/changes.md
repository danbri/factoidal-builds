### Since the previous full run: +30 subtests (+0.0013 points)

Previous: `20261126T2150Z-wpt-linux-x86_64-gh45897356294a1`, core `87d5c360a`, 92.6571%. This run: core `c7a52eea3`, 92.6584%; 250 commits between.
Tests that lost subtests: 2 (-2); that gained: 3 (+32). Page outcomes: CRASH +1, TIMEOUT -1.

**Directories that fell** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| secure-contexts | 86 | 14 | 13 | -1 |

**Directories that rose** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| streams | 5,796 | 5,550 | 5,580 | +30 |
| html/semantics | 22,535 | 15,744 | 15,745 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| secure-contexts | 1 | 1 |
| third_party/test262 | 1 | 1 |

**Tests that lost most** (the first 2 of 2)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /secure-contexts/basic-shared-worker.html | 1 | 0 | 5 |
| /third_party/test262/test/built-ins/Temporal/Instant/prototype/since/argument-string-calendar-annotation-invalid-key.test262.html | 1 | 0 | 1 |

**Commits between** (250)

- `fa295e750` proof(evm): establish parent-world rollback for executable CALL opcode runner
- `090fac2fa` assurance(evm): pin new executable CALL opcode rollback theorem source
- `8a1637e34` assurance(evm): pin four real CALL parent rollback theorems and independent opcode evidence
- `fb6aa54fc` ci(evm): require 24 actual Lean theorem axiom lists, including public CALL run rollback
- `bdd06cb33` feat(evm): fork-exact Frontier value transfer with conservation, nonce and gas proofs
- `331fc9432` build(evm): import Frontier mainnet transfer semantics into EVMCleanroom.lean
- `ed6738a6b` build(evm): import Frontier mainnet transfer semantics into CLI.lean
- `d669e079c` feat(evm): add checked Frontier mainnet value-transfer CLI with 256-bit decimal results
- `580084698` evidence(evm): pin first actual Ethereum mainnet signed tx, block and pre-Byzantium receipt commitments
- `7147bc56d` test(mainnet): authenticate block 46147 signed transaction, transaction/receipt tries and conditional Lean Frontier transition
- `12f0bce06` ci(mainnet): require real Frontier block/receipt commitments and checked Lean transfer with fail-closed source caveats
- `6acdfa0b6` assurance(mainnet): pin historical Frontier raw signed transaction, roots and explicitly conditional Lean replay boundaries
- `9b29574f8` fix(evm): use ordinary Lean comment before Frontier #guard checks
- `4dcaf4a01` assurance(evm): repin Frontier proof file after Lean comment syntax repair
- `bf389f90e` feat(mainnet): verify historical EIP-1186 account proofs and recompute intermediate+final roots via Lean and sparse MPT
- `4389effc3` feat(mainnet): acquire archive EIP-1186 proofs and independently require exact intermediate+final Frontier state roots
- `1495a9a07` ci(mainnet): validate sparse account MPT proofs and probe public historical archive without relaxing evidence gate
- `f0b5aa47a` assurance(mainnet): pin EIP-1186 verifier/fetcher and explicit two-stage authenticated state-root replay exit
- `6a1399d2a` assurance(mainnet): register six live Frontier arithmetic theorems and their printed axiom sets
- `2b44551a7` ci(mainnet): enforce 30 source-pinned actual Lean theorem axiom lists including Frontier
- `222cbf900` ci(mainnet): probe publicly observed historical EIP-1186 archive services with no claim on failures
- `5d2ec7110` test(mainnet): verify sparse account proofs for both existing and absent 2015 recipients
- `31bbdb5b6` ci(mainnet): require both EIP-1186 account-existence cases and ten proof/root mutations
- `46969b793` assurance(mainnet): pin nonexistence Merkle-proof test revision and 10 falsification gates
- `0615a88f8` feat(evm): model stipend, new-account surcharge and journalled nonzero CALL value transfer in Lean
- `80bd3a0d0` feat(evm): dispatch nonzero-value CALL via proved stipend and world payment journal
- `0de5d3db1` feat(evm): expose actual CALL prestate balances and post-call account observations in Lean CLI
- `7ff6bbe63` test(evm): compare real nonzero CALL transfer and gas stipend against EthereumJS on hundreds of programs
- `798c650d5` build(evm): include nonzero value CALL stipend proofs in Lean root library
- `0bf3d478f` fix(mainnet): distinguish EIP-1186 nonexistent account zero-hash fields from existing empty Ethereum account hashes
- `955880608` ci(evm): require 450 actual nonzero CALL value and stipend oracle cases plus rollback
- `a7073f1fa` assurance(mainnet): pin proof-verified nonmembership RPC hash semantics and preserve root mismatch as fatal
- `d6805bb37` assurance(evm): pin nonzero CALL implementation and oracle with pending-evidence status
- `276adb414` fix(evm): expose let-bound call budget branches to Lean proof splits and parenthesize Bool hypothesis
- `77faca951` assurance(evm): repin corrected Lean value-call budget proof source
- `3e25f7e9d` test(mainnet): make synthetic absent-account EIP-1186 fields match real RPC zero-hash convention
- `14bbedc93` assurance(mainnet): pin corrected synthetic EIP-1186 absent account witness generation
- `7cf5b08d4` ci(evm): cancel obsolete same-branch EVM runs to prioritize newest proof and historical replay gate
- `d161d6000` fix(evm): remove unattached Lean doc comment and handle CALL stack underflow exhaustively
- `0b43936cb` assurance(evm): pin corrected exhaustive CALL opcode dispatcher
- `08790785c` assurance(evm): pin seven actual Lean value-CALL theorem axiom lists (31 total)
- `24613b699` ci(evm): require 31 live theorem axiom fingerprints including stipend/value CALL proofs
- `e3245eddb` assurance(mainnet): independent pure-Python Keccak/RLP/secure-MPT replay of authenticated Frontier transaction and reward
- `fe2c9daf5` evidence(mainnet): pin full 2015 archive EIP-1186 account proofs and parent header for offline Frontier replay
- `986eb3d05` feat(evm): execute ADDRESS, CALLVALUE and SELFBALANCE from explicit Lean frame context
- `f2d5e2d12` proof(evm): bind CALL context address and balance to actual transaction world projection
- `746bb84f2` test(mainnet): six adversarial mutation controls for standalone 2015 Keccak/RLP/MPT state replay
- `12065d090` feat(evm): execute CALLVALUE with actual transferred child value and post-transfer SELFBALANCE
- `a5ced26a5` feat(evm): refresh parent SELFBALANCE after actual CALL account transfer or rollback
- `9896418d0` ci(mainnet): mandatory offline authenticated Frontier prestate replay in Lean+EthereumJS and independent Python, with roots pinned
- `bcad6ed3c` test(evm): guard executable ADDRESS CALLVALUE SELFBALANCE and world frame-context projection
- `5ef6bb8d0` assurance(mainnet): pin real archive 2015 account proofs, independent Keccak/RLP/MPT oracle and mandatory two-root verification
- `2d47bfb1d` test(evm): independently compare 128 executed child CALLVALUE/SELFBALANCE/ADDRESS and parent balances
- `6713c7e6a` build(evm): include verified executable CALL context guards in Lean library
- `04e079159` ci(evm): require 128 independent CALLVALUE/SELFBALANCE/ADDRESS actual-bytecode matches
- `6ede61776` assurance(evm): pin actual EVM context execution sources and 128-case oracle (pending CI)
- `e59416f5c` ci(mainnet): dedicated fail-closed offline proof-backed 2015 transaction and block root replay in two implementations
- `840c99799` fix(evm): correct Frontier Keccak padding and compose replay gates
- `be578f90d` feat(evm): integrate calldata, CALL repairs and read-only chain evidence
- `c33266528` feat(evm): execute guarded Solidity and a deployed OP Sepolia call
- `b4bae69ac` feat(evm): implement full-precision ADDMOD and MULMOD with proof and oracle gates
- `5f90c3e6f` fix(evm): qualify transitivity lemma in modular arithmetic proofs
- `f9fec7cbc` Execute nested EVM CALL with calldata, return data and independent client checks
- `d752d109d` Record nested CALL proofs, independent results, timing samples and full Ethereum goal
- `997211564` feat(evm): implement signed SDIV SMOD SAR and connected Lean statements
- `6bfe56b3e` feat(evm): permit signed context-free ops in guarded frame
- `efcdb287d` test(evm): exercise signed arithmetic/shift edges and actual dispatcher
- `96095683a` test(evm): compare 198 signed operation paths against pinned EthereumJS
- `5a01274df` evidence(evm): pin signed opcode sources without premature proof claim
- `0147217e8` ci(evm): require 381 signed/solidity comparisons and 75 pinned sources
- `4143a52ec` docs(evm): list signed division remainder and arithmetic right shift
- `fe2642756` docs(evm): record signed opcode theorem scope and reproduction gates
- `5945f56aa` fix(evm): decide signed predicates before Boolean sign comparison
- `8be7569c9` evidence(evm): refresh signed dispatcher blob after type-safe predicate fix
- `265c7cac6` fix(evm): avoid forward reference to signBit in signed division
- `41242a3fc` evidence(evm): repin compilable early signed division definition
- `cc1c0603b` proof(evm): select seven actually compiled signed opcode axiom sets
- `f1be80600` ci(evm): fail closed on all 103 printed theorem axiom sets
- `22a2b6ab0` fix(evm): audit qualified Word theorem symbols in source-pinned ledger
- `90bd86bd2` feat(evm): execute SIGNEXTEND with bounded byte index and differential guards

