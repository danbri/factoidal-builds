### Since the previous full run: +28 subtests (+0.0012 points)

Previous: `20261125T1507Z-wpt-linux-x86_64-gh45639976657a1`, core `66d81dd54`, 92.6378%. This run: core `da5649160`, 92.6390%; 5 commits between.
Tests that lost subtests: 1 (-1); that gained: 3 (+29). Page outcomes: OK +2, STALL -1, TIMEOUT -1.

**Directories that rose** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/dom | 72,463 | 69,902 | 69,928 | +26 |
| html/semantics | 22,498 | 15,588 | 15,589 | +1 |
| preload | 956 | 242 | 243 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 1 directories, the first 1)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| html/dom | 1 | 1 |

**Tests that lost most** (the first 1 of 1)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /html/dom/documents/resource-metadata-management/load-event-after-readystatechange-starts-load.html | 1 | 0 | 1 |

**Commits between** (5)

- `cbe377a49` Keep out-of-flow media wrappers from adding an empty line (#1037)
- `95939144c` Foafnaut: commit the Tor component probe (labs/demos/foafnaut/tor-probe)
- `9bcd55993` CLAUDE.md: the owner is the upstream route (owner, 2026-11-25)
- `e75f38792` Foafnaut Tor record: arti-client builds for wasm with no default features; survey of Tor-in-wasm work
- `da5649160` Flag missing photo bodies in offline page captures (#1048)

