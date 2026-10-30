# Checked FOAFNaut SVG packaging controls

`scripts/build-foafnaut.sh` now detects policy-capable core sources by the
presence of `labs/demos/foafnaut/PolicyBridge.lean`. Older labs keep their
existing checks and do not need the new browser assets or export flags.
A declared policy capability cannot silently omit these files or results.

In the relocated package directory, whose path includes spaces, the script:

1. Runs the compiled UI with `--demo foafnaut --emit-svg checked.svg`.
2. Runs the compiled native SVG executable on that exact file, with
   `--emit-artifact checked-native.json`.
3. Validates the SVG, `checked.svg.policy.json`, storage artifact and browser
   package assets with `scripts/check-foafnaut-policy.py`.
4. Saves the validated policy report in build metadata as `foafnaut-policy.json`.

The required browser package consists of policy-demo.html, policy-demo.mjs,
policy_engine.mjs, foafnaut_transport.mjs, people.ttl and both the FOAFNaut and
layout-policy engine JS/WASM pairs under the paths used by core's packager.
The WASM files must have a version-one WebAssembly header.

The report must name experimental-graph-browser-v1, the clipped pairwise-box
metric and export-only timing. Application bounds must be ordered subranges
of overlap 300..700 basis points and requested check rate 12..24 Hz; chosen
values must stay inside the application's bounds. Node reports must be
nonempty, use distinct person indices, have positive viewport-clipped areas,
match the reported pairwise overlap sum and satisfy the chosen budget.
These are independent release-test assertions about exported evidence, not a
second application admission API or a theorem establishing useful UX bounds.

The native artifact must use lean-svg-v1/read-only-storage, match exported SVG
dimensions and painted-primitive count, have finite bounded tagged records and
well-formed Lean reference probes. The validator checks record lengths and
array bounds as well as the presence of a storage shader. This does not prove
shader execution, raster equivalence or GPU-driver behavior. No OS scheduling
or browser execution claim follows from this gate.

## Validation

The original twelve release-control tests pass unchanged. Eight additional
tests pass: valid evidence, policy mutations, missing browser assets, invalid
storage/probe evidence, duplicate JSON keys, legacy-source packaging, capable
source export/compile path identity, and missing-web failure. Mutation controls
include a caller choosing 700 against an application capped at 500, duplicated
or understated overlap evidence and uniform-buffer artifacts. The shell tests
use explicit stub binaries, not fake GPU/conformance results.

`python3 -m unittest discover -s tests -v`: 20 tests pass.
`bash -n scripts/build-foafnaut.sh` and whitespace checks pass.

Without rebuilding the demos, the new validator also accepted outputs from
the existing cached compiled executables, run in a private directory:
8 node reports, 1880 primitives and 37608 storage floats. The exported SVG SHA256
was `335e03372bd4f0d233d6414ee8eb4c4ffbef572cc58f071264a93536850ce313`.
Evidence is in `/private/tmp/foafnaut-packaging-policy-check/`; control logs are
`/private/tmp/foafnaut-release-{before,after}.log`.

A complete new package build and CI remain coordinator-owned. No Lean source,
fixture, exclusion, workflow, release pointer or GPU test was changed or run.
