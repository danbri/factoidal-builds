### Since the previous full run: -511 subtests (-0.0225 points)

Previous: `20261127T0530Z-wpt-linux-x86_64-gh45941782781a1`, core `f7619f1a2`, 92.8185%. This run: core `0e05ae111`, 92.7960%; 29 commits between.
Tests that lost subtests: 3 (-657); that gained: 21 (+146). Page outcomes: OK -2, STALL +2.

**Directories that fell** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| shadow-dom | 14,726 | 14,154 | 13,500 | -654 |

**Directories that rose** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webaudio | 5,873 | 3,474 | 3,617 | +143 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| shadow-dom/declarative | 654 | 1 |
| webaudio/the-audio-api | 3 | 2 |

**Tests that lost most** (the first 3 of 3)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /shadow-dom/declarative/declarative-shadow-dom-attachment.html | 654 | 0 | 654 |
| /webaudio/the-audio-api/the-audiocontext-interface/audiocontext-detached-execution-context.html | 4 | 2 | 7 |
| /webaudio/the-audio-api/the-audioparam-interface/k-rate-audiobuffersource-connections.html | 2 | 1 | 2 |

**Commits between** (29)

- `9af616560` WebAudio: AudioParam value reads clamped to the nominal range; BiquadFilterNode gain maximum in single precision; AudioBufferSourceNode detu
- `226f189db` WebAudio: offline rendering in steps (op 187 with a quantum count), suspend, resume, close and chunked startRendering in the page; one chann
- `593b4107b` WebAudio: ended events per render step; buffer playback extrapolates past the last frame; grain duration includes the sub-sample start (issu
- `a747b2180` WebAudio: node outputs rounded to binary32 (issue 1169)
- `08533c7bd` WebAudio: an AudioBufferSourceNode acquires its buffer's content at start() (op 184 with acquire), and the arrays getChannelData returned ar
- `4dfd84714` WebAudio: BiquadFilterNode kernel in direct form I (time-varying coefficients as the specification's difference equation); notes (issue 1169
- `e5075fbb1` WebAudio: the buffer setter sends the dimensions before start(), the samples at start() (issue 1169)
- `19709a3fa` WebAudio: NaN test by isNaN (x != x is false for NaN in Lean); parameter computed values are binary32 (issue 1169)
- `a9125d85b` l4w3c --engine=shipped: the W3C SPARQL 1.1 suite through the shipped evaluator (issue 1183, P6)
- `a902829d3` l4w3c --engine=shipped: print how many SELECT/ASK queries went through shippedEvaluator and how many took the backend path; the workflow fai
- `36e2bc926` Audio plan: WPT webaudio round 1 (2,572 to 2,702 subtests), clusters and what remains; acquire keeps the earlier arrays attached (issue 1169
- `d4199ecdb` l4w3c --engine=shipped: count the queries the backend runner answered, apart from the reference fallback of shippedRun
- `4ca887d51` l4w3c --engine=shipped: take the backend from LawfulDataset.ofCertified, as the wasm op does (the assumption gate refuses a bare indexedData
- `ed3ce024e` Turtle: a prefixed name with prefix e<digits> in object position is not a number (found by the random Turtle campaign, issue 1184)
- `3941b0e7c` l4w3c --engine=shipped also reads the Turtle, N-Triples and N-Quads tests with the shipped readers (parseTurtleText, parseNTriplesDocument, 
- `0c02ca9db` Merge wip/1169-wpt-round1 (WPT webaudio round 1, issue 1169): op 184 is setBuffer(ctx, node, mode, channels, length, sampleRate, data...), w
- `ae8eb4e09` BubblePopJS: fastGet reads string wrapper methods directly; record of page time and the call path
- `41f633653` Merge pull request #1204 from danbri/wip/turtle-exponent-prefix
- `1d07850f5` Merge remote-tracking branch 'origin/main' into wip/1169-wpt-merge
- `6bc22879f` Audio plan 12b: WPT webaudio after the merges of 2026-11-27 (2,780 of 3,298 subtests pass, with --dangerously-permit-audio), the op 184 layo
- `1174be44c` wpt-runs skill: WebDriver classic (wdspec) runs in branch checks and full runs; first numbers
- `6ea6d45a1` Merge pull request #1195 from danbri/wip/1183-l4w3c-shipped
- `8dbb3f328` Differential campaign: TriG documents (default graph, { } blocks, GRAPH g { }, g { }) beside Turtle; the generator returns whole statements
- `37a473a00` Differential campaign: random RDF/XML documents (about, nodeID, ID with xml:base, typed nodes, property attributes, parseType Resource/Colle
- `ebbab72e2` RDF/XML campaign: no xml:lang="" (pyoxigraph 0.5.13 refuses it); count documents that are the same up to XMLLiteral namespace declarations a
- `007886281` Formal-verification review: section 7, reader campaign results and two pyoxigraph 0.5.13 behaviours recorded locally
- `8dd54dce0` Differential campaign: N-Triples and N-Quads documents (UCHAR in IRIs, ECHAR/UCHAR in literals, blank node labels with . - _ and non-ASCII, 
- `a2d04c99c` Differential campaign: mutated documents (one random edit each) for Turtle, N-Triples, N-Quads and TriG, so the readers' refusals are compar
- `0e05ae111` npm test: expected failures for two N-Triples/N-Quads statements on one line (issue 1209)

