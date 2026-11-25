### Since the previous full run: +32 subtests (+0.0014 points)

Previous: `20261125T0028Z-wpt-linux-x86_64-gh45517751795a1`, core `4e8b173fd`, 92.6316%. This run: core `d38eaddb3`, 92.6330%; 13 commits between.
Tests that lost subtests: 1 (-1); that gained: 5 (+33). Page outcomes: OK +3, STALL -3.

**Directories that rose** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/dom | 72,463 | 69,902 | 69,929 | +27 |
| webcodecs | 4,168 | 2,636 | 2,639 | +3 |
| IndexedDB | 5,853 | 5,503 | 5,504 | +1 |
| preload | 956 | 242 | 243 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 1 directories, the first 1)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| html/semantics | 1 | 1 |

**Tests that lost most** (the first 1 of 1)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /html/semantics/embedded-content/the-img-element/list-of-available-images-does-not-coalesce-in-flight-requests.sub.tentative.html | 1 | 0 | 1 |

**Commits between** (13)

- `530319505` Hub: Wikidata queries as set browsing (Parallax view), one page per query
- `4fd549461` Keep generated quotes with their nowrap words
- `7b81d5bd1` Let headings balance below completed floats
- `23b95d44c` Preserve background image CSS-wide shorthand values
- `762216329` Integrate the settled GOV.UK search control and balanced headings
- `8f560793c` Merge pull request #975 from danbri/wip/w3c-nowrap-quote-line-break
- `17242ba7f` Merge pull request #979 from danbri/wip/background-shorthand-wide-image
- `aa2c4b775` Merge pull request #974 from danbri/claude/wikidata-parallax-page
- `fc246f938` Add the Wikidata query explainer and set-browsing classifier
- `c9c6f48bd` Font clusters: byte-to-character lookup in an array, not a tree map
- `894b4d8a3` Restyle after child writes: sheet signature, and :has()-safe child writes (issue 871)
- `11c6771da` Draw content: url() images in ::before and ::after (issue 874, part 1)
- `d38eaddb3` Merge pull request #978 from danbri/wip/balance-below-floats

