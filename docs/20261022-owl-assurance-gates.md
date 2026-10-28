# OWL packed-artifact gates

First written 2026-10-22; revised 2026-10-28 (owner, 2026-10-28: "Yes" to
"make builds PR 1 ready to merge, keep only the packed-package steps").

The OWL source gates (reader contracts, the W3C restricted-reader
measurement, the public-producer boundary) run in core's own CI
(`danbri/factoidal-core` `.github/workflows/verify-lean4.yml`). This workflow
adds what core CI cannot check: the package that the build makes.

- Linux native job: `tools/check-owl-public-boundary.py` on the exact core
  commit built here. Its report (23 cases on 2026-10-28) is the case list for
  the web gate and is uploaded even when the gate fails.
- Web gate: after the built wasm is installed into the checkout, `npm pack`,
  extract, record the tarball SHA-256, then:
  - `tools/test-owl-public-artifact.mjs`: runner controls on a synthetic
    package (baseline, a generic exception with no ABI envelope, a
    synchronous hang that ignores SIGTERM and needs SIGKILL);
  - `tools/check-owl-public-artifact.mjs`: every case through the low-level
    op and the public `owlIsConsistent` of the unpacked package, each in a
    child process with a 15 s deadline. Known defects are expected failures
    with an issue; one that passes fails the run. On 2026-10-28:
    https://github.com/danbri/factoidal/issues/1118 (two RDF 1.2 cases).

Failures propagate: no continue-on-error. The existing npm suite is
unchanged; web publication still requires the web-gates job.

Merge order: the core tools needed the issue 960 verdicts
(https://github.com/danbri/factoidal/issues/960) and 23 cases; that repair is
https://github.com/danbri/factoidal-core/pull/178. Merge it first: with the
2026-10-22 tools both web steps stop before any case runs.

Older core commits: the merge order above covers new commits only. A build of
a core commit that does not contain PR 178 (merge `e655516c`) runs that
commit's 2026-10-22 tools, which stop before any case. The 0.20.0 commit
`0c9a222b` is such a commit, so after this workflow landed its web release
could not be made (run
https://github.com/danbri/factoidal-builds/actions/runs/40655703183 was
cancelled for this reason on 2026-10-28). The step "OWL package check tools
for this core commit" now asks the GitHub compare API whether the built
commit contains `e655516c`. If it does not, the two tools of `e655516c` run
and the step prints a warning; the case list still comes from the built
commit. Between `0c9a222b` and `e655516c` no OWL Lean module, OWL wasm op,
boundary tool or OWL part of `lib/api.mjs` changed.

Measured locally on 2026-10-28 (core `main` `ebc1b36a` plus the repair, the
packed 0.20.0 package): boundary gate 23 of 23 cases, 5 of 5 proof mutations
rejected; package check 23 pass, 0 fail (out of 23, 2 expected failures);
runner controls 3 pass, 0 fail (out of 3). No remote run of this workflow yet.
These gates check a restricted consistency API only; they are no claim of OWL
completeness or of the entailment API.
