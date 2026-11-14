### Since the previous full run: +9,723 subtests (+0.4284 points)

Previous: `20261114T0609Z-wpt-linux-x86_64-gh43564968070a1`, core `262289028`, 84.6344%. This run: core `d799500c7`, 85.0629%; 14 commits between.
Tests that lost subtests: 69 (-1,530); that gained: 308 (+11,253). Page outcomes: CRASH -3, ERROR -27, NO_RESULT -2, OK -35, TIMEOUT +67.

**Directories that fell** (11; the first 11)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| encoding/legacy-mb-japanese | 447,723 | 447,722 | 446,722 | -1,000 |
| dom/ranges | 44,720 | 40,355 | 39,917 | -438 |
| connection-allowlist | 365 | 85 | 73 | -12 |
| xhr | 2,344 | 1,605 | 1,596 | -9 |
| clear-site-data | 59 | 9 | 1 | -8 |
| cors | 463 | 352 | 349 | -3 |
| custom-elements | 4,404 | 3,420 | 3,419 | -1 |
| gamepad | 116 | 42 | 41 | -1 |
| subresource-integrity | 491 | 129 | 128 | -1 |
| third_party/test262 | 53,833 | 36,342 | 36,341 | -1 |
| wasm/serialization | 76 | 6 | 5 | -1 |

**Directories that rose** (36; the first 36)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| quirks | 6,984 | 2,123 | 6,883 | +4,760 |
| html/syntax | 8,984 | 5,284 | 8,512 | +3,228 |
| svg/interact | 9,295 | 6,862 | 8,806 | +1,944 |
| css/css-cascade | 1,759 | 360 | 837 | +477 |
| html/browsers | 3,303 | 352 | 565 | +213 |
| referrer-policy | 8,815 | 3,564 | 3,772 | +208 |
| fetch | 13,288 | 4,359 | 4,486 | +127 |
| content-security-policy | 4,544 | 1,607 | 1,710 | +103 |
| html/webappapis | 3,665 | 2,473 | 2,519 | +46 |
| mixed-content | 2,281 | 1,119 | 1,133 | +14 |
| html/dom | 72,323 | 67,368 | 67,377 | +9 |
| x-frame-options | 157 | 60 | 69 | +9 |
| webstorage | 1,291 | 1,228 | 1,236 | +8 |
| html/cross-origin-embedder-policy | 596 | 94 | 100 | +6 |
| compute-pressure | 187 | 2 | 7 | +5 |
| permissions-policy | 638 | 34 | 39 | +5 |
| css/cssom-view | 2,696 | 690 | 694 | +4 |
| FileAPI | 1,645 | 1,193 | 1,196 | +3 |
| font-access | 38 | 0 | 3 | +3 |
| html/semantics | 22,364 | 11,840 | 11,843 | +3 |
| clipboard-apis | 253 | 14 | 16 | +2 |
| cookies | 1,293 | 109 | 111 | +2 |
| dom/events | 927 | 640 | 642 | +2 |
| dom/nodes | 15,420 | 14,761 | 14,763 | +2 |
| html/infrastructure | 1,664 | 596 | 598 | +2 |
| upgrade-insecure-requests | 982 | 234 | 236 | +2 |
| webusb | 845 | 60 | 62 | +2 |
| client-hints | 205 | 57 | 58 | +1 |
| cookiestore | 636 | 44 | 45 | +1 |
| hsts | 1 | 0 | 1 | +1 |
| mediacapture-insertable-streams | 94 | 2 | 3 | +1 |
| mediacapture-streams | 497 | 21 | 22 | +1 |
| svg/linking | 148 | 22 | 23 | +1 |
| webcodecs | 3,922 | 9 | 10 | +1 |
| webmessaging | 304 | 138 | 139 | +1 |
| webxr | 1,342 | 138 | 139 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 23 directories, the first 23)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| encoding/legacy-mb-japanese | 1,000 | 1 |
| dom/ranges | 439 | 3 |
| connection-allowlist/tentative | 15 | 3 |
| xhr | 12 | 10 |
| html/semantics | 11 | 11 |
| mixed-content/gen | 9 | 7 |
| clear-site-data | 8 | 2 |
| html/browsers | 8 | 7 |
| html/infrastructure | 4 | 4 |
| content-security-policy/sandbox | 3 | 3 |
| cors | 3 | 1 |
| html/webappapis | 3 | 2 |
| content-security-policy/form-action | 2 | 2 |
| content-security-policy/frame-src | 2 | 2 |
| third_party/test262 | 2 | 2 |
| webmessaging | 2 | 2 |
| content-security-policy/child-src | 1 | 1 |
| content-security-policy/generic | 1 | 1 |
| custom-elements/registries | 1 | 1 |
| gamepad | 1 | 1 |
| secure-contexts | 1 | 1 |
| subresource-integrity/integrity-policy | 1 | 1 |
| wasm/serialization | 1 | 1 |

**Tests that lost most** (the first 40 of 69)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /encoding/legacy-mb-japanese/euc-jp/eucjp-decode-x-euc-jp.html?1001-2000 | 1,000 | 0 | 1,000 |
| /dom/ranges/Range-cloneContents.html | 181 | 1 | 187 |
| /dom/ranges/Range-extractContents.html | 140 | 1 | 187 |
| /dom/ranges/Range-deleteContents.html | 121 | 1 | 125 |
| /connection-allowlist/tentative/navigation-response-origin.sub.window.html | 12 | 0 | 12 |
| /clear-site-data/navigation-insecure.html | 4 | 0 | 4 |
| /clear-site-data/navigation.https.html | 4 | 0 | 4 |
| /cors/preflight-cache.htm | 3 | 0 | 6 |
| /xhr/xmlhttprequest-sync-default-permissions-policy.tentative.sub.html | 5 | 2 | 5 |
| /connection-allowlist/tentative/navigation-wildcard.sub.window.html | 7 | 5 | 12 |
| /html/browsers/windows/nested-browsing-contexts/window-top.html | 3 | 1 | 3 |
| /html/webappapis/scripting/events/onerroreventhandler.html | 3 | 1 | 3 |
| /mixed-content/gen/iframe-inherit.http-rp/opt-in/worker-import-data.https.html | 8 | 6 | 8 |
| /mixed-content/gen/srcdoc-inherit.meta/unset/worker-import.https.html | 8 | 6 | 8 |
| /connection-allowlist/tentative/navigation-redirect-allow.sub.window.html | 3 | 2 | 3 |
| /content-security-policy/child-src/child-src-allowed.sub.html | 2 | 1 | 2 |
| /content-security-policy/form-action/form-action-src-allowed-target-frame.sub.html | 1 | 0 | 1 |
| /content-security-policy/form-action/form-action-src-get-allowed.sub.html | 1 | 0 | 1 |
| /content-security-policy/frame-src/frame-src-allowed.sub.html | 2 | 1 | 2 |
| /content-security-policy/frame-src/frame-src-sandboxed-allowed.html | 1 | 0 | 1 |
| /content-security-policy/generic/policy-does-not-affect-child.sub.html | 1 | 0 | 1 |
| /content-security-policy/sandbox/iframe-inside-csp.sub.html | 1 | 0 | 1 |
| /content-security-policy/sandbox/sandbox-allow-scripts.sub.html | 1 | 0 | 1 |
| /content-security-policy/sandbox/sandbox-last-directive-csp.html | 1 | 0 | 1 |
| /custom-elements/registries/initial-about-blank.window.html | 1 | 0 | 4 |
| /gamepad/gamepad-permissions-policy-event-listener.html | 1 | 0 | 1 |
| /html/browsers/browsing-the-web/navigating-across-documents/anchor-fragment-form-submit-longfragment.html | 1 | 0 | 1 |
| /html/browsers/browsing-the-web/navigating-across-documents/anchor-fragment-form-submit-withpath.html | 1 | 0 | 1 |
| /html/browsers/browsing-the-web/navigating-across-documents/anchor-fragment-form-submit.html | 1 | 0 | 1 |
| /html/browsers/browsing-the-web/navigating-across-documents/anchor-jsurl-form-submit.html | 1 | 0 | 1 |
| /html/browsers/sandboxing/sandbox-window-open-srcdoc.html | 1 | 0 | 2 |
| /html/browsers/the-window-object/window-reuse-in-nested-browsing-contexts.tentative.html | 4 | 3 | 7 |
| /html/infrastructure/safe-passing-of-structured-data/structured-cloning-error-extra.html | 1 | 0 | 2 |
| /html/infrastructure/urls/resolving-urls/query-encoding/windows-1251.html?include=svg | 1 | 0 | 4 |
| /html/infrastructure/urls/resolving-urls/query-encoding/windows-1252.html?include=svg | 1 | 0 | 4 |
| /html/infrastructure/urls/terminology-0/document-base-url-about-srcdoc.https.window.html | 1 | 0 | 2 |
| /html/semantics/embedded-content/the-iframe-element/sandbox_012.htm | 1 | 0 | 1 |
| /html/semantics/embedded-content/the-iframe-element/sandbox_013.htm | 1 | 0 | 1 |
| /html/semantics/embedded-content/the-iframe-element/sandbox_014.htm | 1 | 0 | 1 |
| /html/semantics/embedded-content/the-iframe-element/sandbox_015.htm | 1 | 0 | 1 |

**Commits between** (14)

- `348de4289` Frames: a frame window keeps what is set on it; a frame's message names its window; Math.random seeded per page
- `540722dd5` Frames: a document's origin is its response URL's, asked after it is attached; documents of another origin get a session of their own
- `a10eba562` prelude: a rewritten frame document's childNodes follow the new document; fetch abort errors the response body
- `6a2b9d09e` SVG text: the lowered group keeps the text's pointer-events
- `de0dfebfb` prelude: the Origin interface (Origin.from, opaque, isSameOrigin, isSameSite)
- `c0c84bf25` docs: frames of another origin, frame windows, written documents and the seed in the networking and SVG record
- `9631481e6` Links navigate frames: a link in a frame's document, or one whose target names a frame (node_query 190)
- `34d6de630` prelude: postMessage() in a frame's script posts to that frame's window
- `3295b0160` Frames: a blob URL has the origin of the URL in its path
- `5423cef2a` SVG links: an SVG a element with an href has activation behaviour and navigates frames
- `e0642e054` docs: rounds 2 and 3 measured, blob URL origins and links into frames in the networking and SVG record
- `d16c72012` prelude: storage events between the windows of a realm; a frame's body handlers are its own window's
- `6e1a6342a` WPT runner: a page request names the browser, as a browser host's HTTP client does
- `d799500c7` fetch: redirect mode error is decided in Lean (web_api op 79)

