### Since the previous full run: +78 subtests (+0.0034 points)

Previous: `20261126T1752Z-wpt-linux-x86_64-gh45871410277a1`, core `4a81bddce`, 92.6550%. This run: core `38690d66d`, 92.6584%; 75 commits between.
Tests that lost subtests: 1 (-1); that gained: 68 (+79). Page outcomes: CRASH -1, ERROR -28, OK +39, STALL -1, TIMEOUT -9.

**Directories that fell** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| fetch | 13,314 | 8,823 | 8,822 | -1 |

**Directories that rose** (5; the first 5)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| third_party/test262 | 53,838 | 46,355 | 46,418 | +63 |
| referrer-policy | 8,815 | 5,748 | 5,754 | +6 |
| fs | 1,123 | 995 | 1,000 | +5 |
| html/infrastructure | 1,664 | 985 | 989 | +4 |
| secure-contexts | 86 | 13 | 14 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 1 directories, the first 1)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| fetch/metadata | 1 | 1 |

**Tests that lost most** (the first 1 of 1)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /fetch/metadata/generated/element-img.https.sub.html | 18 | 17 | 45 |

**Commits between** (75)

- `33de80525` Tor wasm build on macOS: use Homebrew LLVM for ring's C (Apple clang has no wasm32 target)
- `994dd4adb` Tor host: --trace-conns, one line per TCP connection (times, bytes, connect errors; no addresses)
- `225aa1799` Foafnaut: engine time by subsystem (BubblePopJS, canvas raster, page paint) on three pages
- `b69bcd66d` svg-tiny-pixels: count a case that needs animation apart (NEEDS_ANIMATION)
- `33433d433` Tor host: event-loop lag in --trace-conns; PAR/END groups run streams at once; private network test runs 6 at once
- `41e93d0a9` Foafnaut: status of Web Audio, audio for media and GPU video; decisions for the owner
- `469ff4f77` Tor: stream API in the module, SOCKS5 server in the worker, NO_PROXY bypass found and closed
- `1afce5e83` BubblePopJS: yield and await in destructuring, tagged templates, ++, super[], logical assignment
- `642062d6c` SVG: accept version and baseProfile on svg (SVG Tiny 1.2 §5.1.2)
- `0915cb321` SVG: xml:id is an element identifier (SVG Tiny 1.2 §5.10.2)
- `8d0305aa9` SVG: elements in unknown namespaces are private data, not rendered (SVG Tiny 1.2 §23.1)
- `7d12da2ef` SVG: text and font properties pass on non-text elements; xml:id wins over id
- `10b49dccf` Render scores: svg-tiny-admission measured at 225aa179 and after the profile, xml:id, private-data and text-property steps
- `518998560` SVG Tiny admission: draw text through the Lean text lowering, strictly
- `5a198d2b3` Render scores: svg-tiny-admission 137 admitted of 496 (SVG text lowered in Lean)
- `e33848e6b` Tor trace: OS error text (addresses removed) and address family per connection; summary counts connect timeouts, still connecting, IPv6
- `1d197c7c3` Tor record section 19: Mac public-network failure, cause open; corrects the claim in the e33848e6b message
- `36cf00ede` Tor record section 19: the OONI measurement is another user on the same ISP, not the owner's Mac
- `9e4222acc` SVG: viewport-fill, zoomAndPan, polygon points lacuna; name the refused graphics child
- `e50d50603` Render scores: svg-tiny-admission 142 admitted of 496
- `3f52b2c0d` BubblePopJS: octal escape at the end of a class range; yield in a for-of or for-in target
- `ba7a04275` Render scores: wpt-images-native measured on Linux at 225aa1799 (6 pass of 279); run.py records the real host
- `769ba957a` Foafnaut: trace the time of each page-load step before the first frame; engine_time_split windows load and first-layout
- `f02427311` Render scores: svg-tiny-pixels measured again at b69bcd66d (Linux, Mesa lavapipe)
- `d1eb61624` SVG: refuse timed elements in defs and SVG fonts on the strict text path
- `eabb4e044` Render scores: svg-tiny-admission 115 admitted of 496
- `7470bdadf` Tor trace: ClientHello size and time, write count, peer end of stream, read errors; record the hotspot run (first public onion fetch; exit r
- `b629c2b71` BubblePopJS tier 2: inline cache for property reads measured, not landed; LTO default needs three packages in factoidal-builds (issue 471)
- `a5231ad28` Tor record section 18: owner's request for theorems on the SOCKS5 decisions, and the plan
- `4a2ab162e` CLAUDE.md: Tor switch in Settings, confirmed by typing LOL-YOLO-I-WILL-REGRET-THIS-FOLLY (owner, 2026-11-26)
- `43817f658` Hub pages in Foafnaut: design record, two traps in the foafnaut skill, Textnaut --verbose settle trace
- `b211f43d4` Media: decoder modules pinned by SHA-256, MP3 test clips, audio plan; owner's decisions recorded
- `94b26052e` Tor: scrub IP addresses from every Arti log line (a debug line printed relay addresses); record the second hotspot run (exit request answere
- `5bddeecfc` Web Audio channel rules in Lean: computedNumberOfChannels, up/down-mix matrices, theorems and guards (issue 1169 stage B)
- `4325a431b` WebAudio: library root and umbrella module, so the Web Audio theorems build in every lake build (issue 1169)
- `ab8261334` Lean SOCKS5 decisions of the Foafnaut Tor worker, with theorems
- `1d7107d9f` Audio plan: the structure of the Web Audio engine for stage B (issue 1169)
- `c7a85dc47` leanjs LTO: -K needs -R (a configured workspace built without LTO, no message); measured again on b629c2b71: instructions 0.951, size +1.98%
- `0128f6003` SOCKS5: keep a leading byte order mark in user names and hosts (TextDecoder removed it, so EF BB BF 61 was admitted as partition a); record 
- `1847fa078` Web Audio AudioParam automation event list in Lean: insertion, cancellation, value at time, theorems
- `dee25914f` Web Audio automation: guard tests from WPT cases, notes on what is not done
- `f23f93413` Web Audio automation: binary64 time sums and frame conversion, exact comparison of stored times
- `2b349eecf` WebAudio umbrella: import the AudioParam automation module (issue 1169)
- `f1887ceaf` WebAudio kernels: Gain, ConstantSource, Delay, StereoPanner, Splitter, Merger with shape theorems
- `059cbe3bb` WebAudio kernels: 67 #guard value tests for the six kernels
- `1fa0a0778` WebAudio umbrella: import the block kernels module (issue 1169)
- `bbd44a137` Media: MP3 stream reader in Lean, decoded one frame a call by the minimp3 module (issue 1169 stage C)
- `7507d103c` WebAudio.Graph: audio graph, connect and disconnect, processing order with DelayNode split and cycle muting, 36 guards (issue 1169)
- `7cce27238` WebAudio.Graph: theorems for order (nodup, topological, muted nodes on cycles) and idempotent connect
- `af0ae10fe` WebAudio umbrella: import the graph order module (issue 1169)
- `d0b9599a9` Audio plan: state of stage B files and the MP3 reader (issue 1169)
- `146a50bfb` WebAudio.Render: state of one context and one render quantum (issue 1169)
- `eeac31bff` WebAudio.Context: offline context, node creation, automation methods, startRendering, theorems and 58 guards (issue 1169)
- `fa0321aaf` WebAudio umbrella: import Render and Context (issue 1169)
- `47f4f9856` Audio plan: Render and Context landed; open defects of the engine files (issue 1169)
- `529ff0f25` Foafnaut: start a script session for a page whose only scripts are modules (inspect modules)
- `2d9fb5f09` Expected failures for page import() and Intl; regression guard for yield in a for-of target
- `27c4e37d1` WebAudio: AudioBuffer and AudioBufferSourceNode playback kernel in Lean, with theorems and tests (stage B, issue 1169)
- `59ad5d71d` WebAudio umbrella: import AudioBuffer and the buffer source (issue 1169)
- `531881c86` Web Audio: BiquadFilterNode coefficients, block kernel and getFrequencyResponse in Lean (issue 1169, stage B)
- `e270b721b` Web Audio: PeriodicWave, built-in waveforms and OscillatorNode block kernel in Lean (issue 1169, stage B)
- `6120b9264` WebAudio umbrella: import Oscillator and Filters (issue 1169)
- `d72eade61` Audio plan: design of the Web Audio page interfaces (ops 170 to 189, issue 1169)
- `37e894136` Generate the Web Audio IDL table in Lean from WPT webaudio.idl
- `937ee004e` WebAudio umbrella: import the IDL interface table (issue 1169)
- `c86a3e6c7` WebAudio Graph: parameter edges into a split DelayNode go to its reader step
- `1078485be` WebAudio Render: call the oscillator, biquad and buffer source kernels
- `c9d3edb30` WebAudio Context: create and configure oscillator, biquad filter and buffer source nodes
- `3a802c20a` WebAudio Context: render tests for oscillator, filter, buffer source and the split delay
- `e13f98d3c` Audio plan: oscillator, filter and buffer source rendered; graph defect 1 fixed (issue 1169)
- `0052ed5af` Hub pages in Foafnaut: measured results against Chrome, tools/hub-text-compare.py
- `f4621bc5c` skills/subagent-prompting: stop a cherry-pick landing loop at the first failure (a break returns 0)
- `7b55c4763` web-render CLI: --resources ROOT gives an HTML page its local images; native WPT harness passes the corpus root
- `897b9a280` WebRender: compileWith above the export attribute of compile
- `38690d66d` Render scores: wpt-images-native 9 pass of 279 at 2741abd21 (local images supplied)

