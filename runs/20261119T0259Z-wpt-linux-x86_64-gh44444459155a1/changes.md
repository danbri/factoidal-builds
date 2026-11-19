### Since the previous full run: -2 subtests (-0.0001 points)

Previous: `20261119T0201Z-wpt-linux-x86_64-gh44438459868a1`, core `3249012ac`, 92.5978%. This run: core `1ba2ef928`, 92.5978%; 2 commits between.
Tests that lost subtests: 5 (-5); that gained: 3 (+3). Page outcomes: CRASH -1, OK +1.

**Directories that fell** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| fetch | 13,290 | 8,808 | 8,807 | -1 |
| html/semantics | 22,416 | 15,576 | 15,575 | -1 |
| preload | 956 | 243 | 242 | -1 |
| shadow-dom | 14,724 | 14,133 | 14,132 | -1 |

**Directories that rose** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| web-locks | 517 | 448 | 449 | +1 |
| webcodecs | 3,926 | 2,576 | 2,577 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 5 directories, the first 5)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| fetch/metadata | 1 | 1 |
| html/semantics | 1 | 1 |
| preload | 1 | 1 |
| shadow-dom/declarative | 1 | 1 |
| third_party/test262 | 1 | 1 |

**Tests that lost most** (the first 5 of 5)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /fetch/metadata/generated/element-img.https.sub.html | 19 | 18 | 45 |
| /html/semantics/embedded-content/the-img-element/list-of-available-images-does-not-coalesce-in-flight-requests.sub.tentative.html | 1 | 0 | 1 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |
| /shadow-dom/declarative/declarative-shadow-dom-repeats-2.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/assignment/dstr/ident-name-prop-name-literal-let-escaped.test262.html | 1 | 0 | 1 |

**Commits between** (2)

- `7de3af4e7` Package Foafnaut with a native Linux window and desktop input
- `1ba2ef928` Merge pull request #617 from danbri/wip/linux-browser-build

