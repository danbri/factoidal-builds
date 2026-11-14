### Since the previous full run: +11,408 subtests (+0.5025 points)

Previous: `20261114T1415Z-wpt-linux-x86_64-gh43602343945a1`, core `b323da1b0`, 91.0088%. This run: core `64af7ef92`, 91.5114%; 47 commits between.
Tests that lost subtests: 120 (-643); that gained: 1,060 (+12,051). Page outcomes: CRASH -24, ERROR -45, NO_RESULT +79, OK -18, STALL +1, TIMEOUT +7.

**Directories that fell** (10; the first 10)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| quirks | 6,984 | 6,884 | 6,623 | -261 |
| upgrade-insecure-requests | 982 | 220 | 196 | -24 |
| html/infrastructure | 1,664 | 789 | 775 | -14 |
| svg/geometry | 609 | 407 | 397 | -10 |
| connection-allowlist | 365 | 89 | 83 | -6 |
| resource-timing | 1,207 | 24 | 19 | -5 |
| html/editing | 868 | 514 | 510 | -4 |
| trusted-types | 3,754 | 2,715 | 2,712 | -3 |
| mimesniff | 3,886 | 2,624 | 2,623 | -1 |
| web-animations | 4,256 | 3,705 | 3,704 | -1 |

**Directories that rose** (76; the first 40)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| dom/ranges | 44,720 | 40,356 | 44,051 | +3,695 |
| fetch | 13,288 | 7,443 | 8,758 | +1,315 |
| referrer-policy | 8,815 | 3,583 | 4,581 | +998 |
| urlpattern | 3,266 | 2,265 | 3,014 | +749 |
| content-security-policy | 4,544 | 1,905 | 2,501 | +596 |
| service-workers | 3,262 | 957 | 1,361 | +404 |
| url | 12,437 | 11,380 | 11,768 | +388 |
| html/semantics | 22,381 | 14,687 | 15,031 | +344 |
| html/dom | 72,399 | 69,270 | 69,540 | +270 |
| html/canvas | 6,251 | 3,443 | 3,675 | +232 |
| streams | 5,796 | 5,362 | 5,580 | +218 |
| css/mediaqueries | 1,786 | 985 | 1,195 | +210 |
| dom/(root) | 2,768 | 2,230 | 2,440 | +210 |
| cookiestore | 636 | 303 | 503 | +200 |
| IndexedDB | 5,853 | 5,202 | 5,397 | +195 |
| css/selectors | 6,266 | 5,521 | 5,707 | +186 |
| html/rendering | 11,705 | 8,123 | 8,306 | +183 |
| css/filter-effects | 3,007 | 2,660 | 2,838 | +178 |
| websockets | 2,389 | 1,110 | 1,229 | +119 |
| svg/(root) | 1,754 | 1,212 | 1,311 | +99 |
| domparsing | 3,731 | 2,369 | 2,435 | +66 |
| workers | 1,598 | 632 | 697 | +65 |
| mathml | 4,321 | 1,024 | 1,088 | +64 |
| beacon | 102 | 29 | 87 | +58 |
| html/webappapis | 3,665 | 2,914 | 2,969 | +55 |
| mixed-content | 2,281 | 1,034 | 1,087 | +53 |
| web-locks | 517 | 400 | 449 | +49 |
| storage | 482 | 401 | 449 | +48 |
| encoding/(root) | 23,822 | 23,420 | 23,467 | +47 |
| css/geometry | 1,575 | 517 | 561 | +44 |
| html/browsers | 3,309 | 723 | 766 | +43 |
| fs | 1,121 | 955 | 994 | +39 |
| push-api | 290 | 39 | 71 | +32 |
| css/css-grid | 16,015 | 9,084 | 9,115 | +31 |
| infrastructure | 286 | 82 | 109 | +27 |
| page-visibility | 41 | 4 | 27 | +23 |
| user-timing | 862 | 426 | 446 | +20 |
| web-based-payment-handler | 145 | 30 | 50 | +20 |
| gpc | 77 | 51 | 68 | +17 |
| content-index | 105 | 17 | 31 | +14 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 24 directories, the first 24)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| quirks/unitless-length | 205 | 3 |
| mixed-content/gen | 196 | 51 |
| quirks/hashless-hex-color | 56 | 1 |
| upgrade-insecure-requests/gen | 43 | 10 |
| content-security-policy/gen | 32 | 16 |
| fetch/corb | 29 | 3 |
| html/infrastructure | 15 | 5 |
| svg/geometry | 10 | 1 |
| html/semantics | 7 | 4 |
| service-workers/service-worker | 7 | 1 |
| connection-allowlist/tentative | 6 | 3 |
| domparsing | 6 | 1 |
| html/webappapis | 6 | 3 |
| resource-timing | 5 | 1 |
| fetch/api | 4 | 4 |
| html/editing | 4 | 2 |
| html/browsers | 3 | 2 |
| trusted-types | 3 | 3 |
| content-security-policy/parsing | 1 | 1 |
| fetch/range | 1 | 1 |
| html/dom | 1 | 1 |
| mimesniff/sniffing | 1 | 1 |
| performance-timeline | 1 | 1 |
| web-animations/timing-model | 1 | 1 |

**Tests that lost most** (the first 40 of 120)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /quirks/unitless-length/quirks.html | 1,590 | 1,407 | 1,590 |
| /quirks/hashless-hex-color/quirks.html | 692 | 636 | 692 |
| /fetch/corb/script-resource-with-json-parser-breaker.tentative.sub.html | 27 | 0 | 27 |
| /quirks/unitless-length/limited-quirks.html | 1,581 | 1,570 | 1,581 |
| /quirks/unitless-length/no-quirks.html | 1,581 | 1,570 | 1,581 |
| /svg/geometry/svg-geometry-apis-in-non-rendered-elements.html | 27 | 17 | 36 |
| /service-workers/service-worker/fetch-event.https.html | 9 | 2 | 43 |
| /domparsing/parsed-document-origin.window.html | 7 | 1 | 7 |
| /mixed-content/gen/iframe-inherit.http-rp/opt-in/sharedworker-import-data.https.html | 6 | 0 | 8 |
| /mixed-content/gen/iframe-inherit.http-rp/opt-in/sharedworker-import.https.html | 6 | 0 | 8 |
| /mixed-content/gen/iframe-inherit.http-rp/opt-in/worker-import-data.https.html | 6 | 0 | 8 |
| /mixed-content/gen/iframe-inherit.http-rp/opt-in/worker-import.https.html | 6 | 0 | 8 |
| /mixed-content/gen/iframe-inherit.meta/unset/sharedworker-import-data.https.html | 6 | 0 | 8 |
| /mixed-content/gen/iframe-inherit.meta/unset/sharedworker-import.https.html | 6 | 0 | 8 |
| /mixed-content/gen/iframe-inherit.meta/unset/worker-import-data.https.html | 6 | 0 | 8 |
| /mixed-content/gen/iframe-inherit.meta/unset/worker-import.https.html | 6 | 0 | 8 |
| /mixed-content/gen/sharedworker-module-data.http-rp/opt-in/fetch.https.html | 6 | 0 | 8 |
| /mixed-content/gen/sharedworker-module-data.http-rp/opt-in/xhr.https.html | 6 | 0 | 8 |
| /mixed-content/gen/sharedworker-module-data.meta/unset/fetch.https.html | 6 | 0 | 8 |
| /mixed-content/gen/sharedworker-module-data.meta/unset/xhr.https.html | 6 | 0 | 8 |
| /mixed-content/gen/srcdoc-inherit.http-rp/opt-in/sharedworker-import-data.https.html | 6 | 0 | 8 |
| /mixed-content/gen/srcdoc-inherit.http-rp/opt-in/sharedworker-import.https.html | 6 | 0 | 8 |
| /mixed-content/gen/srcdoc-inherit.http-rp/opt-in/worker-import-data.https.html | 6 | 0 | 8 |
| /mixed-content/gen/srcdoc-inherit.http-rp/opt-in/worker-import.https.html | 6 | 0 | 8 |
| /mixed-content/gen/srcdoc-inherit.meta/unset/sharedworker-import-data.https.html | 6 | 0 | 8 |
| /mixed-content/gen/srcdoc-inherit.meta/unset/sharedworker-import.https.html | 6 | 0 | 8 |
| /mixed-content/gen/srcdoc-inherit.meta/unset/worker-import-data.https.html | 6 | 0 | 8 |
| /mixed-content/gen/srcdoc-inherit.meta/unset/worker-import.https.html | 6 | 0 | 8 |
| /upgrade-insecure-requests/gen/srcdoc-inherit.meta/unset/sharedworker-import-data.https.html | 6 | 0 | 6 |
| /upgrade-insecure-requests/gen/srcdoc-inherit.meta/unset/sharedworker-import.https.html | 6 | 0 | 6 |
| /upgrade-insecure-requests/gen/srcdoc-inherit.meta/unset/worker-import-data.https.html | 6 | 0 | 6 |
| /upgrade-insecure-requests/gen/srcdoc-inherit.meta/unset/worker-import.https.html | 6 | 0 | 6 |
| /upgrade-insecure-requests/gen/top.meta/unset/sharedworker-import.https.html | 6 | 0 | 6 |
| /resource-timing/idlharness.any.worker.html | 5 | 0 | 79 |
| /upgrade-insecure-requests/gen/sharedworker-module-data.meta/unset/fetch.https.html | 6 | 1 | 6 |
| /upgrade-insecure-requests/gen/sharedworker-module-data.meta/unset/xhr.https.html | 6 | 1 | 6 |
| /connection-allowlist/tentative/websocket-shared-worker.https.sub.window.html | 4 | 0 | 5 |
| /html/semantics/embedded-content/the-img-element/update-the-image-data/src-then-lazy-load.html | 8 | 4 | 8 |
| /mixed-content/gen/iframe-inherit.meta/opt-in/sharedworker-import-data.https.html | 4 | 0 | 5 |
| /mixed-content/gen/iframe-inherit.meta/opt-in/sharedworker-import.https.html | 4 | 0 | 5 |

**Commits between** (47)

- `176db71d2` demo pages: webgpu-force-graph.html in the manifest and in the index's script group (the index is generated; build-demo-pages.py --check fai
- `37ca051f6` WPT runner: answer the script fetches a page asks for after a page request was answered
- `e7b33a69a` Referrer source: the page document's current URL (as its history has it) names the referrer
- `733b891bd` prelude: a service worker's fetch keeps the XMLHttpRequest class its scope hides
- `4549afb6b` WebSocketStream and WebSocketError over the same connections; close() with a reason and no code sends 1000
- `97fd4e24e` fetch: ReadableStream bodies for Response and Request (duplex half)
- `dbd25330f` prelude: Location's href setter and window.open throw SyntaxError for a URL that does not parse
- `99f45cbdd` Time goes on while a worker holds an open WebSocket; the runner's test-driver slices stop when the page waits for the network
- `0230f2a54` formData(): multipart/form-data bodies read in Lean (Net.Multipart, web_api 164)
- `9256a39b5` SVG DOM: attribute getters are named 'get <attribute>' (WebIDL 3.7.6)
- `1dd9df06f` docs: net third-phase record: WebSocketStream, multipart formData, stream bodies, runner fixes
- `1c0fada29` navigator.sendBeacon: a POST with credentials through the page's fetch (no-cors for a CORS-safelisted body type, else cors); TypeError for a
- `668229036` Net.PageFetch: a redirect to a URL with credentials is refused once a cors request has left the page's origin (Fetch 4.4 step 7)
- `361353294` Net.Xhr: a session keeps the address it chose for each name; a later request to that name starts pinned (one resolve per name, not per reque
- `c5df0d602` Module workers: new Worker(url, {type: 'module'}) and module SharedWorkers run their module graph
- `821b76209` Workers: a worker's own script that a redirect took to another origin is a network error; fetch: null body for null body statuses and HEAD
- `4f1e45fcf` Images and inserted scripts make element requests: destination, CORS settings, raw answers; img load/error, naturalWidth/Height, complete, d
- `4773dadcf` docs: net third-phase record: element requests, module workers, DNS pins, open items
- `3ba90ac5a` Images: the window's load event waits for the images of the page's start (HTML 4.8.4.3, the load event delayed until each has its load or er
- `335dd56c6` Images: a page's own images beyond the first 16 are requested when a script reads their state, not up front (a host that draws the page fetc
- `f365c76fe` Cache.put leaves the response's body stream locked, as reading it through a reader does
- `e2625154c` Cookie Store: the maxAge option (with expires as well: TypeError); a change of a cookie's attributes alone is a change event
- `2f46f19a0` Cookie Store: the document's creation URL, not its current URL after history.pushState
- `b367e05cd` docs: client storage record: measured after the 873955244 merge, and what is open
- `83c04db95` Storage Buckets: a bucket's caches and locks are its own (storage key gains the bucket; Lean Buckets.route, theorem route_origin; web_api 20
- `4549431ba` Grid: self-start and self-end follow the item's own writing mode and direction (CSS Box Alignment 3 §4.1), read from its LogicalAxes frame
- `a677fb995` Grid track sizing: shared-out space never exceeds the space (distribute_sum_le), and with no growth limits it is all handed out (distribute_
- `a83556fa7` Design record: grid's writing modes, overflow alignment, resource bounds and the new sizing theorems
- `31ad9e149` measure op 17 of a node with no box answers zeros again (WebDriver's in-view centre reads them) with a twelfth number -1 that tells getClien
- `00f67b9d2` Interface objects made on first use (the canvas 2D interfaces) get the Web IDL shape when first read; HTMLInputElement width and height refl
- `3320e1717` Script elements: a parser-inserted script with no src and no child text runs when text is added later (prepare bails before already-started)
- `c373e1ace` Presentational hints: percentage heights from attributes too (the layout now resolves a percentage height against a definite containing heig
- `31b15acd0` getComputedStyle of an element in a frame's document: a cascade of that document from its root (UA sheet and its own style elements); its bo
- `a531477d4` Presentational hints above the UA sheet: a property a hint sets (width, height, margins) takes no value from a UA rule (CSS.hintedProperties
- `a7cc7964f` Popovers: the popover attribute change steps (a showing popover whose state changes or whose attribute goes hides with events, once: a hide 
- `d8b0a53e7` A frame that a script inserts with no URL to load runs its iframe load event steps at once (HTML 4.8.5 process the iframe attributes, initia
- `34c35514a` Document: hidden, visibilityState, referrer, lastModified, domain (setting another domain is refused), onreadystatechange and onvisibilitych
- `b78efb0c3` autocomplete of input, select and textarea: the IDL-exposed autofill value (HTML.Autofill: the autofill processing model's field table, cate
- `55996332f` A body or frameset in a document with no browsing context has no window: its window-reflecting event handlers are null and setting them does
- `98a49318d` Window: its operations are enumerable own properties; print(); the BarProp bars, status, closed, length (child frames), originAgentCluster a
- `93de0569a` Document operations and the dir and designMode accessors throw TypeError on an object that is not a Document; getElementsByName needs its ar
- `983705742` docs: dom-html design record, step 14
- `e24beaf4a` Style: one hintedProperties after the rebase over main's copy
- `37ac40c4c` Trusted mousedown, mouseup and click stop below a disabled form control in the event path (the listeners of the control and above it do not 
- `a6d4e0ef1` getComputedStyle of a margin, padding or size: a normal UA declaration is left to the layout profile, which has it below the presentational 
- `9d9c4b3a1` Margins collapse through an empty block (CSS 2.1 §8.3.1)
- `64af7ef92` docs: layout record, margins through an empty block

