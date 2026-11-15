### Since the previous full run: +42 subtests (+0.0019 points)

Previous: `20261114T2321Z-wpt-linux-x86_64-gh43652848883a1`, core `ff075ad5a`, 91.8449%. This run: core `8c96d3ec8`, 91.8468%; 3 commits between.
Tests that lost subtests: 3 (-11); that gained: 41 (+53). Page outcomes: ERROR +1, OK +337, STALL -1, TIMEOUT -337.

**Directories that fell** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 3,922 | 2,584 | 2,575 | -9 |
| content-security-policy | 4,544 | 2,501 | 2,500 | -1 |
| html/semantics | 22,381 | 15,155 | 15,154 | -1 |

**Directories that rose** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| websockets | 2,389 | 1,229 | 1,260 | +31 |
| mixed-content | 2,281 | 1,291 | 1,309 | +18 |
| connection-allowlist | 365 | 85 | 89 | +4 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 3 directories, the first 3)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| webcodecs | 9 | 1 |
| content-security-policy/connect-src | 1 | 1 |
| html/semantics | 1 | 1 |

**Tests that lost most** (the first 3 of 3)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /webcodecs/image-decoder.https.any.html | 25 | 16 | 47 |
| /content-security-policy/connect-src/connect-src-websocket-allowed.sub.html | 1 | 0 | 1 |
| /html/semantics/embedded-content/the-img-element/list-of-available-images-does-not-coalesce-in-flight-requests.sub.tentative.html | 1 | 0 | 1 |

**Commits between** (3)

- `421f10a45` WebSocket: a socket in its opening handshake keeps the page waiting for the network (Net.Xhr.State.waiting), so settling stops there; before
- `a4a046275` Textnaut 0.1.3: the engine of 0.37.0 (build-ff075ad5af99-foafnaut-web, 11.7 MB); the package carries page-load.mjs inside app/ and rewrites 
- `8c96d3ec8` Hub: a script turn whose animated values changed asks for a layered frame, as the engine's animation clock does; a whole-page frame at the r

