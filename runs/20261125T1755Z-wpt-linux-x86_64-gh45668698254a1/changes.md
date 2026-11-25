### Since the previous full run: +13 subtests (+0.0006 points)

Previous: `20261125T1702Z-wpt-linux-x86_64-gh45657456869a1`, core `98cf12b45`, 92.6334%. This run: core `76f307e51`, 92.6340%; 12 commits between.
Tests that lost subtests: 2 (-2); that gained: 8 (+15). Page outcomes: CRASH -1, ERROR -2, STALL +2, TIMEOUT +1.

**Directories that fell** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 4,138 | 2,721 | 2,720 | -1 |

**Directories that rose** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/semantics | 22,523 | 15,602 | 15,616 | +14 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| third_party/test262 | 1 | 1 |
| webcodecs | 1 | 1 |

**Tests that lost most** (the first 2 of 2)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /third_party/test262/test/built-ins/RegExp/property-escapes/generated/strings/Emoji_Keycap_Sequence.test262.html | 1 | 0 | 1 |
| /webcodecs/image-decoder.https.any.html | 9 | 8 | 47 |

**Commits between** (12)

- `22b51b930` Foafnaut engine: image decode per file and document word shaping in tasks, with decodesFor_eq and rememberPar_eq; real-page first-layout ben
- `0b569a62b` Blocks use the window's width; dotted lines join wrapped chains
- `f606a4a12` Query page titles span the blocks' width, a size smaller, and wrap evenly
- `9d8f0fab6` Avoid arbitrary-precision conversion when sampling bitmap bytes
- `948bc8539` Merge remote-tracking branch 'origin/wip/1031-engine-par'
- `8492ff6ad` Foafnaut engine: parallel image decode and word shaping measured on 5 real pages (first compile 0.94, relayout 0.92, same scenes); record se
- `214fcd033` CLAUDE.md: one engine worker per tab stays the default; new tab page and Particle Rex (owner, 2026-11-25)
- `c575c92a7` Validate submitters and form constraints before submission
- `577ac9b87` Foafnaut Tor record: what Deno can give the Arti wasm client (section 11)
- `e073b9f05` Send composed input and commit text edits when focus leaves
- `02db5c481` Show the new page URL in the first presented frame
- `76f307e51` After a pivot the rows are pairs: say so, count it, and show the answer's shape

