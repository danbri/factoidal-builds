### Since the previous full run: +3,511 subtests (+0.1547 points)

Previous: `20261114T1851Z-wpt-macos-arm64-gh43628874175a1`, core `c3d227a9f`, 91.6558%. This run: core `3b456743b`, 91.8105%; 34 commits between.
Tests that lost subtests: 16 (-30); that gained: 1,075 (+3,541). Page outcomes: CRASH +7, OK -6, STALL +1, TIMEOUT -2.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 3,922 | 2,578 | 2,575 | -3 |
| xhr | 2,344 | 1,815 | 1,814 | -1 |

**Directories that rose** (22; the first 22)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/css-grid | 16,015 | 9,115 | 11,121 | +2,006 |
| third_party/test262 | 53,833 | 42,513 | 43,375 | +862 |
| css/css-text | 5,863 | 3,134 | 3,297 | +163 |
| html/semantics | 22,381 | 15,024 | 15,168 | +144 |
| html/rendering | 11,705 | 8,334 | 8,461 | +127 |
| IndexedDB | 5,853 | 5,397 | 5,493 | +96 |
| css/css-sizing | 6,523 | 4,968 | 5,012 | +44 |
| css/CSS2 | 2,566 | 2,421 | 2,432 | +11 |
| css/css-flexbox | 4,813 | 3,671 | 3,681 | +10 |
| css/css-position | 1,553 | 1,335 | 1,345 | +10 |
| referrer-policy | 8,815 | 4,571 | 4,581 | +10 |
| css/css-writing-modes | 421 | 209 | 218 | +9 |
| css/css-inline | 869 | 631 | 636 | +5 |
| css/css-values | 10,428 | 4,901 | 4,905 | +4 |
| storage | 482 | 449 | 453 | +4 |
| css/css-contain | 499 | 305 | 307 | +2 |
| css/cssom | 4,463 | 3,604 | 3,606 | +2 |
| css/cssom-view | 2,696 | 1,189 | 1,191 | +2 |
| compat | 143 | 101 | 102 | +1 |
| fs | 1,121 | 994 | 995 | +1 |
| js | 160 | 64 | 65 | +1 |
| webidl | 838 | 646 | 647 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 8 directories, the first 8)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| html/semantics | 16 | 4 |
| third_party/test262 | 6 | 6 |
| webcodecs | 3 | 1 |
| css/css-fonts | 1 | 1 |
| css/css-inline | 1 | 1 |
| css/css-tables | 1 | 1 |
| html/rendering | 1 | 1 |
| xhr | 1 | 1 |

**Tests that lost most** (the first 16 of 16)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /html/semantics/popovers/popover-light-dismiss-command.html | 11 | 5 | 14 |
| /html/semantics/popovers/popover-light-dismiss-input-button.html | 11 | 5 | 14 |
| /html/semantics/popovers/popover-light-dismiss.html | 18 | 15 | 33 |
| /webcodecs/image-decoder.https.any.html | 19 | 16 | 47 |
| /css/css-fonts/font-size-zero-ligatures.html | 1 | 0 | 4 |
| /css/css-inline/text-box-trim/text-box-on-non-root-inline-box.html | 1 | 0 | 4 |
| /css/css-tables/tentative/td-box-sizing-003.html | 5 | 4 | 11 |
| /html/rendering/non-replaced-elements/the-page/iframe-body-margin-attributes.html | 2 | 1 | 3 |
| /html/semantics/popovers/popover-invoking-attribute.html | 1,402 | 1,401 | 1,402 |
| /third_party/test262/test/built-ins/Array/prototype/concat/create-proto-from-ctor-realm-array.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/Array/prototype/filter/create-proto-from-ctor-realm-array.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/Array/prototype/map/create-proto-from-ctor-realm-array.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/Array/prototype/slice/create-proto-from-ctor-realm-array.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/Array/prototype/splice/create-proto-from-ctor-realm-array.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/staging/sm/extensions/typedarray-set-detach.test262.html | 1 | 0 | 1 |
| /xhr/xhr-timeout-longtask.any.html | 1 | 0 | 1 |

**Commits between** (34)

- `27861e975` docs: dataflow inventory: Temporal joins the directories no entry names (65 of 91)
- `b24a33007` Animated values reach the frame a host paints: the layout field animated, carried from each script turn
- `44f3011af` @import: imported style sheets are fetched and read in place; a session hears of late sheets
- `1b0be2f57` The image of an img is chosen from srcset and picture, among the formats the engine decodes
- `46bade4dd` The window shows a page before its images are in, and draws it again with them
- `82f6359ad` A turn's answer gives the animated values of the session's last layout
- `2f2b194df` The window loads the QuickJS guest when a page first runs on it
- `d00e26040` The window's first compile of a page asks for no CPU probe
- `1692b7e4b` The loader reads a page's sheets and scripts six at a time, in document order
- `f62e2a738` fontFaces: no cascade when the page's rules name every face
- `03294d47e` Real pages record: animated values, @import, image sources, the time to a first frame, the runner's page font
- `8691b3265` The loader reads a page's scripts, images and icon while its sheets are read
- `81bbd5efa` The window makes the main-thread engine's first call while the page is fetched
- `89f9af642` Real pages record: the loader's concurrent reads, the main-thread engine's first call, the warm-up that was tried
- `7e88ef022` The window: images after the first frame only for a page that runs no script; the main-thread engine's first call during the first compile
- `53326e401` A page's own web fonts are the fonts of its text when no page font is held
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

