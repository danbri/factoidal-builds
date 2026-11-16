### Since the previous full run: +1,837 subtests (+0.0808 points)

Previous: `20261116T0008Z-wpt-linux-x86_64-gh43778572970a1`, core `82ad63988`, 91.8546%. This run: core `1b2fc90d5`, 91.9355%; 17 commits between.
Tests that lost subtests: 21 (-52); that gained: 1,723 (+1,889). Page outcomes: CRASH +1, ERROR -42, OK +21, STALL -1, TIMEOUT +21.

**Directories that fell** (6; the first 6)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| urlpattern | 3,266 | 3,014 | 2,994 | -20 |
| custom-elements | 4,822 | 3,833 | 3,820 | -13 |
| webcodecs | 3,922 | 2,584 | 2,571 | -13 |
| fetch | 13,288 | 8,813 | 8,812 | -1 |
| html/dom | 72,400 | 69,541 | 69,540 | -1 |
| js | 160 | 65 | 64 | -1 |

**Directories that rose** (8; the first 8)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| third_party/test262 | 53,833 | 43,533 | 45,233 | +1,700 |
| html/infrastructure | 1,664 | 775 | 888 | +113 |
| html/webappapis | 3,674 | 2,975 | 3,021 | +46 |
| html/semantics | 22,381 | 15,154 | 15,173 | +19 |
| ecmascript | 21 | 13 | 17 | +4 |
| xhr | 2,344 | 1,816 | 1,818 | +2 |
| preload | 956 | 242 | 243 | +1 |
| workers | 1,598 | 703 | 704 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 8 directories, the first 8)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| urlpattern | 20 | 12 |
| webcodecs | 13 | 1 |
| custom-elements | 12 | 1 |
| html/semantics | 3 | 3 |
| custom-elements/registries | 1 | 1 |
| fetch/metadata | 1 | 1 |
| html/dom | 1 | 1 |
| js/builtins | 1 | 1 |

**Tests that lost most** (the first 21 of 21)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /webcodecs/image-decoder.https.any.html | 25 | 12 | 47 |
| /custom-elements/CustomElementRegistry.html | 43 | 31 | 46 |
| /urlpattern/urlpattern.any.html | 368 | 366 | 370 |
| /urlpattern/urlpattern.any.serviceworker.html | 368 | 366 | 370 |
| /urlpattern/urlpattern.any.sharedworker.html | 368 | 366 | 370 |
| /urlpattern/urlpattern.any.worker.html | 368 | 366 | 370 |
| /urlpattern/urlpattern.https.any.html | 368 | 366 | 370 |
| /urlpattern/urlpattern.https.any.serviceworker.html | 368 | 366 | 370 |
| /urlpattern/urlpattern.https.any.sharedworker.html | 368 | 366 | 370 |
| /urlpattern/urlpattern.https.any.worker.html | 368 | 366 | 370 |
| /custom-elements/registries/define.html | 70 | 69 | 70 |
| /fetch/metadata/generated/element-img.https.sub.html | 18 | 17 | 45 |
| /html/dom/documents/dom-tree-accessors/document.scripts.html | 1 | 0 | 1 |
| /html/semantics/scripting-1/the-script-element/import-attributes/invalid-import-errors-order.html | 1 | 0 | 1 |
| /html/semantics/scripting-1/the-script-element/import-attributes/unsupported-attribute.html | 1 | 0 | 1 |
| /html/semantics/scripting-1/the-script-element/json-module/parse-error.html | 1 | 0 | 1 |
| /js/builtins/Promise-subclassing.html | 1 | 0 | 8 |
| /urlpattern/urlpattern-generate.tentative.any.html | 11 | 10 | 20 |
| /urlpattern/urlpattern-generate.tentative.any.serviceworker.html | 11 | 10 | 20 |
| /urlpattern/urlpattern-generate.tentative.any.sharedworker.html | 11 | 10 | 20 |
| /urlpattern/urlpattern-generate.tentative.any.worker.html | 11 | 10 | 20 |

**Commits between** (17)

- `e0e235b17` Test262 host for BubblePopJS: no CRASH or STALL, $262 realms, import(), top-level await, JSON modules
- `01156778d` Modules: indirect exports resolved at link, a module's functions are lexical, for-in with await on the generator machine, shared Symbol regi
- `cf22c0eae` Promise combinators append values without Array.prototype setters; runner heap 2^22; import.source() rejects with a TypeError
- `b79e7bb92` Tail-recursion gate: constructNative and protoFromCtor, fuel-bounded calls as construct and get
- `4d8f37e72` Test262 runner: an error of the module graph after an import is the test's outcome
- `501d91d02` Import attributes: an unknown key parses and is refused when the module is loaded (SyntaxError at resolution)
- `1d014d20d` BubblePopJS Test262 built-ins: RegExp (Unicode 17 properties, code points with u/v, Canonicalize, backward lookbehind, modifiers, v class se
- `11ef3831b` Merge pull request #499 from danbri/wip/t262-builtins
- `0a62bf28a` HostContract: every Foafnaut target described in Lean (model, trace conformance, cross-host agreement theorems)
- `2fcec0287` Host contract: boundary traces from Textnaut (native, Wasm) and the Hub's Textnaut host, checked by the engine (op hostContract); scroll lim
- `d1cae0dfe` Host contract: point the records at issue 458
- `3860cbdf9` HostContract: violations after its csimp theorem, so the compiled checker uses the loop (lean-csimp-reach gate)
- `1513ef6be` LabHygiene imports WebHostContract, so the hygiene ratchet sees the new lab module
- `07f5983f9` cpu_render_diff_check: serve finite-floats.mjs, which render_plan.ts imports since 3e6745f19 (the Hub layer surface failed to load)
- `ce5f07d65` spinal-bisect budgets: static probe frame limit at spinal-perf's 1500 ms (accepted: 560 ms on the macOS CI runner, about 500 ms on an M1 in 
- `be8f7503e` Merge pull request #459 from danbri/wip/host-contract
- `1b2fc90d5` Tail-recursion allow lines: deleteOrThrow (Proxy chain) and arrayGeneric (fuel-bounded [[Get]]/[[Set]] cycle) from #499

