### Since the previous full run: -246 subtests (-0.0108 points)

Previous: `20261115T1616Z-wpt-linux-x86_64-gh43730704981a1`, core `b4bcecec8`, 91.8477%. This run: core `6efc9cffb`, 91.8369%; 18 commits between.
Tests that lost subtests: 6 (-249); that gained: 1 (+3). Page outcomes: OK +1, STALL -3, TIMEOUT +2.

**Directories that fell** (5; the first 5)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| selection/(root) | 33,918 | 33,664 | 33,432 | -232 |
| webcodecs | 3,922 | 2,584 | 2,571 | -13 |
| html/semantics | 22,381 | 15,155 | 15,153 | -2 |
| preload | 956 | 243 | 242 | -1 |
| service-workers | 3,262 | 1,393 | 1,392 | -1 |

**Directories that rose** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| shadow-dom | 14,720 | 14,126 | 14,129 | +3 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 5 directories, the first 5)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| selection | 232 | 1 |
| webcodecs | 13 | 1 |
| html/semantics | 2 | 2 |
| preload | 1 | 1 |
| service-workers/cache-storage | 1 | 1 |

**Tests that lost most** (the first 6 of 6)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /selection/addRange-44.html | 232 | 0 | 232 |
| /webcodecs/image-decoder.https.any.html | 25 | 12 | 47 |
| /html/semantics/embedded-content/the-img-element/available-images-onload.html | 1 | 0 | 1 |
| /html/semantics/embedded-content/the-img-element/list-of-available-images-does-not-coalesce-in-flight-requests.sub.tentative.html | 1 | 0 | 1 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |
| /service-workers/cache-storage/cache-abort.https.any.serviceworker.html | 9 | 8 | 9 |

**Commits between** (18)

- `b75785156` CI: F* workflows run only by hand
- `7541db440` fast-verify-extract skill: the CI F* caches serve manual runs only
- `3e6745f19` Finite-float checks in a loop, not every(): 7.6 of 11 ms of an unchanged frame (issue 450)
- `bcc551039` Merge pull request #461 from danbri/wip/no-fstar
- `e98d545ed` Spinal Tap page taken apart: 25 variants, engine and window, feature against added cost (issue 450)
- `e4406808e` spinal_bisect_check.ts in test.sh; budgets from the fast run; SKILL.md; CPU samples of an exited window ignored (issue 450)
- `173c907d0` spinal_bisect.ts: type check clean
- `1a2ddd3c4` Merge pull request #460 from danbri/wip/finite-check
- `074c2aa4d` Merge pull request #462 from danbri/wip/spinal-bisect
- `05ebe0cd7` Linux libweb-render.so needs no Lean toolchain at run time
- `63f2caee0` Textnaut: --install-native installs the Linux engine; engine_parity.py compares native and Wasm
- `289d29896` Textnaut: --install-native TAG installs that release, if it is self-contained
- `f25d2f899` Textnaut docs: the native engine on Linux; engine_parity.py: several links for Tab, blank grids compare
- `ec6a312d4` build-leanrt-no-gmp.sh (Linux): hidden __isoc23_* forwarders, so the library links against the toolchain's older glibc
- `06d899e03` textnaut sync.mjs: skip a __pycache__ directory left by the Python checks
- `84d5a5ac9` engine_parity.py: read the terminal while textnaut quits, kill its process group, bound the quiet wait, print each key time and the terminal
- `1dbca74ce` engine_parity.py: read the top bar without colour escapes (24-bit gradient splits the words)
- `6efc9cffb` Merge pull request #463 from danbri/wip/linux-native

