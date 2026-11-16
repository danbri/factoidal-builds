### Since the previous full run: +187 subtests (+0.0082 points)

Previous: `20261116T1246Z-wpt-macos-arm64-gh43869544981a1`, core `6e2d79003`, 91.9586%. This run: core `ddf6be714`, 91.9668%; 13 commits between.
Tests that lost subtests: 74 (-262); that gained: 9 (+449). Page outcomes: NO_RESULT +10, OK -2, STALL -1, TIMEOUT -7.

**Directories that fell** (8; the first 8)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| referrer-policy | 8,815 | 5,029 | 4,856 | -173 |
| intersection-observer | 440 | 212 | 161 | -51 |
| html/semantics | 22,381 | 15,189 | 15,176 | -13 |
| subresource-integrity | 491 | 197 | 184 | -13 |
| page-visibility | 41 | 27 | 23 | -4 |
| websockets | 2,389 | 1,260 | 1,256 | -4 |
| shadow-dom | 14,720 | 14,129 | 14,127 | -2 |
| webcodecs | 3,922 | 2,576 | 2,574 | -2 |

**Directories that rose** (5; the first 5)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| streams | 5,796 | 5,283 | 5,580 | +297 |
| webidl | 838 | 500 | 647 | +147 |
| webmessaging | 304 | 150 | 153 | +3 |
| third_party/test262 | 53,833 | 45,717 | 45,718 | +1 |
| xhr | 2,344 | 1,816 | 1,817 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 12 directories, the first 12)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| referrer-policy/gen | 107 | 40 |
| intersection-observer | 51 | 2 |
| referrer-policy/4K+1 | 24 | 9 |
| referrer-policy/4K | 22 | 8 |
| referrer-policy/4K-1 | 20 | 6 |
| html/semantics | 13 | 3 |
| subresource-integrity/unencoded-digest | 13 | 1 |
| page-visibility | 4 | 1 |
| websockets/stream | 4 | 1 |
| webcodecs | 2 | 1 |
| shadow-dom/focus | 1 | 1 |
| shadow-dom/untriaged | 1 | 1 |

**Tests that lost most** (the first 40 of 74)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /intersection-observer/idlharness.window.html | 50 | 0 | 50 |
| /subresource-integrity/unencoded-digest/tentative/script.window.html?include=integrity-fail | 13 | 0 | 14 |
| /html/semantics/embedded-content/the-img-element/relevant-mutations.html | 89 | 80 | 113 |
| /referrer-policy/4K+1/gen/top.http-rp/no-referrer-when-downgrade/script-tag.http.html | 12 | 6 | 12 |
| /referrer-policy/4K+1/gen/top.http-rp/unsafe-url/script-tag.http.html | 12 | 6 | 12 |
| /referrer-policy/4K-1/gen/top.http-rp/no-referrer-when-downgrade/script-tag.http.html | 12 | 6 | 12 |
| /referrer-policy/4K-1/gen/top.http-rp/unsafe-url/script-tag.http.html | 12 | 6 | 12 |
| /referrer-policy/4K/gen/top.http-rp/no-referrer-when-downgrade/script-tag.http.html | 12 | 6 | 12 |
| /referrer-policy/4K/gen/top.http-rp/unsafe-url/script-tag.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/top.http-rp/origin-when-cross-origin/fetch.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/top.http-rp/origin/xhr.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/top.meta/always/script-tag.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/top.meta/origin-when-cross-origin/fetch.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/top.meta/origin-when-crossorigin/xhr.http.html | 12 | 6 | 12 |
| /referrer-policy/gen/top.meta/unset/script-tag.http.html | 12 | 6 | 12 |
| /page-visibility/test_attributes_exist.html | 4 | 0 | 4 |
| /websockets/stream/tentative/abort.any.worker.html?wss | 4 | 0 | 5 |
| /html/semantics/scripting-1/the-script-element/module/import-meta/import-meta-url.any.sharedworker-module.html | 3 | 0 | 3 |
| /referrer-policy/gen/top.meta/default/xhr.http.html | 12 | 9 | 12 |
| /referrer-policy/gen/top.meta/origin-when-crossorigin/a-tag.http.html | 3 | 0 | 4 |
| /referrer-policy/gen/top.meta/strict-origin-when-cross-origin/svg-a-tag.http.html | 3 | 0 | 4 |
| /referrer-policy/4K+1/gen/top.http-rp/origin-when-cross-origin/worker-module.http.html | 2 | 0 | 2 |
| /referrer-policy/4K+1/gen/top.http-rp/strict-origin-when-cross-origin/fetch.http.html | 2 | 0 | 2 |
| /referrer-policy/4K+1/gen/top.meta/origin-when-cross-origin/fetch.http.html | 2 | 0 | 2 |
| /referrer-policy/4K+1/gen/top.meta/same-origin/script-tag.http.html | 2 | 0 | 2 |
| /referrer-policy/4K+1/gen/top.meta/unset/fetch.http.html | 2 | 0 | 2 |
| /referrer-policy/4K-1/gen/top.http-rp/strict-origin-when-cross-origin/fetch.http.html | 2 | 0 | 2 |
| /referrer-policy/4K-1/gen/top.meta/origin-when-cross-origin/fetch.http.html | 2 | 0 | 2 |
| /referrer-policy/4K-1/gen/top.meta/same-origin/script-tag.http.html | 2 | 0 | 2 |
| /referrer-policy/4K-1/gen/top.meta/unset/fetch.http.html | 2 | 0 | 2 |
| /referrer-policy/4K/gen/top.http-rp/strict-origin-when-cross-origin/fetch.http.html | 2 | 0 | 2 |
| /referrer-policy/4K/gen/top.meta/origin-when-cross-origin/fetch.http.html | 2 | 0 | 2 |
| /referrer-policy/4K/gen/top.meta/same-origin/script-tag.http.html | 2 | 0 | 2 |
| /referrer-policy/4K/gen/top.meta/unset/fetch.http.html | 2 | 0 | 2 |
| /referrer-policy/gen/req.attr/no-referrer-when-downgrade/a-tag.http.html | 2 | 0 | 4 |
| /referrer-policy/gen/req.attr/strict-origin-when-cross-origin/iframe-tag.http.html | 2 | 0 | 12 |
| /referrer-policy/gen/req.attr/strict-origin/iframe-tag.http.html | 2 | 0 | 12 |
| /referrer-policy/gen/req.attr/strict-origin/svg-a-tag.http.html | 2 | 0 | 4 |
| /referrer-policy/gen/srcdoc-inherit.http-rp/no-referrer/worker-module.http.html | 2 | 0 | 2 |
| /referrer-policy/gen/srcdoc-inherit.http-rp/origin-when-cross-origin/worker-module.http.html | 2 | 0 | 2 |

**Commits between** (13)

- `0391fe0d0` realpages: add nature-telemetry, infobomb, w3c-maxf to the survey (#528)
- `cdb310373` Hub: Web platform lists Textnaut, start, demos, stress, settings, notebook, conformance; Hub copies of openly licensed pages open in place i
- `17c7b1bc9` Test results: an index page for the site toolbar's Test Results link (it answered 404)
- `19eac6182` Settings in every UI: Textnaut's s key opens a settings screen (engine build, page scripts, strictness); the Hub passes the system's dark mo
- `dae92ae22` Hub README: Hub copies, how they are made, served and added
- `3cc24f393` Chrome: a flat look by default (light and dark faces, rounded address field with a focus ring, vector line icons, settings button in a circl
- `14ba800e3` Web platform page: link the data and documents conformance page
- `86b7fea8f` Chrome: line icons 20 points and a little heavier (readable at 1x); copy licence line spacing
- `cce8aea38` Chrome: circles as 16-sided polygons, square caps and mitred joins (no curve to flatten; the flat look cost 1.5 to 3 times the classic chrom
- `6cfb23d66` Chrome: the gear is one filled shape with the hub as a hole; each icon's lines are one stroked path (at most two primitives an icon)
- `aa42acc12` Chrome: icon lines are filled quadrilaterals in one path (nonzero), not strokes
- `336905e13` Start page: a Books, texts and essays group and a Small tools group, 32 more plain sites (probed with Textnaut 0.1.4 native), 10 more Hub co
- `ddf6be714` scroll_layers_check: chrome rows apart; a sloped or round chrome edge sampled by the other rule (issue 1269) is counted as that expected fai

