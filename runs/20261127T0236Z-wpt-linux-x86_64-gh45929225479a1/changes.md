### Since the previous full run: -23 subtests (-0.0010 points)

Previous: `20261127T0223Z-wpt-linux-x86_64-gh45928054998a1`, core `b70f732cd`, 92.7761%. This run: core `2a5550213`, 92.7751%; 40 commits between.
Tests that lost subtests: 3 (-25); that gained: 2 (+2). Page outcomes: OK -1, TIMEOUT +1.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| selection/contenteditable | 252 | 146 | 128 | -18 |
| webaudio | 5,873 | 3,393 | 3,387 | -6 |

**Directories that rose** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| secure-contexts | 86 | 13 | 14 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 3 directories, the first 3)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| selection/contenteditable | 18 | 1 |
| webaudio/the-audio-api | 6 | 1 |
| third_party/test262 | 1 | 1 |

**Tests that lost most** (the first 3 of 3)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /selection/contenteditable/modify-around-inline-element-boundary.tentative.html | 18 | 0 | 36 |
| /webaudio/the-audio-api/the-audioparam-interface/audioparam-setValueAtTime.html | 6 | 0 | 6 |
| /third_party/test262/test/built-ins/Temporal/PlainMonthDay/basic.test262.html | 1 | 0 | 1 |

**Commits between** (40)

- `64385ebb2` Tor record section 13: who does the networking in the Ethereum and Tor components
- `57f5f12c6` Network record section 9: TLS, what we do and what the host does, with the owner's direction
- `39f5a0b08` CLAUDE.md and the audio plan: the owner's answers of 2026-11-26 on AAC through AudioToolbox, the HRTF data set and the autoplay rule with --
- `a0b86f170` CLAUDE.md: owner's order of the BubblePopJS JIT work after tier 2 (global names, cheaper steps, shapes, LTO default); PR 475 closed; the JIT
- `59f250dd6` svg-tiny-pixels: leave the 3-pixel frame border out of the comparison (owner, 2026-11-27)
- `9336dea43` CLAUDE.md: one host runtime (Deno), XMPP must not break; owner decision of 2026-11-27, plan in issue 1176
- `0046786b9` Network record section 9: Deno 2.9.8 TLS stack (rustls 0.23.40, aws-lc-rs, Mozilla roots by default)
- `ca39dff2c` SVG text: SFNT fonts for a family or a character that the SVG font lacks; CLI takes several --svg-sfnt [FAMILY=]FILE
- `50f75872f` svg-tiny-pixels: report the bands with and without the border in one run, and the pixels left out
- `49c2af32e` CLAUDE.md: SVG Tiny 1.2 implemented in full; admission is a check, not the target (owner, 2026-11-27)
- `ec25a92ee` render-dashboard: --host and --chrome-arg for wpt-images-wasm on a Linux host
- `79563b7df` render-dashboard: put --chrome-arg flags inside the launch options
- `969493262` render-dashboard: serve finite_floats.ts to the 2 November harness (render_plan.ts imports it)
- `5edb2d6df` render-dashboard: --runner-limit for the wpt-images-wasm runner on a slow machine
- `3ddeb94b8` render-dashboard: HTML tests of wpt-images-wasm get the files that Lean asks for
- `e4e45004d` CLAUDE.md: npx factoidal stays on Node; no tie to one runtime; external-code exposure recorded (owner, 2026-11-27)
- `cd9ac11c3` Record of external code per network, TLS and crypto path (owner, 2026-11-27: exposure must be clear and documented)
- `31d61e2c5` SVG Tiny: say accepted and refused, not admitted and unsupported
- `6bc7a5413` engine_time_split.py: list the lab's own engine functions (NativeSVG, WebRender, ...), not only L4Factoidal ones
- `4c3c9ce36` XMPP host: check TLS certificates and keys before listening, on every runtime and TLS path (issue 1176)
- `fcd0a2f7b` Audio plan: the media decoders are on factoidal-builds main (57d766d3)
- `a93f1c257` SVG fonts on the strict path: text in an SVG font family is drawn with its glyphs (SVG Tiny 1.2 §20)
- `ca063378a` SVG Tiny 1.2 scripting: script, handler and listener run by BubblePopJS on the XML DOM before drawing (issue 1166)
- `0823ce240` Design record: the Anthropic formal-verification post compared with Factoidal practice, ten proposals
- `c012c955b` Formal-verification review: correct the Foafnaut TS/JS count (34,821 tracked lines, by kind) and add P11, the host boundary lint
- `edcc4910a` Formal-verification review: link issues 1178 to 1188 and batch 1189
- `6c93c4b80` SVG textArea: line breaks at UAX 14 opportunities; strict textArea with SVG fonts (SVG Tiny 1.2 §10.11)
- `49a0470b4` Claims register (issue 1178, P1) with statement freeze (issue 1179, P2): 12 proposed claims, static gate, axioms check in CI
- `ce66fd9db` SVG text, SFNT path: a right-to-left run with one positioned character starts its chunk at its first visual glyph
- `b35e44c9d` Theorem count with closed-value tests apart (issue 1186, P9); theorem-pipeline skill names the claims register
- `96ba8113b` npm-release skill: claims and found-by-proof lines in each release note (issue 1185, P8)
- `321794930` Foafnaut host policy ratchet (issue 1188, P11): 690 policy sites in 124 host files, held per file with a reason
- `0b6bb4b1e` Lean lemma index, built from the tree on each run (issue 1187, P10); proof skills name the search step
- `f5cb09d30` WebRender: an SVG image key with #xywh= draws that region as the whole image
- `01fab38f8` SVG font text, strict: glyph coverage walks SVGFont.pick as lowerText does (lang, arabic-form, ligatures)
- `f125afa19` SVG Tiny 1.2 animation at a document time (SVGAnimate)
- `d334a1191` SvgTinyProbe: the module description is a module doc comment
- `9b68b2d55` SVG animation: inherit, path data, dash arrays, font-size, repeat events, periodic intervals; the pixel path draws the snapshot
- `2a42be5e5` Panic-site ratchet for code the wasm reaches (issue 1181, P4 step 1): 1,276 sites in 937 modules
- `2a5550213` assurance.json writer (issue 1182, P5 core side); claims name their dataflow stages

