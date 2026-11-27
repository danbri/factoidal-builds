### Since the previous full run: +2,679 subtests (+0.1177 points)

Previous: `20261126T2237Z-wpt-linux-x86_64-gh45901862984a1`, core `c7a52eea3`, 92.6584%. This run: core `b70f732cd`, 92.7761%; 250 commits between.
Tests that lost subtests: 7 (-7); that gained: 160 (+2,686). Page outcomes: ERROR -21, OK +14, STALL +3, TIMEOUT +4.

**Directories that fell** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| preload | 956 | 243 | 242 | -1 |

**Directories that rose** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webaudio | 5,873 | 714 | 3,393 | +2,679 |
| secure-contexts | 86 | 13 | 14 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 3 directories, the first 3)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| webaudio/the-audio-api | 5 | 5 |
| preload | 1 | 1 |
| third_party/test262 | 1 | 1 |

**Tests that lost most** (the first 7 of 7)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |
| /third_party/test262/test/built-ins/Temporal/PlainDateTime/compare/argument-string-critical-unknown-annotation.test262.html | 1 | 0 | 1 |
| /webaudio/the-audio-api/the-analysernode-interface/ctor-analyser.html | 16 | 15 | 78 |
| /webaudio/the-audio-api/the-iirfilternode-interface/iirfilter.html | 16 | 15 | 68 |
| /webaudio/the-audio-api/the-pannernode-interface/ctor-panner.html | 13 | 12 | 125 |
| /webaudio/the-audio-api/the-pannernode-interface/panner-distance-clamping.html | 7 | 6 | 51 |
| /webaudio/the-audio-api/the-waveshapernode-interface/ctor-waveshaper.html | 13 | 12 | 54 |

**Commits between** (250)

- `2f3e67721` fix(consensus): use kernel-checked decision for multiproof sort examples
- `5883087d8` fix(consensus): use transparent bounded SSZ helper sort for kernel equality proofs
- `bd72c142b` docs(consensus): pin exact-head verified multiproof axioms, 2048-case oracle and failure history
- `71a689094` docs(consensus): assess upstream proved EthLib SSZ and pin 4.35 integration gap
- `c46c17506` test(consensus): machine-check exact SSZ axiom ledger against Lean output and source blob
- `7c50781db` fix(consensus): match actual printed Lean theorem names and axiom lists
- `db570c0e7` Verify SSZ byte proofs with independent pure Lean SHA-256
- `b16380fbe` feat(consensus): pure Lean SSZ basic uint64/bool codecs and checked roots
- `852c778a5` feat(consensus): add native JSONL SSZ scalar codec transport
- `8914d7de0` build(consensus): register SSZ basic-type native entry point
- `e58869831` build(consensus): include SSZ scalar codecs in library and axiom audit
- `1f5605c91` test(consensus): compare SSZ scalar bytes and roots with independent Python
- `eae120b1e` ci(consensus): build and differentially test standalone SSZ basic codecs
- `1795c2a0d` test(consensus): make forged-root negative control differ from zero root
- `1f4e6aa66` fix(consensus): guard Except results using decidable equality, not missing BEq
- `6cbc3c917` fix(consensus): normalise multiline maximum uint64 guard
- `0a17a0667` fix(consensus): inspect scalar Except cases without unavailable equality instances
- `9eb1f46ff` fix(consensus): parenthesize checked decoder calls in guards
- `3c3e739f5` test(consensus): repin retained SSZ axiom evidence to extended source tree
- `c03e0d6e9` test(consensus): audit basic-codec theorem evidence with existing fail-closed ledger checker
- `79fe7fa01` test(consensus): pin seven actual SSZ scalar theorem axiom sets and source graph
- `ff680e6cc` ci(consensus): enforce seven source-pinned actual Lean scalar axiom reports
- `e00c09546` ci(consensus): retain scalar codec axiom and oracle outputs as evidence artefacts
- `0c9be2a2e` docs(consensus): record exact Lean scalar code, proofs, oracle coverage and failure corrections
- `40b8fc966` feat(consensus): implement bounded SSZ fixed uint64 vector packing and Merkle reduction
- `ab2a80b71` feat(consensus): expose pure Lean SSZ fixed vector verifier through JSONL
- `96782c4e4` test(consensus): independently compare packed uint64 SSZ roots with Python SHA-256
- `d6a538595` build(consensus): add native pure Lean fixed-vector SSZ executable
- `69c76721a` ci(consensus): fresh Lean vector proof build and independent SHA-256 oracle
- `c43f853b5` evidence(consensus): pin vector Merkle source blobs and theorem inventory
- `c7afa33d7` test(consensus): verify exact code blob pins and nine actual Lean axiom reports
- `2775ba27c` ci(consensus): fail closed on source-pinned vector theorem axiom inventory
- `cd6c5b1fa` proof(consensus): simplify failed Except.bind paths at actual vector entry
- `67948c3c2` evidence(consensus): repin vector proof source after monadic proof repair
- `d4831fe8d` evidence(consensus): record exact nine printed axiom sets and 1406 native comparisons
- `0a683a137` audit(consensus): require exact nine Lean axiom sets, not merely a foundation allowlist
- `05797b16f` docs(consensus): source-linked fixed-vector validation and corrected proof evidence
- `be457b1e8` feat(consensus): add typed SSZ beacon header and signing container roots
- `098ad4c05` feat(consensus): add checked JSONL entry for four beacon SSZ containers
- `ce2347c6d` test(consensus): independent 1461-case beacon SSZ container oracle
- `1a648bd89` build(consensus): compile checked SSZ container roots as Lean executable
- `819e09298` build(consensus): compile checked SSZ container roots as Lean executable
- `e1a888eec` ci(consensus): fresh Lean container proofs and independent Merkle comparison
- `334ec166b` test(consensus): add strict ten-claim printed-axiom source audit
- `e20294fb1` Implement independent fork-aware SSZ signing domains and proposer header roots
- `a69406bc8` Implement independent fixed attestation data and target-epoch signing roots (#868)
- `1afc4b935` Connect attestation signing to native consensus dispatcher
- `593ccd78f` Include attestation module in consensus library audit
- `c60292d7e` Refresh only aggregate consensus root pin for appended attestation import
- `07d844bd6` Refresh only aggregate consensus root pin for appended attestation import
- `c48b574ca` Add independent attestation byte and target-domain oracle with mutation controls
- `9c62e9711` Pin attestation code and check actual kernel axiom output
- `30fc4512e` Require native attestation comparison and printed axiom evidence in consensus CI
- `2f6818100` Record attestation implementation scope and pending proof/test evidence
- `4da645336` Add bounded consensus verification diagnostic for #872
- `da57d912f` Add bounded consensus verification diagnostic for #872
- `2acab381d` Run focused bounded SSZ builds before unchanged full consensus gate (#872)
- `5decf5cfe` Record repeated consensus build cancellation and exact local diagnostic results (#872)
- `ec423c87a` Repair explicit SSZ error and root paths (ContainerRoots.lean)
- `483e82812` Repair explicit SSZ error and root paths (AttestationData.lean)
- `b7b52f9cd` Bind active attestation audit to repaired source blobs
- `23cf3b9c2` Select the rejecting branch under the width inequality
- `59664192c` Refresh exact active fixed-container source pin
- `e70308cd2` Record observed container failure and repair evidence boundary
- `8465c5daf` Implement independent attester-slashing evidence preparation
- `f50febdf6` Connect checked slashing preparation to existing consensus JSON transport
- `28832ed1c` Advance active attestation transport source pin
- `ab69a02c0` Add independent indexed vote conflict and signing-root oracle
- `88c7c035a` Require actual slashing theorem reports and exact source pins
- `6a600c2df` Run slashing preparation proof, dependency and independent native gates
- `94ac12d2e` Bind slashing proof evidence to reused SHA2 theorem and dependency audit sources
- `f6c7f9c74` Record predecessor verification and new slashing evidence boundaries
- `5a5be19e9` Repair reserved Lean binder in indexed-attestation transport
- `fd04c9e36` Bind active axiom ledger to corrected transport source
- `95f479ac0` Bind active axiom ledger to corrected transport source
- `4f33710de` Record exact slashing build failure and bounded repair evidence
- `01d7a64b9` Implement Validator SSZ root and indexed registry proof admission
- `f3ff7e75d` Add bounded executable registry membership and candidate transport
- `b4d87e80d` Add independent sparse-tree registry vectors and comparator controls
- `1cd85b270` Run registry theorem and independent execution checks on pinned Lean

