### Since the previous full run: +39 subtests (+0.0017 points)

Previous: `20261114T2013Z-wpt-macos-arm64-gh43636351834a1`, core `3b456743b`, 91.8105%. This run: core `ff075ad5a`, 91.8122%; 7 commits between.
Tests that lost subtests: 181 (-689); that gained: 286 (+728). Page outcomes: CRASH -44, ERROR +24, NO_RESULT -321, OK +119, TIMEOUT +222.

**Directories that fell** (7; the first 7)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| streams | 5,796 | 5,580 | 5,160 | -420 |
| third_party/test262 | 53,833 | 43,375 | 43,245 | -130 |
| html/semantics | 22,381 | 15,168 | 15,154 | -14 |
| shadow-dom | 14,712 | 14,127 | 14,125 | -2 |
| webcodecs | 3,922 | 2,575 | 2,573 | -2 |
| svg/shapes | 18 | 1 | 0 | -1 |
| svg/types | 1,136 | 910 | 909 | -1 |

**Directories that rose** (10; the first 10)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| referrer-policy | 8,815 | 4,581 | 4,858 | +277 |
| mixed-content | 2,281 | 1,087 | 1,291 | +204 |
| fetch | 13,288 | 8,745 | 8,800 | +55 |
| service-workers | 3,262 | 1,361 | 1,392 | +31 |
| upgrade-insecure-requests | 982 | 196 | 218 | +22 |
| html/cross-origin-embedder-policy | 596 | 113 | 122 | +9 |
| workers | 1,598 | 697 | 703 | +6 |
| connection-allowlist | 365 | 83 | 85 | +2 |
| subresource-integrity | 491 | 184 | 186 | +2 |
| xhr | 2,344 | 1,814 | 1,815 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 14 directories, the first 14)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| streams | 218 | 1 |
| third_party/test262 | 141 | 141 |
| streams/piping | 111 | 3 |
| streams/readable-streams | 91 | 1 |
| referrer-policy/gen | 85 | 20 |
| html/semantics | 14 | 1 |
| referrer-policy/4K | 6 | 3 |
| referrer-policy/4K+1 | 6 | 3 |
| referrer-policy/4K-1 | 6 | 3 |
| fetch/content-type | 5 | 1 |
| shadow-dom | 2 | 1 |
| webcodecs | 2 | 1 |
| svg/shapes | 1 | 1 |
| svg/types | 1 | 1 |

**Tests that lost most** (the first 40 of 181)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /streams/idlharness.any.worker.html | 218 | 0 | 228 |
| /streams/readable-streams/templated.any.sharedworker.html | 91 | 0 | 91 |
| /streams/piping/pipe-through.any.worker.html | 42 | 0 | 43 |
| /streams/piping/error-propagation-backward.any.worker.html | 36 | 0 | 36 |
| /streams/piping/abort.any.worker.html | 33 | 0 | 33 |
| /html/semantics/embedded-content/the-img-element/relevant-mutations.html | 86 | 72 | 113 |
| /referrer-policy/gen/top.http-rp/same-origin/script-tag.http.html | 10 | 4 | 10 |
| /referrer-policy/gen/top.meta/always/fetch.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/top.meta/default/xhr.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/top.meta/origin/script-tag.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/top.meta/unset/fetch.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/worker-classic.http-rp/no-referrer-when-downgrade/fetch.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/worker-classic.http-rp/origin/fetch.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/worker-classic.http-rp/strict-origin/fetch.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/worker-module.http-rp/no-referrer-when-downgrade/fetch.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/worker-module.http-rp/origin/fetch.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/worker-module.http-rp/strict-origin/fetch.http.html | 12 | 6 | 12 |
| /fetch/content-type/script.window.html | 15 | 10 | 31 |
| /referrer-policy/gen/top.meta/default/a-tag.http.html | 3 | 0 | 4 |
| /referrer-policy/4K+1/gen/top.http-rp/strict-origin-when-cross-origin/xhr.http.html | 2 | 0 | 2 |
| /referrer-policy/4K+1/gen/top.meta/origin-when-cross-origin/xhr.http.html | 2 | 0 | 2 |
| /referrer-policy/4K+1/gen/top.meta/unset/xhr.http.html | 2 | 0 | 2 |
| /referrer-policy/4K-1/gen/top.http-rp/strict-origin-when-cross-origin/xhr.http.html | 2 | 0 | 2 |
| /referrer-policy/4K-1/gen/top.meta/origin-when-cross-origin/xhr.http.html | 2 | 0 | 2 |
| /referrer-policy/4K-1/gen/top.meta/unset/xhr.http.html | 2 | 0 | 2 |
| /referrer-policy/4K/gen/top.http-rp/strict-origin-when-cross-origin/xhr.http.html | 2 | 0 | 2 |
| /referrer-policy/4K/gen/top.meta/origin-when-cross-origin/xhr.http.html | 2 | 0 | 2 |
| /referrer-policy/4K/gen/top.meta/unset/xhr.http.html | 2 | 0 | 2 |
| /referrer-policy/gen/req.attr/no-referrer/a-tag.http.html | 2 | 0 | 4 |
| /referrer-policy/gen/req.attr/origin-when-cross-origin/script-tag.http.html | 2 | 0 | 12 |
| /referrer-policy/gen/req.attr/strict-origin/iframe-tag.http.html | 2 | 0 | 12 |
| /referrer-policy/gen/req.attr/unsafe-url/svg-a-tag.http.html | 2 | 0 | 4 |
| /referrer-policy/gen/top.http-rp/no-referrer/svg-a-tag.http.html | 2 | 0 | 4 |
| /referrer-policy/gen/top.http-rp/unset/iframe-tag.http.html | 2 | 0 | 12 |
| /referrer-policy/gen/top.meta/no-referrer/svg-a-tag.http.html | 2 | 0 | 4 |
| /referrer-policy/gen/top.meta/unsafe-url/iframe-tag.http.html | 2 | 0 | 12 |
| /shadow-dom/slots-fallback-in-document.html | 2 | 0 | 2 |
| /webcodecs/image-decoder.https.any.html | 16 | 14 | 47 |
| /svg/shapes/line-pathLength.svg | 1 | 0 | 1 |
| /svg/types/scripted/SVGLength-zoom.html | 1 | 0 | 1 |

**Commits between** (7)

- `144c45efe` WPT runner: script fetches and frames are answered until neither asks (at most 64 rounds), so a page never waits on a request nobody answers
- `94ba8ed8c` Fetch: whether a response's body is null is decided in Lean (PageFetch.nullBody: a null body status or a HEAD request; web_api 67 read 10), 
- `b64821988` WebSocket: the close code kept (1000 for a reason with no code) is Lean's (Net.WebSocket.closeCode, web_api 163 answers it), for close() and
- `eb25a375c` Network theorems: a request without credentials "include" that crossed origins sends no cookie on any later hop of its redirect chain, nor a
- `4677badc3` Classic script elements: an answer of a type the element may not run is a network error (Fetch §4.1 MIME type and nosniff checks, Subresourc
- `cbc27ce78` WPT runner: the page's bound on script fetches answered is 1024, not 4096: at about 57 ms a fetch on the Linux checks, a page that asks for 
- `ff075ad5a` @factoidal/core 0.37.0: version and changelog

