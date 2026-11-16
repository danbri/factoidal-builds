### Since the previous full run: +669 subtests (+0.0294 points)

Previous: `20261116T1211Z-wpt-linux-x86_64-gh43864240722a1`, core `9fd90c894`, 91.9770%. This run: core `1ad66797e`, 92.0065%; 5 commits between.
Tests that lost subtests: 4 (-14); that gained: 41 (+683). Page outcomes: ERROR -2, OK +1, STALL -1, TIMEOUT +2.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 3,922 | 2,584 | 2,576 | -8 |
| dom/nodes | 15,595 | 14,838 | 14,837 | -1 |

**Directories that rose** (9; the first 9)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| url | 12,437 | 11,768 | 12,356 | +588 |
| html/infrastructure | 1,664 | 918 | 979 | +61 |
| mixed-content | 2,281 | 1,296 | 1,309 | +13 |
| content-security-policy | 4,544 | 2,499 | 2,503 | +4 |
| html/semantics | 22,381 | 15,173 | 15,176 | +3 |
| shadow-dom | 14,720 | 14,126 | 14,129 | +3 |
| xhr | 2,344 | 1,818 | 1,821 | +3 |
| service-workers | 3,262 | 1,391 | 1,393 | +2 |
| html/browsers | 3,309 | 766 | 767 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 3 directories, the first 3)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| webcodecs | 8 | 1 |
| dom/nodes | 5 | 2 |
| html/semantics | 1 | 1 |

**Tests that lost most** (the first 4 of 4)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /webcodecs/image-decoder.https.any.html | 25 | 17 | 47 |
| /dom/nodes/Document-cloneNode-about-base-url.window.html | 4 | 1 | 5 |
| /dom/nodes/Document-cloneNode-base-url-xml.window.html | 2 | 0 | 3 |
| /html/semantics/embedded-content/the-img-element/list-of-available-images-does-not-coalesce-in-flight-requests.sub.tentative.html | 1 | 0 | 1 |

**Commits between** (5)

- `43a97d928` Frozen base URL: <base href> set or changed by script resolves reflected URLs (url/ a-element*); BaseURL theorems, 46 guards
- `fe719a70a` Base URLs at zero cost on pages without a base: inlined idle checks, slow paths out of line, base fields in BaseURL.State; encoding prescan 
- `893901e4e` Base URLs: select again only when a change can alter the selected base (no tree walk per append on a page with a base); removals name the re
- `fa038a174` Base URLs tracked from the first use only: no base work at mutations of a page that reads no URL; changedBases out of the records so command
- `1ad66797e` Frozen base URL record: lazy tracking, gated selection, timings against main, checks

