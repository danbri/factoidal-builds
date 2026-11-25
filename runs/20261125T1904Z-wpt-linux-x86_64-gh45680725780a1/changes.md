### Since the previous full run: +4 subtests (+0.0002 points)

Previous: `20261125T1814Z-wpt-linux-x86_64-gh45672409584a1`, core `af74c4f5d`, 92.6359%. This run: core `3f499a901`, 92.6361%; 9 commits between.
Tests that lost subtests: 5 (-10); that gained: 5 (+14). Page outcomes: CRASH +1, ERROR +1, OK -2.

**Directories that fell** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html-aam | 1,016 | 855 | 847 | -8 |
| IndexedDB | 5,853 | 5,504 | 5,503 | -1 |
| html/semantics | 22,523 | 15,617 | 15,616 | -1 |

**Directories that rose** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| accname | 515 | 435 | 441 | +6 |
| html/interaction | 842 | 338 | 342 | +4 |
| webcodecs | 4,138 | 2,722 | 2,725 | +3 |
| fetch | 13,314 | 8,822 | 8,823 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 4 directories, the first 4)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| html-aam/accname-computation-by-element | 6 | 2 |
| html-aam | 2 | 1 |
| IndexedDB | 1 | 1 |
| html/semantics | 1 | 1 |

**Tests that lost most** (the first 5 of 5)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /html-aam/accname-computation-by-element/section-and-grouping-elements.html | 100 | 96 | 100 |
| /html-aam/accname-computation-by-element/area.html | 4 | 2 | 7 |
| /html-aam/optgroup-name.tentative.html | 2 | 0 | 4 |
| /IndexedDB/interleaved-cursors-large.any.html | 1 | 0 | 1 |
| /html/semantics/embedded-content/the-img-element/list-of-available-images-does-not-coalesce-in-flight-requests.sub.tentative.html | 1 | 0 | 1 |

**Commits between** (9)

- `6277aa530` tools/foafnaut-ab.py: use the factoidal-builds release library of a commit when there is one
- `27785eb55` tools/foafnaut-ab.py: gate also runs the svg and html reftests
- `05f93669d` tools/foafnaut-ab.py: suites fetches the release library when no library is kept
- `9ddee1ddf` tools/foafnaut-ab.py: stub the wasm runtime import when absent; refuse a suite run where every test is CRASH
- `cde500432` Respect CSS visibility in accessible names (#1067)
- `41789954b` Handle pinned IPv6 addresses in Deno TCP proxies
- `3312ae035` Apply CSS transforms to positioned and block replaced boxes (#1062)
- `37ebba864` Resolve horizontal-grid percentage edges after track sizing (#1052)
- `3f499a901` Use HTML’s element-specific defaults for tabIndex (#1070)

