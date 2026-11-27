### Since the previous full run: +963 subtests (+0.0423 points)

Previous: `20261127T0433Z-wpt-linux-x86_64-gh45936472171a1`, core `9a8ffacab`, 92.7762%. This run: core `f7619f1a2`, 92.8185%; 48 commits between.
Tests that lost subtests: 3 (-36); that gained: 76 (+999). Page outcomes: ERROR +7, OK +239, SKIP other -253, STALL -3, TIMEOUT +10.

**Directories that rose** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webdriver | 10,555 | 12 | 889 | +877 |
| webaudio | 5,873 | 3,393 | 3,474 | +81 |
| webnn | 14,256 | 14,205 | 14,208 | +3 |
| third_party/test262 | 53,838 | 46,416 | 46,418 | +2 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 1 directories, the first 1)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| webaudio/the-audio-api | 36 | 3 |

**Tests that lost most** (the first 3 of 3)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /webaudio/the-audio-api/the-audiocontext-interface/audiocontextoptions.html | 41 | 11 | 41 |
| /webaudio/the-audio-api/the-audiocontext-interface/suspend-after-construct.html | 5 | 0 | 5 |
| /webaudio/the-audio-api/the-audiocontext-interface/audiocontext-suspend-resume.html | 4 | 3 | 4 |

**Commits between** (48)

- `3e2745226` prelude.js: the Web Audio page classes over ops 173 to 189 (interface table from Lean, Web IDL conversions, errors as DOMExceptions, Offline
- `3406f844b` Merge remote-tracking branch 'origin/wip/1169-webaudio-prelude' into wip/1169-realtime-run
- `67b8651af` WebAudio.RenderSide: the rendering side of a real-time context as pure functions (messages in order, quanta for the output, reports; theorem
- `ea290dd28` WebAudio.Api.takeDecodeJobs: List.mergeSort in place of Array.qsort (the tail-recursion gate); allow-list rows for RenderSide.quanta and Rin
- `97a489f29` Foafnaut: real-time Web Audio in the engine (issue 1169, D3 first part)
- `7cf6c0772` Foafnaut real-time Web Audio: the runs end with their engine session (web_session_free and the end of a task session call WebDocument.engine
- `f3d36fdb9` Audio plan 13.10: D3 first part landed on wip/1169-realtime-run, with its measures (440 Hz bit for bit with no under-run, rendering thread C
- `37ca8a4b5` WebAudioRun: the module doc says when the quanta go in one write (after the sink opens or after resume) (issue 1169)
- `d49774c91` Merge remote-tracking branch 'origin/main' into wip/1169-autoplay
- `26e713331` Web Audio autoplay rule (owner, 2026-11-26): permission to start with no user activation is the risk token Risk.audioWithoutActivation, made
- `e64f67f64` Autoplay rule: the Hub's Settings page says its browser has no audio output; plan 13.10 lists what the autoplay work changed (issue 1169)
- `2229477b0` LabHygiene: the owner approved the raise for the audio output on 2026-11-27 (formal extern 32 to 38, opaque 1 to 2); CLAUDE.md records it (i
- `53e146a1d` Web Audio: decodeAudioData in pages on ops 194 and 195, and linear-time large buffers
- `d925b6875` Merge remote-tracking branch 'origin/wip/1169-page-decode' into wip/1169-autoplay
- `cdb159715` Merge remote-tracking branch 'origin/main' into wip/1169-autoplay
- `0052ce97d` webaudio_decode_test.ts: expected failure of issue 1177 (one page call carries at most 64 MiB, so an AudioBuffer of 18 million samples can n
- `b531edfac` Audio plan 13.10: the 64 MiB limit of one page call is issue 1177, with its expected-failure case
- `f768abd72` Autoplay rule: activation also from the host's pointer and click actions (the window's mouse input), in both engines, before the events are 
- `d7d1705c1` BubblePopJS call capacity 1 GiB and Web Audio maxSamples 2^27 on a 64-bit host (64 MiB and 2^25 stay on 32-bit hosts and in the QuickJS buil
- `0e4877cee` WebAudio.Api: the refusal guards test the new maxSamples (32 channels of 5,000,000 frames, and maxSamples + 1)
- `85fc8426f` HostContract.relaxFields on one line again: host_contract_source_test.ts reads it from one line
- `9fd871e24` WebScripts: the pointer action's activation as a let before the run (Lean's column rule had cut the application)
- `3506d9d62` factoidal-lean-basics: the trap of an argument on a new line left of a match arm's right-hand side (2026-11-27, one failed engine build)
- `1ada37a0f` Claim hypothesis witnesses (issue 1180, P3): 3 witnessed, 4 with a reason, gate ratchet
- `2c8633375` WebApi.maxInput as LeanJS.outCap: 1 GiB on a 64-bit host, 64 MiB on a 32-bit host, with a guard that they agree (the web_api argument block 
- `fc63297af` dataflow-inventory.md: list the new directory Claims among the directories no entry names (the Dataflow gate's regeneration of PR 1192)
- `7f8d127e2` Merge remote-tracking branch 'origin/main' into wip/1169-autoplay
- `376184759` Render scores: svg-tiny-pixels with SFNT fonts (run at wip/1165-fonts 7870fb3ab, engine of a4947f8ce); SVG text keeps a sole SVG font's miss
- `38238d732` leanjs compile-stats: why each function is not compiled to the register machine (issue 471)
- `555561681` Constant-time check: clang x86-64 branch in HACL* mod_exp_consttime recorded as expected failure (issue 1200); pipefail on the Valgrind job
- `ed1cebc65` Render scores: svg-tiny-acceptance at 787b48a66
- `37b229d2c` Merge pull request #1192 from danbri/wip/1180-claim-witnesses
- `41238e3f7` Turtle differential campaign, Factoidal against Oxigraph (issue 1184, P7): random Turtle with the grammar's harder forms, compared by RDFC-1
- `b2a3922e6` CLAUDE.md: owner decisions of 2026-11-27 on Foafnaut timelines, remote debugging and WebDriver scores
- `c50158c64` Merge remote-tracking branch 'origin/main' into wip/1169-autoplay
- `b43cde018` foafnaut skill: trap, a pull while build-web-render.sh runs gives an engine of no single commit
- `301e85c74` factoidal-lean-basics: checking one lab module alone is valid only when no library module it imports changed (2026-11-27, false errors after
- `b45f02cbd` Foafnaut: trace_to_perfetto.py, a run's trace records as a Trace Event Format timeline (Perfetto, Chrome DevTools)
- `e4686e0c7` Foafnaut WebDriver BiDi: design record for stage 1 (issue 372): transport, where each decision is, gate and invariants of issue 1120, module
- `a81b7c9fe` Differential campaigns: also run against the newest web build of main (tools/fetch-builds.sh --set web), so a fix shows before a release
- `17b8d8067` WebDriver BiDi in Lean, stage 1 (issue 372): message parse and BiDi errors, session.status/new/end/subscribe/unsubscribe, browsingContext.ge
- `8b350fa2d` BubblePopJS: a built-in call makes no result cells for its step charge, and Math's one-argument functions take no closure (issue 471)
- `663dad2f3` Merge remote-tracking branch 'origin/main' into wip/1169-autoplay
- `559ea8f38` SVG Tiny 1.2 uDOM: TraitAccess, SVGMatrix, SVGPath, SVGRGBColor, SVGException in the page realm; web_api ops 210 and 211 call DOM.SvgTinyTra
- `c4e660941` SVGScript: leave out of the drawing copy an attribute with a colon in its name and no namespace (udom-dom-209 was refused after step 1; issu
- `681a44327` Page host: a tor wire goes only through the Tor route; Tor mode refuses direct wires and WebSockets (issue 1060)
- `7e855fa9b` BubblePopJS: a call to compiled code makes no tuple for its callee (issue 471)
- `f7619f1a2` Render scores: svg-tiny-pixels at 376184759, border out, SFNT fonts in

