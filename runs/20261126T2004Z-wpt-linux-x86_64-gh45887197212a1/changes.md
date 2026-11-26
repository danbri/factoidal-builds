### Since the previous full run: -30 subtests (-0.0013 points)

Previous: `20261126T1917Z-wpt-linux-x86_64-gh45882517268a1`, core `38690d66d`, 92.6584%. This run: core `25ed4f09e`, 92.6571%; 21 commits between.
Tests that lost subtests: 1 (-30); that gained: 0 (+0). Page outcomes: CRASH +1, OK -4, STALL +3.

**Directories that fell** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| streams | 5,796 | 5,580 | 5,550 | -30 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 1 directories, the first 1)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| streams/piping | 30 | 1 |

**Tests that lost most** (the first 1 of 1)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /streams/piping/close-propagation-forward.any.html | 30 | 0 | 30 |

**Commits between** (21)

- `e52b2283b` Tail-recursion allow list: BubblePopJS destructuring lowering (dstr*), bounded by fuel 10000
- `ab762954b` Media.Wav: RIFF/WAVE reader (PCM, float, A-law, mu-law, extensible) with guards (issue 1169)
- `f5a471026` Media.Decode: float paths opusF32, vorbisF32, mp3F32 and the Ogg and WebM readers over them (issue 1169)
- `745032a7d` WebAudio.Decode: decodeAudioData, windowed-sinc resampler, media-bench decode (issue 1169)
- `a17dd53f9` Media tests: Wav cases; media-bench decode
- `afc75cd4b` Audio plan: decodeAudioData core landed (issue 1169)
- `295173571` WebAudio.Api: page operations 173 to 189 and the contexts kept between script turns (issue 1169)
- `7dd1842b2` WebApi: route ops 173 to 189 to WebAudio.Api; Web Audio state in State.audio (issue 1169)
- `cdd5a0600` WebAudio.Api: the sine guard checks sin(2 pi 440 k / 44100) at frames 1 and 100 within 1e-6 (the earlier expected value was wrong)
- `de2b4cb94` Audio plan: Web Audio ops are 173 to 189; Lean side landed (issue 1169)
- `580e36fcb` WebAudio Mix: tail-recursive mixInput with mixInput_shape theorem
- `4c47e2a7c` WebAudio: tail-recursive Mix.apply with shape theorem; delay minimum wins in a cycle; delay line re-mixed on input channel count change
- `3ccc730bc` Audio plan: record fixes of defects 3, 4, 5
- `c3f61291b` WebAudio graph: mute delay cycles made only of delayTime connections; isMuted by node id (1169)
- `127ed88e5` WebAudio graph: prove completeness of the reachability search (reach_complete, onCycle_iff)
- `583c75d5f` WebAudio graph: prove order_complete for well-formed graphs (Kahn completeness, acyclicity of live steps), WellFormed preserved by connect
- `e9f637920` WebAudio graph: header, umbrella line and guards 31, 32 for order_complete
- `b74f365cc` Audio plan: graph order completeness proved; the delayTime-only delay cycle defect it found (issue 1169)
- `0d92effb4` Audio plan: stage D design (real-time AudioContext: rendering task, control messages, ring, sinks, ops 190 to 193) (issue 1169)
- `744282b88` Foafnaut: jukebox page on the Web Audio API (MP3, Ogg Vorbis, Opus, WAV; gapless play; click-to-sound from getOutputTimestamp), generated wi
- `25ed4f09e` Audio plan: decodeAudioData in pages as a Lean task job (ops 194, 195) and where the engine reads the decoder modules (issue 1169)

