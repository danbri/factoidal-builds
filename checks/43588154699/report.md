## Branch WPT check: `ef8b0d869` (ef8b0d8698f1)

**10,114 of 10,242 Chrome subtests passed; baseline 10,114; difference +0.** 20 of 20 names run at WPT `2358bd4835`. 0 tests got worse, 0 got better. Baseline: `20261114T0949Z-wpt-linux-x86_64-gh43581071421a1` (core `2b464c0a8ade`). A development check of the selected names, not a score.

### Crashes, stalls and harness timeouts of these names (against the baseline)

CRASH 1, STALL 0, TIMEOUT 6; against `20261114T0949Z-wpt-linux-x86_64-gh43581071421a1`: CRASH 4 -> 1 (+0 new, -3 gone), STALL 0 -> 0 (+0 new, -0 gone), TIMEOUT 3 -> 6 (+3 new, -0 gone).

**CRASH** (1, by top directory; NEW: not in the previous run's list)

- wasm/
  - `/wasm/core/f32.wast.js.html`: halted: step budget exhausted

**No longer CRASH** (3): `/serial/serial-allowed-by-permissions-policy-attribute.https.sub.html`, `/serial/serial-allowed-by-permissions-policy.https.sub.html`, `/serial/serial-disabled-by-permissions-policy.https.sub.html`

**New TIMEOUT** (3): `/serial/serial-allowed-by-permissions-policy-attribute.https.sub.html`, `/serial/serial-allowed-by-permissions-policy.https.sub.html`, `/serial/serial-disabled-by-permissions-policy.https.sub.html`


| Directory | Names | Chrome subtests | Passed | Baseline | Difference | Outcomes |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| dom/abort | 10/10 | 72 | 41 | 41 | +0 | OK 10 |
| serial | 7/7 | 137 | 42 | 42 | +0 | OK 2, TIMEOUT 5 |
| serial/getPorts | 1/1 | 1 | 0 | 0 | +0 | TIMEOUT 1 |
| serial/requestPort | 1/1 | 1 | 0 | 0 | +0 | OK 1 |
| wasm/core | 1/1 | 10,031 | 10,031 | 10,031 | +0 | CRASH 1 |

### Tests that got worse (0)


### Tests that got better (0; the largest 40)

