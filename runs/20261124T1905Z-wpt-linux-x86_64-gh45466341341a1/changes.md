### Since the previous full run: +3 subtests (+0.0001 points)

Previous: `20261124T1733Z-wpt-linux-x86_64-gh45447091963a1`, core `074a3e51f`, 92.6282%. This run: core `bbac00eea`, 92.6283%; 11 commits between.
Tests that lost subtests: 1 (-1); that gained: 1 (+4). Page outcomes: unchanged.

**Directories that fell** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| fetch | 13,290 | 8,807 | 8,806 | -1 |

**Directories that rose** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/css-flexbox | 4,933 | 3,893 | 3,897 | +4 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 1 directories, the first 1)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| fetch/metadata | 1 | 1 |

**Tests that lost most** (the first 1 of 1)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /fetch/metadata/generated/element-img.https.sub.html | 18 | 17 | 45 |

**Commits between** (11)

- `a1cabc364` Decode bounded lossy WebP key-frame controls and partitions (#921)
- `1763d4a0b` Decode bounded VP8L entropy planes (#922)
- `c8ba916ea` Add a Hub page of rule-based explanations for the MLP Wikidata queries
- `ba81433bc` Merge pull request #926 from danbri/claude/wikidata-query-explanations
- `9549f2873` Present Wikidata result views as a QLever gallery (#929)
- `7517927eb` Serve credited Commons thumbnails in the Wikidata gallery (#930)
- `5052a26af` Version the Wikidata gallery assets together (#933)
- `71a7067fc` Load Wikidata previews on scroll and check parser capabilities (#935)
- `51701d034` Page host: an attribute write is seen as one that changes the rules only when the written element is a style or link element; before, the wh
- `70ce18105` Page host: a child write is seen as one that changes the rules only when the added or removed nodes hold a style or link element, or the par
- `bbac00eea` testharness-run: load the sheets that the page's sheets import (page-load.mjs loadImports) and give them as imported to fontFaces and to the

