# OWL source and packed-artifact gates

Date: 2026-10-22. Draft; depends on
[factoidal-core PR #2](https://github.com/danbri/factoidal-core/pull/2),
branch `claude/owl-checked-consistency-review`.
Do not merge this workflow before the required core tools are available in
the source revision selected for a build. Missing tools intentionally fail.
This change does not request a build dispatch, merge or publication.

The Linux native job runs durable parser/resource-failure controls, 45 reader
cases with seven production proof mutations, the W3C restricted-reader
measurement, and 20 actual-public-producer cases with three proof mutations.
Source reports are uploaded even when a gate fails. The W3C run's unsupported
and unknown counts remain separate: no wrong verdict observed is not a
conformance or completeness pass.

The web gate downloads that build's source case report, packs the npm package
after installing the built Wasm, extracts it, records the tarball SHA-256,
and runs the public consistency checks on the unpacked artifact. It also
tests the runner itself against a synthetic baseline, a generic exception
without an ABI envelope and a synchronous hang that traps SIGTERM. The
runner uses SIGKILL; the control has a separate outer deadline. Synthetic
package controls are not engine conformance evidence.

The existing npm suite is retained unchanged. Failures propagate: no
continue-on-error or expected-failure conversion is added. Reports and pack
metadata are uploaded with always(). Web publication already requires the
successful web-gates artifact in scripts/publish.sh; that requirement remains.
Other artifact sets retain their existing independent completeness rules.
The separate npm-publish workflow is not modified by this PR.

Validation: both workflow YAML files and all 11 changed/related shell snippets
parse locally; the embedded Python pack step compiles. Core's actual source,
packed-artifact and runner-control results are preserved in its
`docs/audits/owl-assurance-20261022/` directory. There has been no remote run
of these workflow edits. Local checks do not establish remote enforcement.

The core proposal remains a draft: its restricted consistency path reduces
coverage, four broader OWL regression expectations still fail, and the broad
50-case artifact audit is not green. These gates must not be described as
approval of a release, complete OWL, or the separate legacy entailment API.
