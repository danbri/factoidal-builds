### Since the previous full run: +105 subtests (+0.0046 points)

Previous: `20261119T0443Z-wpt-linux-x86_64-gh44458826256a1`, core `4120db7d1`, 92.6205%. This run: core `182c86e47`, 92.6251%; 6 commits between.
Tests that lost subtests: 7 (-13); that gained: 17 (+118). Page outcomes: CRASH -1, OK -2, STALL +2, TIMEOUT +1.

**Directories that fell** (6; the first 6)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 3,926 | 2,577 | 2,573 | -4 |
| IndexedDB | 5,853 | 5,504 | 5,503 | -1 |
| html/semantics | 22,416 | 15,576 | 15,575 | -1 |
| service-workers | 3,268 | 1,393 | 1,392 | -1 |
| shadow-dom | 14,724 | 14,133 | 14,132 | -1 |
| third_party/test262 | 53,838 | 46,250 | 46,249 | -1 |

**Directories that rose** (10; the first 10)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| sanitizer-api | 3,816 | 2,562 | 2,625 | +63 |
| css/css-sizing | 6,743 | 5,101 | 5,138 | +37 |
| css/css-position | 1,605 | 1,371 | 1,375 | +4 |
| css/css-writing-modes | 421 | 219 | 223 | +4 |
| css/css-align | 5,473 | 4,452 | 4,453 | +1 |
| css/css-flexbox | 4,933 | 3,798 | 3,799 | +1 |
| css/css-overflow | 1,215 | 725 | 726 | +1 |
| html/rendering | 11,717 | 10,092 | 10,093 | +1 |
| preload | 956 | 242 | 243 | +1 |
| web-locks | 517 | 448 | 449 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 7 directories, the first 7)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| html/rendering | 4 | 1 |
| webcodecs | 4 | 1 |
| IndexedDB | 1 | 1 |
| html/semantics | 1 | 1 |
| service-workers/cache-storage | 1 | 1 |
| shadow-dom/declarative | 1 | 1 |
| third_party/test262 | 1 | 1 |

**Tests that lost most** (the first 7 of 7)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /html/rendering/widgets/baseline-alignment-and-overflow.tentative.html | 4 | 0 | 132 |
| /webcodecs/image-decoder.https.any.html | 14 | 10 | 47 |
| /IndexedDB/interleaved-cursors-large.any.html | 1 | 0 | 1 |
| /html/semantics/forms/the-select-element/select-option-display-inherit.tentative.html | 1 | 0 | 3 |
| /service-workers/cache-storage/cache-abort.https.any.worker.html | 9 | 8 | 9 |
| /shadow-dom/declarative/declarative-shadow-dom-repeats-2.html | 1 | 0 | 1 |
| /third_party/test262/test/language/eval-code/direct/cptn-nrml-expr-prim.test262.html | 1 | 0 | 1 |

**Commits between** (6)

- `50d17b22d` Limit Darwin browser engine exports to the public shim ABI
- `1cff5bd6f` Keep anonymous control text out of page geometry
- `4b330942d` Integrate current Linux browser and PI attribute landings
- `9d347b60c` Preserve nested control boxes and make pacing fixture deterministic
- `e089543af` Merge remote-tracking branch 'origin/main' into wip/mac-release-closeout
- `182c86e47` Merge pull request #606 from danbri/wip/mac-release-closeout

