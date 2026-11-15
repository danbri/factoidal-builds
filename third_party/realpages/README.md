# Real-page snapshots

Snapshots of public web pages for the offline runs of the real-page survey
(`.github/workflows/realpages.yml`; tools in danbri/factoidal-core `labs/demos/foafnaut/realpages/`:
`snapshot.ts` makes them, `replay.ts` answers a host's requests from them, `survey.ts --snapshots`
runs the survey on them). Public pages only, nothing behind a login; each is vendored as fair use for
testing a web browser, under the licence and with the attribution below, and is not for
redistribution as content.

Each ZIP holds `manifest.json` (the URL, the fetch time, every response kept with its status and
HTTP header fields and the server's address, and every response left out with the reason),
`PROVENANCE.txt`, `reference.png` (headless Chrome's picture of the page area at the time) and the
decoded response bodies under `bodies/`. First come the requests the Foafnaut host made itself
(run_html.ts of factoidal-core cc73af028 on its engine, off screen for 15 s, recorded by
`replay.ts`), then the document as the host's plain fetch gets it, then the other responses
headless Chrome received while loading the page (a fresh profile; Set-Cookie fields dropped). Media, files over 1.5 MB, images over 300 KB and anything past 6 MB a page are
left out.

Refresh: `deno run -A labs/demos/foafnaut/realpages/snapshot.ts --out third_party/realpages` in a
core checkout writes `<site>/<id>-<YYYYMMDD>.zip`; the survey takes the newest of each page. Remove
the old one when the new one is committed (size: keep this directory under 50 MB).

| Snapshot | URL | Fetched | Licence | Responses | Size |
|---|---|---|---|---|---|
| [bbc.co.uk/news-bbc-20261115.zip](bbc.co.uk/news-bbc-20261115.zip) | https://www.bbc.co.uk/news/articles/cwdr1dmn563do | 2026-11-15T18:39Z | copyright of its owners; public page vendored as fair use for testing | 128 kept, 0 left out | 2.87 MB |
| [developer.mozilla.org/mdn-display-20261115.zip](developer.mozilla.org/mdn-display-20261115.zip) | https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/display | 2026-11-15T18:41Z | prose CC BY-SA 2.5 (https://creativecommons.org/licenses/by-sa/2.5/), code samples CC0; site of Mozilla; Mozilla Contributors, MDN Web Docs, https://developer.mozilla.org/ | 130 kept, 0 left out | 0.99 MB |
| [en.m.wikipedia.org/m-stub-enm-20261115.zip](en.m.wikipedia.org/m-stub-enm-20261115.zip) | https://en.m.wikipedia.org/wiki/Spodnje_Danje | 2026-11-15T18:38Z | text CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/); images under their own licences; skin and scripts of the Wikimedia Foundation (GPL-2.0+ MediaWiki); Wikipedia contributors, "Spodnje Danje", https://en.wikipedia.org/wiki/Spodnje_Danje | 66 kept, 0 left out | 0.88 MB |
| [en.wikipedia.org/m-spinal-20261115.zip](en.wikipedia.org/m-spinal-20261115.zip) | https://en.wikipedia.org/wiki/This_Is_Spinal_Tap?useskin=minerva | 2026-11-15T18:37Z | text CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/); images under their own licences; skin and scripts of the Wikimedia Foundation (GPL-2.0+ MediaWiki); Wikipedia contributors, "This Is Spinal Tap", https://en.wikipedia.org/wiki/This_Is_Spinal_Tap | 50 kept, 0 left out | 0.89 MB |
| [en.wikipedia.org/m-stub-20261115.zip](en.wikipedia.org/m-stub-20261115.zip) | https://en.wikipedia.org/wiki/Spodnje_Danje?useskin=minerva | 2026-11-15T18:36Z | text CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/); images under their own licences; skin and scripts of the Wikimedia Foundation (GPL-2.0+ MediaWiki); Wikipedia contributors, "Spodnje Danje", https://en.wikipedia.org/wiki/Spodnje_Danje | 53 kept, 0 left out | 0.85 MB |
| [en.wikipedia.org/m-us-20261115.zip](en.wikipedia.org/m-us-20261115.zip) | https://en.wikipedia.org/wiki/United_States?useskin=minerva | 2026-11-15T18:38Z | text CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/); images under their own licences; skin and scripts of the Wikimedia Foundation (GPL-2.0+ MediaWiki); Wikipedia contributors, "United States", https://en.wikipedia.org/wiki/United_States | 103 kept, 2 left out | 1.85 MB |
| [en.wikipedia.org/wp-spinal-20261115.zip](en.wikipedia.org/wp-spinal-20261115.zip) | https://en.wikipedia.org/wiki/This_Is_Spinal_Tap | 2026-11-15T18:34Z | text CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/); images under their own licences; skin and scripts of the Wikimedia Foundation (GPL-2.0+ MediaWiki); Wikipedia contributors, "This Is Spinal Tap", https://en.wikipedia.org/wiki/This_Is_Spinal_Tap | 54 kept, 0 left out | 1.10 MB |
| [en.wikipedia.org/wp-stub-20261115.zip](en.wikipedia.org/wp-stub-20261115.zip) | https://en.wikipedia.org/wiki/Spodnje_Danje | 2026-11-15T18:34Z | text CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/); images under their own licences; skin and scripts of the Wikimedia Foundation (GPL-2.0+ MediaWiki); Wikipedia contributors, "Spodnje Danje", https://en.wikipedia.org/wiki/Spodnje_Danje | 56 kept, 0 left out | 1.06 MB |
| [en.wikipedia.org/wp-us-20261115.zip](en.wikipedia.org/wp-us-20261115.zip) | https://en.wikipedia.org/wiki/United_States | 2026-11-15T18:35Z | text CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/); images under their own licences; skin and scripts of the Wikimedia Foundation (GPL-2.0+ MediaWiki); Wikipedia contributors, "United States", https://en.wikipedia.org/wiki/United_States | 104 kept, 2 left out | 1.99 MB |
| [github.com/gh-deno-20261115.zip](github.com/gh-deno-20261115.zip) | https://github.com/denoland/deno | 2026-11-15T18:41Z | copyright of its owners; public page vendored as fair use for testing | 150 kept, 4 left out | 1.80 MB |
| [jvns.ca/blog-jvns-20261115.zip](jvns.ca/blog-jvns-20261115.zip) | https://jvns.ca/ | 2026-11-15T18:42Z | copyright of its owners; public page vendored as fair use for testing | 35 kept, 0 left out | 0.67 MB |
| [news.ycombinator.com/hn-20261115.zip](news.ycombinator.com/hn-20261115.zip) | https://news.ycombinator.com/ | 2026-11-15T18:42Z | copyright of its owners; public page vendored as fair use for testing | 6 kept, 0 left out | 0.19 MB |
| [w3.org/w3c-flexbox-20261115.zip](w3.org/w3c-flexbox-20261115.zip) | https://www.w3.org/TR/css-flexbox-1/ | 2026-11-15T18:43Z | W3C Document License (https://www.w3.org/copyright/document-license-2023/); W3C, CSS Flexible Box Layout Module Level 1, https://www.w3.org/TR/css-flexbox-1/ | 31 kept, 0 left out | 0.42 MB |

Total: 15.57 MB.
