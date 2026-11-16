### Since the previous full run: +4 subtests (+0.0002 points)

Previous: `20261115T2330Z-wpt-linux-x86_64-gh43775154889a1`, core `9504dce9e`, 91.8545%. This run: core `82ad63988`, 91.8546%; 10 commits between.
Tests that lost subtests: 3 (-5); that gained: 2 (+9). Page outcomes: OK -3, STALL +3.

**Directories that fell** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| shadow-dom | 14,720 | 14,129 | 14,126 | -3 |
| html/semantics | 22,381 | 15,155 | 15,154 | -1 |
| preload | 956 | 243 | 242 | -1 |

**Directories that rose** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 3,922 | 2,576 | 2,584 | +8 |
| service-workers | 3,262 | 1,392 | 1,393 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 3 directories, the first 3)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| shadow-dom/declarative | 3 | 1 |
| html/semantics | 1 | 1 |
| preload | 1 | 1 |

**Tests that lost most** (the first 3 of 3)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /shadow-dom/declarative/declarative-shadow-dom-repeats.html | 3 | 0 | 3 |
| /html/semantics/embedded-content/the-img-element/available-images-onload.html | 1 | 0 | 1 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |

**Commits between** (10)

- `93b1d9ef8` BubblePopJS: register machine is a parameter of the run (HeapOf.useVm, BUBBLEPOP_VM=off for leanjs); blockN in Stmt.contOutF and genEnter; t
- `901932f5b` BubblePopJS: a halt passes through every handler (catchJS at 69 tryCatch sites)
- `8bcef5c72` BubblePopJS: fuel monotonicity, the relation and its rules (JS/FuelMono.lean); drop the tier-1 cases on this branch
- `80443298d` BubblePopJS fuel monotonicity: rules for forIn (List, Array, Range), mapM, foldlM, filterMapM, map; walk tactic in two halves around the gen
- `71f6b49aa` BubblePopJS fuel monotonicity spike: 75 of 116 step lemmas proved by a generated walk (JS/FuelMonoSteps.lean); the state of the proof in JS/
- `553226525` Merge pull request #487 from danbri/wip/jit-proof
- `c95c532d8` Light shared start page, stress tests page, demo index tidy, ray-marching demo (#492)
- `44d660c16` raymarch.html: frame-rate modes and frame-time percentiles
- `d2c0d20ab` Veil models: system-level transition systems in formal/veil (#494)
- `82ad63988` Hub Conformance: semantic web and data formats, one row per suite, OWL 2 by population (#497)

