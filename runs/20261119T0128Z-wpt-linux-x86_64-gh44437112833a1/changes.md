### Since the previous full run: -4 subtests (-0.0002 points)

Previous: `20261119T0108Z-wpt-linux-x86_64-gh44434604204a1`, core `e3303f6ef`, 92.5977%. This run: core `3249012ac`, 92.5975%; 12 commits between.
Tests that lost subtests: 4 (-5); that gained: 1 (+1). Page outcomes: OK -2, STALL +1, TIMEOUT +1.

**Directories that fell** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| user-timing | 862 | 805 | 803 | -2 |
| html/semantics | 22,416 | 15,576 | 15,575 | -1 |
| service-workers | 3,268 | 1,393 | 1,392 | -1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 4 directories, the first 4)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| user-timing | 2 | 1 |
| html/semantics | 1 | 1 |
| service-workers/cache-storage | 1 | 1 |
| third_party/test262 | 1 | 1 |

**Tests that lost most** (the first 4 of 4)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /user-timing/measure-with-dict.any.worker.html | 2 | 0 | 2 |
| /html/semantics/embedded-content/the-img-element/list-of-available-images-does-not-coalesce-in-flight-requests.sub.tentative.html | 1 | 0 | 1 |
| /service-workers/cache-storage/cache-abort.https.any.worker.html | 9 | 8 | 9 |
| /third_party/test262/test/built-ins/Array/prototype/with/ignores-species.test262.html | 1 | 0 | 1 |

**Commits between** (12)

- `07ff6ac92` Cookies for page loads: the engine's jar for navigations, hop by hop, lasting cookies on disk
- `162da7b78` Merge branch 'wip/daily-basics' into wip/daily-cookies
- `ab51d6dbe` Merge branch 'wip/daily-basics' into wip/daily-cookies
- `76533870b` Merge remote-tracking branch 'origin/main' into wip/daily-cookies
- `7f900a794` Merge remote-tracking branch 'origin/main' into wip/596-cookie-contract
- `9d5b4f8a0` Register cookie jar calculations in the host contract
- `9d3af6188` Drain serial cookie saves before shutting down the engine
- `c8c1546e6` Frame persisted cookies reversibly and prove restoration contracts
- `31526924a` Check cookie restoration proofs against fresh bounded Lean builds
- `505d40b1d` Resolve frame normalization and empty expiry proof obligations
- `d7f6c2a8b` Prove empty expiry parsing using the string numeric specification
- `3249012ac` Merge cookie persistence and navigation fixes

