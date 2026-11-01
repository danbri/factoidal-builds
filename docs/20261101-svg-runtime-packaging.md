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
