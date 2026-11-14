### Since the previous full run: +776 subtests (+0.0342 points)

Previous: `20261114T1913Z-wpt-linux-x86_64-gh43628354844a1`, core `3b456743b`, 91.8106%. This run: core `ff075ad5a`, 91.8448%; 7 commits between.
Tests that lost subtests: 2 (-6); that gained: 307 (+782). Page outcomes: CRASH -44, ERROR +19, NO_RESULT -323, OK +217, TIMEOUT +131.

**Directories that fell** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| preload | 956 | 47 | 46 | -1 |

**Directories that rose** (8; the first 8)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| referrer-policy | 8,815 | 4,581 | 5,029 | +448 |
| mixed-content | 2,281 | 1,087 | 1,291 | +204 |
| fetch | 13,288 | 8,758 | 8,813 | +55 |
| service-workers | 3,262 | 1,361 | 1,392 | +31 |
| upgrade-insecure-requests | 982 | 196 | 218 | +22 |
| html/cross-origin-embedder-policy | 596 | 113 | 122 | +9 |
| workers | 1,598 | 697 | 703 | +6 |
| connection-allowlist | 365 | 83 | 85 | +2 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| fetch/content-type | 5 | 1 |
| preload | 1 | 1 |

**Tests that lost most** (the first 2 of 2)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /fetch/content-type/script.window.html | 15 | 10 | 31 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |

**Commits between** (7)

- `144c45efe` WPT runner: script fetches and frames are answered until neither asks (at most 64 rounds), so a page never waits on a request nobody answers
- `94ba8ed8c` Fetch: whether a response's body is null is decided in Lean (PageFetch.nullBody: a null body status or a HEAD request; web_api 67 read 10), 
- `b64821988` WebSocket: the close code kept (1000 for a reason with no code) is Lean's (Net.WebSocket.closeCode, web_api 163 answers it), for close() and
- `eb25a375c` Network theorems: a request without credentials "include" that crossed origins sends no cookie on any later hop of its redirect chain, nor a
- `4677badc3` Classic script elements: an answer of a type the element may not run is a network error (Fetch §4.1 MIME type and nosniff checks, Subresourc
- `cbc27ce78` WPT runner: the page's bound on script fetches answered is 1024, not 4096: at about 57 ms a fetch on the Linux checks, a page that asks for 
- `ff075ad5a` @factoidal/core 0.37.0: version and changelog

