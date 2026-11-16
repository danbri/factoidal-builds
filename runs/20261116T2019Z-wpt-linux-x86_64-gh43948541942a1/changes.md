### Since the previous full run: -4 subtests (-0.0002 points)

Previous: `20261116T1852Z-wpt-linux-x86_64-gh43930830879a1`, core `8a22b20a3`, 92.0306%. This run: core `efa7f089c`, 92.0305%; 11 commits between.
Tests that lost subtests: 2 (-5); that gained: 1 (+1). Page outcomes: OK +1, TIMEOUT -1.

**Directories that fell** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| mixed-content | 2,281 | 1,309 | 1,304 | -5 |

**Directories that rose** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/semantics | 22,381 | 15,175 | 15,176 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 1 directories, the first 1)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| mixed-content/gen | 5 | 2 |

**Tests that lost most** (the first 2 of 2)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /mixed-content/gen/iframe-inherit.meta/unset/worklet-paint-import-data.https.html | 6 | 2 | 8 |
| /mixed-content/gen/iframe-inherit.meta/opt-in/worklet-animation-import-data.https.html | 4 | 3 | 5 |

**Commits between** (11)

- `b42b559f8` WIP BubblePopJS fuel monotonicity over the whole block (not all checked yet): walk as one tactic with info trees off, built-in lemmas from t
- `4242929c8` WIP fuel monotonicity: rules for if, filterM, inRealm, discard; match reduction; capped split; iterCloseAbrupt out of fuel at 0 (was not mon
- `7888e885d` BubblePopJS fuel monotonicity over the block after the natives move: 126 steps generated in groups, built-in lemmas from the dispatcher (in 
- `efca8bc81` BubblePopJS fuel monotonicity: IH_all proved, on the built-ins split by family (issue 531)
- `271146d92` fetch-builds: take the ancestor release nearest HEAD, not the newest published (an older commit published late put an engine without PR 516 
- `9dafebe13` Fuel-monotonicity tactics: loops in place of recursion in the compiled code (the tail-recursion gate)
- `3b925035e` Merge main (the split of the built-in dispatchers and the iterCloseAbrupt fix are in)
- `fbc67b0bc` Canvas 2D: any change of a canvas's width or height attribute resets its bitmap and context state (HTML 4.12.5), not only the property sette
- `2ff4472d2` Merge pull request #546 from danbri/wip/fetch-builds-nearest
- `f64cb2e67` Merge pull request #539 from danbri/wip/fuelmono-all
- `efa7f089c` Merge pull request #548 from danbri/wip/iso3-canvas

