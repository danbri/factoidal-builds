### Since the previous full run: +624 subtests (+0.0274 points)

Previous: `20261126T2101Z-wpt-linux-x86_64-gh45893348551a1`, core `c105a71cc`, 92.6296%. This run: core `87d5c360a`, 92.6571%; 12 commits between.
Tests that lost subtests: 2 (-31); that gained: 2 (+655). Page outcomes: unchanged.

**Directories that fell** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| streams | 5,796 | 5,580 | 5,550 | -30 |

**Directories that rose** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| shadow-dom | 14,726 | 13,500 | 14,154 | +654 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| streams/piping | 30 | 1 |
| third_party/test262 | 1 | 1 |

**Tests that lost most** (the first 2 of 2)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /streams/piping/close-propagation-forward.any.html | 30 | 0 | 30 |
| /third_party/test262/test/language/expressions/exponentiation/applying-the-exp-operator_A5.test262.html | 1 | 0 | 1 |

**Commits between** (12)

- `fa0a6fe04` WebAudio.Ring: the output ring as a Lean state machine, with invariant, order, under-run and no-overwrite theorems (issue 1169, D1)
- `7253268ab` audio sink: C ring, null and wav consumers, Wasm stub (issue 1169, D1)
- `82716d1e2` audio sink: Lean externs, Lake target and test executable (issue 1169, D1)
- `46a049865` audio sink: consumer waits for the first write; tests/audio (TSan stress, trace replay, WAV check); plan 13.5 (issue 1169, D1)
- `ffec1a393` build-web-render.sh: the audio sink in the native and Wasm builds; plan 13.10 D1; WebAudio umbrella doc (issue 1169)
- `be05254f2` Audio plan: D1 status, native full build not finished in the cloud cap (issue 1169)
- `e3b1f0c16` audio sink: the coreaudio consumer (default output unit, ring-reading render callback, device rate and latency) and the macOS AudioToolbox a
- `5d8d92be4` build-web-render.sh: the audio sink symbol check reads all of nm's output (no SIGPIPE under pipefail)
- `d7cd59f73` WebAudio.Api: real-time contexts in the page state (ops 190 to 196, outbox, report merge), paramCall setValueCurveAtTime and cancelAndHoldAt
- `9b18f9fd2` WebAudio.Api: theorems for outbox, report merge, takeOutbox and decode jobs; guards for ops 190 to 196; routing 173 to 199
- `457c9190c` Audio plan: D2 Lean part landed, op table changes (13.8, 13.10)
- `87d5c360a` WebAudio: insertAfterEqual as a loop proved equal by @[csimp] (issue 1172)

