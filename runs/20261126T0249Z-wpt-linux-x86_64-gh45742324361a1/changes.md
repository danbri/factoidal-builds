### Since the previous full run: -1 subtests (-0.0000 points)

Previous: `20261126T0150Z-wpt-linux-x86_64-gh45738300795a1`, core `8a782f5af`, 92.6627%. This run: core `b8dca504b`, 92.6627%; 11 commits between.
Tests that lost subtests: 2 (-2); that gained: 1 (+1). Page outcomes: OK -1, STALL +2, TIMEOUT -1.

**Directories that fell** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/semantics | 22,523 | 15,752 | 15,751 | -1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| html/semantics | 1 | 1 |
| third_party/test262 | 1 | 1 |

**Tests that lost most** (the first 2 of 2)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /html/semantics/embedded-content/the-img-element/list-of-available-images-does-not-coalesce-in-flight-requests.sub.tentative.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/Temporal/PlainDateTime/prototype/withPlainTime/argument-string-time-zone-annotation.test262.html | 1 | 0 | 1 |

**Commits between** (11)

- `685c5c6f0` Allow the documented 200 KB Brotli growth budget
- `6ca81335c` Preserve executable checker and clarify compressed allowance
- `dd8370b7c` Canvas 2D: source-over pixel loop on USize indices (issue 1098)
- `b7286ac78` Merge pull request #1144 from danbri/codex/brotli-200kb-budget
- `aeb0a9714` Foafnaut host: a timer turn's canvas replay runs after the next turn is asked (issue 1098)
- `d67f5299a` skills/foafnaut: the timer turns line and how to split a canvas game's frame (issue 1098)
- `6da335275` Canvas 2D: clip mask by rows on USize indices (issue 1098)
- `aaf191ff3` Canvas 2D host: decode pixels with the built-in base64 decoder; accept a rectangle origin; cost bench (issue 1098)
- `20f512411` Canvas 2D: upload only the rectangle drawn since the last upload; BubblePopJS writes Float32 and Float64 typed-array bytes by shifts (issue 
- `2d7079e48` Canvas 2D: rleRect reads ranges with no closure; Wire.f64 with no list; canvas2d_test runs with no Chrome; upload bytes in the host trace (i
- `b8dca504b` Canvas cost bench: a game frame case (full-canvas gradient and 300 rects); Particle Rex play steps for the Linux rig (issue 1098)

