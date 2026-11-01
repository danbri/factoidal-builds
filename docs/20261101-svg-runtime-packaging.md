# SVG browser runtime packaging

The development-only packager copies the four existing SVG/render-plan engine
assets, strips types from three existing host bridges and emits exact hashes
and sizes for all seven runtime files. It validates the requested source SHA,
tracked source bytes and required source inventory including SVGCSS.

Tests cover stale/incomplete inventories, wrong revisions, dirty source,
missing/invalid engines, symlinks, output replacement and import rewriting.
The script-check workflow runs these on Node22. No rendering or source-to-binary
correspondence is proved by packaging. Release mode intentionally refuses until
a fresh-build workflow provides the required build evidence. This patch neither
publishes the browser demo nor dispatches a release.

Updated the required closure for SVGDash after dashed-stroke support. Twelve
packaging tests pass, including separate missing-CSS and missing-dash-module
refusal tests. No runtime package was built or published by this check.

The paired dash value/unit implementation adds SVGDashUnits to that required
closure. Thirteen packaging tests now pass, including refusal when this module
is omitted. This guards the new source dependency; it does not establish fresh
binary correspondence or change the development-only release restriction.

## CI artifact integration

The `foafnaut-engines` job now packages the browser runtime after the fresh
engine build and its tests succeed. It installs Node 22 and passes the resolved
core SHA to the packager, then uploads `svg-browser-runtime-development` with
seven-day retention. A packaging failure fails this job; missing upload files
are errors. The package still says development and is not a release asset or
a published demo page. No release pointer or provenance qualification changes.

This step applies to core revisions containing SVGDashUnits, which marks the
source generation supported by the current required closure. Earlier revisions
retain their existing native build path and do not get this browser artifact.
This compatibility condition must not hide missing dependencies in a supported
revision: the packager still checks every required source and engine input.

Local validation parses the workflow YAML and checks build/test → package →
upload ordering. The packaging refusal tests and build-script tests are local
checks. The modified workflow has not run on GitHub yet; a download link exists
only after source/workflow integration and a successful CI run. Once available,
extract the artifact into the browser demo's configured runtime directory,
preserving `engines/` and `provenance.json`. It contains runtime assets, not the
HTML application or proof of visual conformance.
