### Since the previous full run: -8 subtests (-0.0004 points)

Previous: `20261127T1738Z-wpt-linux-x86_64-gh46043399366a1`, core `66a5a8b51`, 92.8250%. This run: core `51bcef8c8`, 92.8247%; 13 commits between.
Tests that lost subtests: 2 (-9); that gained: 1 (+1). Page outcomes: ERROR -1, OK +1, STALL -1, TIMEOUT +1.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/semantics | 22,538 | 15,744 | 15,737 | -7 |
| preload | 956 | 243 | 242 | -1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| html/semantics | 8 | 1 |
| preload | 1 | 1 |

**Tests that lost most** (the first 2 of 2)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /html/semantics/interactive-elements/the-dialog-element/toggle-events.html | 8 | 0 | 12 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |

**Commits between** (13)

- `c550e938a` Ethereum wallet ABI: byte windows, ABI types and values, encoding and single-pass strict decoding
- `25acdbaa7` Ethereum wallet ABI: round-trip and strictness theorems, type-string parser, selectors, calldata, event logs
- `d7d593b34` Ethereum wallet: bounded JSON reader, EIP-712 typed data and EIP-191 digests; shared srcDir stanzas
- `bfcde9769` Ethereum wallet: pinned addresses, known-call builders, confirmation summaries with warnings, CREATE/CREATE2 prediction
- `37eb63324` Ethereum wallet ABI: 235 vectors and negative controls, wallet-abi-vectors executable (built-in, differential, timings)
- `186571dd3` Ethereum wallet ABI: axiom reports, differential oracle (ethers, viem) and CI workflow, recursion bounds, design note on misleading signing 
- `7a1e2b5e9` Ethereum wallet ABI: limb-wise word read and write, byte-array encoder proved equal to the specification and used by the strict decoder, sel
- `5c86e747b` Ethereum wallet ABI: risk token for hashing message data, width refusals in the single pass, domain field order, chain-aware warnings (unkno
- `539d8c42f` Ethereum wallet ABI: list describeTx_keeps for the axiom audit; vector thresholds
- `54e21485f` Merge the wallet signing branch into the ABI branch: root imports, lakefile tools and README sections kept from both
- `16a521dfe` Merge main 0a4c26613265
- `3cc1d1dc9` Merge pull request #1202 from danbri/wip/eth-wallet-abi-20261127
- `51bcef8c8` Foafnaut page loader: Tor mode through the engine's navigation and subresource ops (issue 1060)

