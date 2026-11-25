### Since the previous full run: +123 subtests (+0.0054 points)

Previous: `20261125T1359Z-wpt-linux-x86_64-gh45627967031a1`, core `100307076`, 92.6323%. This run: core `66d81dd54`, 92.6378%; 27 commits between.
Tests that lost subtests: 1 (-1); that gained: 60 (+124). Page outcomes: CRASH +1, STALL -1.

**Directories that fell** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/css-borders | 4,906 | 4,375 | 4,374 | -1 |

**Directories that rose** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| sanitizer-api | 3,839 | 2,576 | 2,639 | +63 |
| third_party/test262 | 53,838 | 46,287 | 46,344 | +57 |
| webcodecs | 4,168 | 2,638 | 2,641 | +3 |
| html/semantics | 22,498 | 15,587 | 15,588 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 1 directories, the first 1)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| css/css-borders | 1 | 1 |

**Tests that lost most** (the first 1 of 1)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /css/css-borders/border-image-slice-shorthand-reset.html | 1 | 0 | 1 |

**Commits between** (27)

- `c90174122` Foafnaut: pointer events carry modifiers, click count and button; Command-click and middle click open a tab (issue 1031)
- `43a60bfda` Foafnaut: gesture lane in the engine worker; copy and gesture frames do not wait for script turns (issue 1031)
- `fff3b316d` native_net: connection pool keyed by origin, partition and pinned address (issue 1031)
- `d7fc27f07` native_net: DNS cache per (partition, host), shared in-flight lookups, bounded prefetch function (issue 1031)
- `30f534768` Apply ArraySetLength to descriptor-backed arrays (#1005)
- `91d459bda` Merge branch 'wip/1031-dns-cache' of https://github.com/danbri/factoidal-core
- `28d6068bf` native_net_dns_test: run without env permission (the real lookup stays opt-in)
- `8f18fecfb` test.sh: run the connection pool and DNS cache tests with network permission, not among the pure tests
- `ddccfe22e` tools/foafnaut-linux-rig: run the desktop browser from source in a Linux cloud session (Xvfb, software Vulkan, released engine) to measure h
- `691df9021` test.sh: allow the DNS_REAL variable for the opt-in real DNS lookup test
- `ba25c10b2` Use the startup page origin for synchronous fetch partitioning (#1036)
- `31ed3c077` Foafnaut: context menu for a page link and for the page, decided in Lean (issue 1031)
- `f7dd9e654` Foafnaut: double click selects a word, triple click a line, decided in Lean (issue 1031)
- `5afb93c63` Foafnaut: --gesture-sweep for desktop gestures (issue 1031)
- `42560cdf2` Merge remote-tracking branch 'origin/main' into wip/1031-input-lane
- `c08629779` Foafnaut: parse and draw CSS border-image (CSS Backgrounds 3 section 6), issue 874 part 2
- `14cc290da` border-image: longhands in the cascade (source order), border shorthand resets them; cascade guards; WebDocument border-image test
- `845bf181d` border-image: each part samples its own slice, so seams do not mix in the next slice (issue 874)
- `e9ae7ee0b` Draw queries beyond set browsing as Scratch-like blocks
- `a29700ff2` Place outside list markers at the border edge (#1032)
- `c42e9a66c` Measure cold compositor pipeline and resource waits (#1033)
- `22fdd694d` Draw every Wikidata query as blocks, with plainer wording and highlighting
- `5e7e446d2` Merge branch 'wip/1031-input-lane' of https://github.com/danbri/factoidal-core
- `96324ab32` Record the measured raw Foafnaut Wasm size after interop fixes (#1046)
- `dd39844ec` Foafnaut: record what Tor and onion services need from the network design
- `1ba7cc421` Foafnaut Tor record: measured Arti components in a Foafnaut page
- `66d81dd54` CLAUDE.md: never report upstream (owner, 2026-11-25)

