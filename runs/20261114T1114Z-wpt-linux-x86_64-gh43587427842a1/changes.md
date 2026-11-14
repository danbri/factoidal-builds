### Since the previous full run: +11,270 subtests (+0.4966 points)

Previous: `20261114T1029Z-wpt-linux-x86_64-gh43585273487a1`, core `69c1357ad`, 86.9035%. This run: core `a9e7eaef2`, 87.4001%; 67 commits between.
Tests that lost subtests: 184 (-793); that gained: 1,408 (+12,063). Page outcomes: CRASH +13, ERROR +42, NO_RESULT +114, OK +562, SKIP engine -723, SKIP other +3, STALL +1, TIMEOUT -12.

**Directories that fell** (7; the first 7)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| referrer-policy | 8,815 | 3,772 | 3,391 | -381 |
| mixed-content | 2,281 | 1,133 | 1,052 | -81 |
| css/css-logical | 1,366 | 1,020 | 980 | -40 |
| upgrade-insecure-requests | 982 | 236 | 220 | -16 |
| html/cross-origin-embedder-policy | 596 | 100 | 97 | -3 |
| css/css-inline | 869 | 509 | 507 | -2 |
| css/css-viewport | 784 | 485 | 484 | -1 |

**Directories that rose** (92; the first 40)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| IndexedDB | 5,853 | 1,792 | 3,958 | +2,166 |
| fetch | 13,288 | 4,615 | 6,674 | +2,059 |
| streams | 5,796 | 2,796 | 4,186 | +1,390 |
| urlpattern | 3,266 | 1,510 | 2,262 | +752 |
| service-workers | 3,262 | 87 | 601 | +514 |
| webcodecs | 3,922 | 2,130 | 2,582 | +452 |
| css/css-cascade | 1,759 | 962 | 1,312 | +350 |
| html/canvas | 6,235 | 3,094 | 3,439 | +345 |
| css/selectors | 6,266 | 5,145 | 5,429 | +284 |
| css/css-gaps | 4,157 | 1,739 | 1,990 | +251 |
| css/css-color | 12,752 | 11,492 | 11,733 | +241 |
| wasm/webapi | 1,066 | 536 | 775 | +239 |
| compression | 1,316 | 490 | 717 | +227 |
| css/css-properties-values-api | 1,394 | 519 | 742 | +223 |
| dom/(root) | 2,759 | 2,017 | 2,224 | +207 |
| workers | 1,598 | 389 | 579 | +190 |
| xhr | 2,344 | 1,683 | 1,818 | +135 |
| css/css-shapes | 7,527 | 5,565 | 5,695 | +130 |
| html/semantics | 22,364 | 13,604 | 13,730 | +126 |
| encoding/(root) | 23,822 | 23,227 | 23,347 | +120 |
| encoding/streams | 472 | 216 | 322 | +106 |
| web-locks | 517 | 207 | 312 | +105 |
| content-security-policy | 4,544 | 1,774 | 1,870 | +96 |
| storage | 482 | 253 | 349 | +96 |
| css/css-images | 3,601 | 3,105 | 3,193 | +88 |
| html/infrastructure | 1,664 | 604 | 679 | +75 |
| css/css-values | 10,422 | 4,197 | 4,269 | +72 |
| css/cssom | 4,463 | 2,926 | 2,998 | +72 |
| fs | 1,121 | 84 | 153 | +69 |
| subresource-integrity | 491 | 128 | 182 | +54 |
| third_party/test262 | 53,833 | 36,711 | 36,765 | +54 |
| css/css-overflow | 1,209 | 505 | 540 | +35 |
| cookiestore | 636 | 202 | 236 | +34 |
| css/css-syntax | 444 | 168 | 200 | +32 |
| html/webappapis | 3,665 | 2,593 | 2,620 | +27 |
| css/css-box | 982 | 389 | 415 | +26 |
| css/css-will-change | 173 | 144 | 170 | +26 |
| user-timing | 862 | 406 | 426 | +20 |
| css/mediaqueries | 1,786 | 967 | 985 | +18 |
| permissions | 212 | 78 | 96 | +18 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 33 directories, the first 33)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| referrer-policy/gen | 304 | 51 |
| referrer-policy/4K+1 | 192 | 36 |
| mixed-content/gen | 81 | 24 |
| css/css-properties-values-api | 48 | 1 |
| css/css-logical | 41 | 1 |
| content-security-policy/gen | 32 | 16 |
| upgrade-insecure-requests/gen | 16 | 5 |
| compat | 12 | 1 |
| css/css-values | 9 | 9 |
| content-security-policy/script-src | 7 | 5 |
| fetch/orb | 7 | 5 |
| content-security-policy/securitypolicyviolation | 6 | 1 |
| html/cross-origin-embedder-policy | 5 | 3 |
| css/css-box | 4 | 2 |
| css/css-inline | 4 | 4 |
| css/cssom | 4 | 2 |
| css/css-cascade | 2 | 1 |
| css/css-ui | 2 | 2 |
| subresource-integrity/signatures | 2 | 1 |
| workers | 2 | 1 |
| connection-allowlist/tentative | 1 | 1 |
| content-security-policy/blob | 1 | 1 |
| content-security-policy/default-src | 1 | 1 |
| content-security-policy/inheritance | 1 | 1 |
| content-security-policy/reporting | 1 | 1 |
| css/css-anchor-position | 1 | 1 |
| css/css-shadow | 1 | 1 |
| css/css-variables | 1 | 1 |
| css/css-viewport | 1 | 1 |
| fetch/corb | 1 | 1 |
| fetch/cross-origin-resource-policy | 1 | 1 |
| fetch/metadata | 1 | 1 |
| referrer-policy/generic | 1 | 1 |

**Tests that lost most** (the first 40 of 184)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /css/css-properties-values-api/typedom.html | 168 | 120 | 325 |
| /css/css-logical/logical-box-padding.html | 44 | 3 | 44 |
| /compat/webkit-box-item-shrink-001.html | 14 | 2 | 20 |
| /referrer-policy/4K+1/gen/top.http-rp/no-referrer-when-downgrade/fetch.http.html | 12 | 0 | 12 |
| /referrer-policy/4K+1/gen/top.http-rp/no-referrer-when-downgrade/script-tag.http.html | 12 | 0 | 12 |
| /referrer-policy/4K+1/gen/top.http-rp/no-referrer-when-downgrade/xhr.http.html | 12 | 0 | 12 |
| /referrer-policy/4K+1/gen/top.http-rp/unsafe-url/fetch.http.html | 12 | 0 | 12 |
| /referrer-policy/4K+1/gen/top.http-rp/unsafe-url/script-tag.http.html | 12 | 0 | 12 |
| /referrer-policy/4K+1/gen/top.http-rp/unsafe-url/xhr.http.html | 12 | 0 | 12 |
| /referrer-policy/4K+1/gen/top.meta/no-referrer-when-downgrade/fetch.http.html | 12 | 0 | 12 |
| /referrer-policy/4K+1/gen/top.meta/no-referrer-when-downgrade/script-tag.http.html | 12 | 0 | 12 |
| /referrer-policy/4K+1/gen/top.meta/no-referrer-when-downgrade/xhr.http.html | 12 | 0 | 12 |
| /referrer-policy/4K+1/gen/top.meta/unsafe-url/fetch.http.html | 12 | 0 | 12 |
| /referrer-policy/4K+1/gen/top.meta/unsafe-url/script-tag.http.html | 12 | 0 | 12 |
| /referrer-policy/4K+1/gen/top.meta/unsafe-url/xhr.http.html | 12 | 0 | 12 |
| /referrer-policy/gen/iframe.http-rp/no-referrer-when-downgrade/fetch.http.html | 12 | 0 | 12 |
| /referrer-policy/gen/iframe.http-rp/no-referrer-when-downgrade/script-tag.http.html | 12 | 0 | 12 |
| /referrer-policy/gen/iframe.http-rp/no-referrer-when-downgrade/xhr.http.html | 12 | 0 | 12 |
| /referrer-policy/gen/iframe.http-rp/unsafe-url/fetch.http.html | 12 | 0 | 12 |
| /referrer-policy/gen/iframe.http-rp/unsafe-url/script-tag.http.html | 12 | 0 | 12 |
| /referrer-policy/gen/iframe.http-rp/unsafe-url/xhr.http.html | 12 | 0 | 12 |
| /referrer-policy/gen/iframe.meta/always/fetch.http.html | 12 | 0 | 12 |
| /referrer-policy/gen/iframe.meta/always/script-tag.http.html | 12 | 0 | 12 |
| /referrer-policy/gen/iframe.meta/always/xhr.http.html | 12 | 0 | 12 |
| /referrer-policy/gen/iframe.meta/no-referrer-when-downgrade/fetch.http.html | 12 | 0 | 12 |
| /referrer-policy/gen/iframe.meta/no-referrer-when-downgrade/script-tag.http.html | 12 | 0 | 12 |
| /referrer-policy/gen/iframe.meta/no-referrer-when-downgrade/xhr.http.html | 12 | 0 | 12 |
| /referrer-policy/gen/iframe.meta/unsafe-url/fetch.http.html | 12 | 0 | 12 |
| /referrer-policy/gen/iframe.meta/unsafe-url/script-tag.http.html | 12 | 0 | 12 |
| /referrer-policy/gen/iframe.meta/unsafe-url/xhr.http.html | 12 | 0 | 12 |
| /referrer-policy/gen/req.attr/no-referrer/script-tag.http.html | 12 | 0 | 12 |
| /referrer-policy/gen/req.attr/origin/script-tag.http.html | 12 | 0 | 12 |
| /referrer-policy/gen/req.attr/strict-origin/script-tag.http.html | 12 | 0 | 12 |
| /referrer-policy/gen/req.attr/origin-when-cross-origin/script-tag.http.html | 12 | 2 | 12 |
| /referrer-policy/gen/req.attr/strict-origin-when-cross-origin/script-tag.http.html | 12 | 2 | 12 |
| /referrer-policy/gen/req.attr/same-origin/script-tag.http.html | 10 | 2 | 10 |
| /content-security-policy/securitypolicyviolation/constructor-required-fields.html | 13 | 7 | 14 |
| /mixed-content/gen/sharedworker-classic-data.http-rp/opt-in/fetch.https.html | 6 | 0 | 8 |
| /mixed-content/gen/sharedworker-classic-data.http-rp/opt-in/xhr.https.html | 6 | 0 | 8 |
| /mixed-content/gen/sharedworker-classic-data.meta/unset/fetch.https.html | 6 | 0 | 8 |

**Commits between** (67)

- `cde84eba9` Referrer: a request carries a Referer cut down by its policy for each hop (Net.PageFetch.referrerOf on ReferrerPolicy.decide)
- `0a932e05b` Net.Xhr: a request's referrer and referrer policy (web_api op 98); the client's URL and policy
- `05326c69b` Referrer: the document or worker that asks gives the URL and the policy (node_query 210, web_api 98)
- `d48590547` prelude: SharedWorker and SharedWorkerGlobalScope on the dedicated worker core
- `7946b12ce` fetch: mode no-cors with opaque responses, redirect mode manual, Response.type from Lean, Origin by policy, fetch metadata
- `bbf86053d` Subresource Integrity for fetch (Net.Integrity, web_api 99)
- `f3fa1c683` Net.CspPolicy: a page's Content Security Policy parsed and decided in Lean
- `bd1798880` Content Security Policy at the session: connect-src for fetch and XMLHttpRequest, the violation queue, ops 150 to 153
- `a4bec450e` HTML.CspSource: a document's meta policies and the parser-inserted scripts its policy lets run
- `142ebbc77` library root: the new networking modules
- `b204c0147` Content Security Policy enforced: scripts, workers, event handler attributes, connect-src; securitypolicyviolation events
- `6cf868526` Net.Cookies: the HTTP side: Set-Cookie of a response, the Cookie field of a request, SameSite, the __Http- prefixes
- `cf471b158` build-web-render: build HTML.CspSource with the core modules (WebScripts imports it)
- `a833e71ed` Net.PageFetch: the Cookie field of a request made with credentials, from the transfer's jar
- `597c674bf` build-web-render: link HTML.CspSource (the native link enumerates its own roots)
- `2cc443c8d` Page: node_query 210 (a document's referrer source) reaches Hosts.Dom.domOp
- `eafd255f4` skills: crashes, hangs and resource exhaustion are safety properties with proved bounds
- `342f63c74` ImageDecoder in Lean: image MIME type verdict (typeVerdict_supported), the Exif orientation of a JPEG as rotation and flip (exifOrientation_
- `b4588d613` ImageDecoder, ImageTrackList and ImageTrack over Lean's ops 133 and 134 and the engine's decoders: still PNG, JPEG and GIF images as one tra
- `0102de4fe` createImageBitmap(blob): the blob's bytes decoded by the engine's decoders (a canvas bitmap of kind 5, cropped by the crop rectangle); an im
- `7d8abc6ff` WebGL: drawingBufferToneMapping on both context interfaces (standard or extended, kept on the context); WebGLObject's label attribute
- `44f8c17c9` WebGL framebuffer objects in Lean (PageGl.State): attachments, renderbuffer storage, checkFramebufferStatus (status_default), level 0 of 2D 
- `d88a0519a` docs: WebGL and WebCodecs record: colour spaces, ImageDecoder, framebuffer objects, their theorems
- `bad7e94ef` Canvas: HTMLCanvasElement.toBlob and OffscreenCanvas.convertToBlob over Lean's encoder (a PNG Blob; null or IndexSizeError for a canvas with
- `8142840aa` Canvas text: a maxWidth that is given and is NaN or not above zero draws nothing; no maxWidth is +Infinity on the wire (it was NaN, so fillT
- `a64e905c5` Canvas: getContext('2d', options) with options that are not an object takes the default settings
- `73dc819a0` AES: hardware only. Theorems that AES output needs the CPU's AES instructions, a gate against software AES, and the skill
- `8c2dfe55c` Keys in a text control: the control counts as hidden only when it or an ancestor has display: none (measure op 20), not when it has no box (
- `f3003dfb5` WebDriver glue: the JSON clone of a script's result is bounded at 64 levels, as Page.fromWire is (a deeper result is a javascript error)
- `adeeaaee3` Cookie Store: change events for the store's own writes; the changed and deleted cookies computed in Lean
- `d4152ea7b` docs: client storage record covers the file pickers, storage buckets and the Cookie Store
- `c9d5e96c0` Cache API: CacheStorage and Cache over the caches of a storage key in Lean (query cache with ignoreSearch, ignoreMethod and Vary; put checks
- `29bc9d8ac` StorageManager.estimate counts IndexedDB store descriptions and the Cache API's entries; usageDetails.caches
- `72aaf0168` docs: client storage record covers the Cache API and the estimate
- `bebbc7d59` Workers that are not secure contexts do not expose navigator.storage, navigator.locks, storageBuckets or the [SecureContext] storage interfa
- `8788b6b2b` IndexedDB: a transaction stays active while its listeners' promise jobs run; a handle of a finished transaction answers InvalidStateError wh
- `573357700` Storage page side: IndexedDB event handler attributes brand-checked; createSyncAccessHandle and persist() exposed by the worker flag; LockMa
- `b669a679a` File System Access: queryPermission and requestPermission of a handle, answered by the file system model (the origin private file system's h
- `a40b9a424` BubblePopJS: Object.prototype.__defineGetter__, __defineSetter__, __lookupGetter__, __lookupSetter__ (ECMA-262 Annex B.2.2.2 to B.2.2.5)
- `2b1693576` IndexedDB: theorems for the exception order of a finished transaction's handles
- `e4ee03daa` FileSystemWritableFileStream: write, seek, truncate, close and abort reject on a wrong receiver or a missing argument instead of throwing
- `9a947892d` IndexedDB: schema methods on a finished upgrade transaction's handle answer TransactionInactiveError before the name checks (theorem schemaG
- `74ca62b0e` docs: client storage record: transaction activity across promise jobs; exception-order theorems
- `fee2bfe2d` Cookie Store: document.cookie writes fire change events while the document's cookieStore exists (Lean docset, proved to write the jar as op 
- `55043075a` getComputedStyle: revert-layer and revert roll back in the cascade
- `1273230b9` selectorText: An+B in its canonical form
- `edfa14c20` Shapes: the radii after round in their shortest form
- `9cec42936` Relative colours: each component has the type its channel takes
- `008993352` Gap rule shorthands: lists of rules and repeat()
- `81b7e5758` CSSOM: a media query with a syntax error is 'not all' in mediaText
- `7231d9bda` CSSOM bindings: CSSRule constants on the prototype; MediaList members on MediaList.prototype
- `eabcca924` @property: rules checked and serialised, CSSPropertyRule, registered custom properties in getComputedStyle
- `20993b5f5` Selectors: comments are no tokens
- `a8d38029e` CSSOM: @scope preludes as selectors
- `1b4f6c64a` CSS Values 5 progress()
- `095e1ea6b` selectorText: *| is left out when the sheet declares no default namespace
- `aa21aed07` Design record: the regressions of the first check and the third part's CSSOM work
- `0393bdcec` CSS.registerProperty: the registration joins the document's registered property set
- `2c2fc06d0` Typed OM: custom properties are unparsed values, registered ones typed by their syntax
- `370fa7658` StylePropertyMap.set: a registered custom property takes the values of its syntax
- `f2b0041d8` Media queries: a negative calc() in a ratio is clamped to 0
- `f87a33f8c` will-change identifiers; overflow: clip in getComputedStyle; display: -webkit-box
- `c10be5622` Selectors: ::scroll-button() and :host(<compound>)
- `24f882425` Relative colours: an origin in the target space keeps its channels
- `aa1a4fb65` Specified colours keep the math functions of lab(), lch(), oklab(), oklch() and color()
- `712049208` Colour channels: calc(infinity) is the upper bound, calc(-infinity) and calc(NaN) the lower
- `a9e7eaef2` Gradients: the default colour interpolation method is left out of the canonical value

