### Since the previous full run: -6 subtests (-0.0003 points)

Previous: `20261117T0757Z-wpt-linux-x86_64-gh44041032609a1`, core `efd07bd22`, 92.4581%. This run: core `68b2a2a1c`, 92.4579%; 14 commits between.
Tests that lost subtests: 4 (-7); that gained: 1 (+1). Page outcomes: unchanged.

**Directories that fell** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| shadow-dom | 14,720 | 14,129 | 14,126 | -3 |
| webcodecs | 3,922 | 2,574 | 2,572 | -2 |
| html/semantics | 22,381 | 15,192 | 15,191 | -1 |
| service-workers | 3,262 | 1,394 | 1,393 | -1 |

**Directories that rose** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| IndexedDB | 5,853 | 5,503 | 5,504 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 4 directories, the first 4)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| shadow-dom/declarative | 3 | 1 |
| webcodecs | 2 | 1 |
| html/semantics | 1 | 1 |
| service-workers/cache-storage | 1 | 1 |

**Tests that lost most** (the first 4 of 4)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /shadow-dom/declarative/declarative-shadow-dom-repeats.html | 3 | 0 | 3 |
| /webcodecs/image-decoder.https.any.html | 15 | 13 | 47 |
| /html/semantics/embedded-content/the-img-element/list-of-available-images-does-not-coalesce-in-flight-requests.sub.tentative.html | 1 | 0 | 1 |
| /service-workers/cache-storage/cache-abort.https.any.serviceworker.html | 9 | 8 | 9 |

**Commits between** (14)

- `e495228bf` BubblePopJS: ToNumber of a Number with no call (toNumQ) in the numeric and bit operators, unary -, ~ and typedConv
- `45e929c5d` BubblePopJS: a typed array's element is read by a Number key with no key string
- `5aa1ea62b` BubblePopJS: a typed array's element is written by a Number key with no key string
- `87bef5c0b` BubblePopJS: String.front compiled as one read (Prim/StringFront.lean), not a slice and an Option
- `d4099cfaf` BubblePopJS regular expressions: a search for a pattern anchored with ^ stops at position 0
- `93f2ac365` A page's start in slices: the first frame does not wait for module scripts and tasks
- `31ed8df06` BubblePopJS register machine: a typed array's element is read before the registers are stashed
- `ca08e419c` lean-csimp-reach.py: String.front is a core left side (Prim/StringFront.lean)
- `c2e8c52de` Merge main into wip/hotpath-b
- `c5794fdd2` Merge remote-tracking branch 'origin/main' into hotpath-b
- `11d2f763f` Merge remote-tracking branch 'origin/main' into bbc-start-slices
- `53cf39d46` Hot paths 2 on main: typed-array fast paths use typedLenOf (length-tracking views); index keys are never private keys (lemma); putV/getV ref
- `db1cda1d2` Merge pull request #573 from danbri/wip/bbc-start-slices
- `68b2a2a1c` Merge pull request #571 from danbri/wip/hotpath-b

