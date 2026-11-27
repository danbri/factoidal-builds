### Since the previous full run: +34 subtests (+0.0015 points)

Previous: `20261127T0620Z-wpt-linux-x86_64-gh45946880270a1`, core `0e05ae111`, 92.7960%. This run: core `0a4c26613`, 92.7975%; 31 commits between.
Tests that lost subtests: 1 (-1); that gained: 5 (+35). Page outcomes: ERROR -7, NO_RESULT +1, OK +12, TIMEOUT -6.

**Directories that fell** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| third_party/test262 | 53,838 | 46,418 | 46,417 | -1 |

**Directories that rose** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webaudio | 5,873 | 3,617 | 3,651 | +34 |
| fetch | 13,314 | 8,822 | 8,823 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 1 directories, the first 1)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| third_party/test262 | 1 | 1 |

**Tests that lost most** (the first 1 of 1)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /third_party/test262/test/built-ins/RegExp/property-escapes/generated/Script_-_Glagolitic.test262.html | 1 | 0 | 1 |

**Commits between** (31)

- `b029c8c9e` Ethereum precompiles: ecrecover, SHA-256, RIPEMD-160, modexp and BLAKE2f in pure Lean, routed through CALL
- `5c5277468` Ethereum precompiles: native runner, published vectors with negative controls, axiom audit and CI
- `ae4cf3caa` BLAKE2f: straight-line rounds on unboxed words (about 13 times faster per round)
- `2756b6507` Ethereum precompiles: alt_bn128 add, mul and pairing; local SHA-256; evidence pins for the grown import closure
- `72a7a6c88` Ethereum wallet: empty stand-alone Lake package for transactions, signing, keys and ABI
- `9f51a1d6a` secp256k1: one shared Jacobian module with a narrow import closure; ecrecover moves to its own module
- `ca896bd40` Ethereum wallet: RFC 6979 secp256k1 signing with low-s and a recovery self-check, on the shared point arithmetic
- `1cb3ce4c3` Ethereum precompiles: KZG point evaluation (0x0a) and the BLS12-381 set (0x0b-0x11)
- `d0bbae76d` Ethereum wallet: unsigned transactions of kinds 0 to 4, signing payloads, and signed encodings read back by the independent decoder
- `0e1cdf109` Precompile field arithmetic: division-free addition, subtraction and negation on canonical values
- `9316abeb8` Precompiles: record of what runs where, what is proved and only tested, vectors, timings and the code-sharing decisions
- `48b137e7a` MODEXP: proof that the exponent loop computes base ^ exponent % modulus
- `086812b02` P256VERIFY (0x100, EIP-7951) under the osaka profile
- `1187e7cf8` Ethereum wallet: eth-wallet-sign tool, vector suites, EthereumJS differential, CI workflow and design record
- `895d3e87b` Wallet signing record: counts of the full execution-specs vector run (12,871 reproduced, 14 refused as the fixtures expect)
- `f7ffbd3da` Fp12: dedicated squaring (symmetric products once), guarded equal to mul a a on both pairing curves
- `d045f1e1d` Wallet signing: fixes from an adversarial review
- `1d1b3c49a` Merge main 681a4432730c into the precompiles branch
- `d9414d64b` Wallet: shared secp256k1 files at the precompile work's head f7ffbd3da; workflow without a concurrency group
- `c3b03258a` Merge main f7619f1a29b2
- `aa3515728` SPARQL differential: profile ext (property paths, VALUES, subqueries, EXISTS, aggregates with HAVING, CONSTRUCT); numeric literals compare b
- `e3d72a060` npm test: expected failures for EXISTS with a literal substituted into the subject (issue 1210) and SUM/AVG of an unbound variable (issue 12
- `eb99b837a` Formal-verification review: section 8, defects found by the campaigns
- `406216a9d` Merge pull request #1193 from danbri/wip/eth-precompiles-20261127
- `4c5751938` Merge main 406216a9d4b2
- `09804c3f2` Foafnaut: the main-thread engine uses the native library, in an engine session of its own
- `7e283bd07` WPT runner: a page with a real-time AudioContext keeps its clock with real time (issue 1169)
- `8787a5b7c` Foafnaut pages: tone.html, a 440 Hz sine through a real-time AudioContext (gain 0.25), linked from the new tab page (issue 1169)
- `a834b9d38` Engine start: compile functions at first call; no audio or IDNA work at module start; faster realm decode
- `98eb72ae0` Web Audio: a new AudioContext is suspended until the rendering side reports running (issue 1169)
- `0a4c26613` Merge pull request #1199 from danbri/wip/eth-wallet-sign-20261127

