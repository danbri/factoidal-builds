### Since the previous full run: +1,230 subtests (+0.0542 points)

Previous: `20261114T1829Z-wpt-linux-x86_64-gh43625567767a1`, core `53326e401`, 91.7565%. This run: core `3b456743b`, 91.8106%; 18 commits between.
Tests that lost subtests: 12 (-24); that gained: 890 (+1,254). Page outcomes: CRASH +7, OK -7.

**Directories that rose** (10; the first 10)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| third_party/test262 | 53,833 | 42,515 | 43,375 | +860 |
| html/semantics | 22,381 | 15,024 | 15,154 | +130 |
| html/rendering | 11,705 | 8,334 | 8,461 | +127 |
| IndexedDB | 5,853 | 5,397 | 5,493 | +96 |
| webcodecs | 3,922 | 2,575 | 2,584 | +9 |
| storage | 482 | 449 | 453 | +4 |
| fs | 1,121 | 994 | 995 | +1 |
| js | 160 | 64 | 65 | +1 |
| preload | 956 | 46 | 47 | +1 |
| webidl | 838 | 646 | 647 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 4 directories, the first 4)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| html/semantics | 16 | 4 |
| third_party/test262 | 6 | 6 |
| html/dom | 1 | 1 |
| html/rendering | 1 | 1 |

**Tests that lost most** (the first 12 of 12)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /html/semantics/popovers/popover-light-dismiss-command.html | 11 | 5 | 14 |
| /html/semantics/popovers/popover-light-dismiss-input-button.html | 11 | 5 | 14 |
| /html/semantics/popovers/popover-light-dismiss.html | 18 | 15 | 33 |
| /html/dom/documents/dom-tree-accessors/document.getElementsByName/document.getElementsByName-interface.html | 1 | 0 | 1 |
| /html/rendering/non-replaced-elements/the-page/iframe-body-margin-attributes.html | 2 | 1 | 3 |
| /html/semantics/popovers/popover-invoking-attribute.html | 1,402 | 1,401 | 1,402 |
| /third_party/test262/test/built-ins/Array/prototype/concat/create-proto-from-ctor-realm-array.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/Array/prototype/filter/create-proto-from-ctor-realm-array.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/Array/prototype/map/create-proto-from-ctor-realm-array.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/Array/prototype/slice/create-proto-from-ctor-realm-array.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/Array/prototype/splice/create-proto-from-ctor-realm-array.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/staging/sm/extensions/typedarray-set-detach.test262.html | 1 | 0 | 1 |

**Commits between** (18)

- `62cf38ddc` BubblePopJS: the RegExp protocol (Symbol.match, replace, search, split, matchAll)
- `a50f473c3` BubblePopJS: ArraySpeciesCreate; an accessor on an Array index
- `dac003dd4` BubblePopJS: regular expression literals checked as the source is parsed; slice by its bounds
- `649173a7a` BubblePopJS: Array.from and Array.of with a constructor this; IsConstructor of a bound function
- `337a1b124` BubblePopJS: typed array [[DefineOwnProperty]], TypedArraySpeciesCreate; fixes from check 43598972695
- `791913da2` tail-recursion allow list: the six BubblePopJS functions of the RegExp protocol and species (bounded as calls)
- `c9c818aaa` Selector matching: no string or sibling array built per test
- `0fa63d71f` Structural pseudo-classes read the parent's child list in place
- `14dbb9bab` Cascade: a :has() inside :is(), :not(), :where() or an of-list is matched once per document too
- `3646690f9` Cascade: structural pseudo-classes worked out once per document
- `48ce9a85f` Cascade: :has() and structural pseudo-classes worked out once also for pages with shadow trees
- `6a8248d61` StorageBucket.estimate counts the bucket's own caches and reports its quota (Manager.bucketEstimate)
- `356d0b912` FileSystemObserver is not defined in service workers
- `1b84bdbdf` docs: client storage record: measured after 83c04db95; proxy keys open
- `c405cd169` Client storage budget: one 32 MiB quota per storage key over IndexedDB, the file system and the Cache API, at most 8 keys with data per sess
- `15d14e7ea` Popovers: light dismiss (a trusted pointerdown and pointerup with the same topmost clicked auto popover hide the auto popovers shown after i
- `e1be74649` Page: node_query's string reaches the measure (pageQuery q), so a frame body gets its container's marginwidth/marginheight; the popover IDL 
- `3b456743b` Reflected IDL attributes: the getter and the fast setter make one host call with no helper calls (the hot path of reflected reads)

