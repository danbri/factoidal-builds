# factoidal-builds

Builds and compiled artifacts for Factoidal. The source is
[danbri/factoidal-core](https://github.com/danbri/factoidal-core): the Lean 4
tree (`formal/lean4`) and the Foafnaut lab (`labs/demos/foafnaut`). The project
is Lean first: since 2026-11-15 no F\* build, test or release product runs
here (the F\* sources stay in core, and its F\* workflows run only by hand).
This repository owns build automation
and generated releases; application source stays in factoidal-core.

## What runs

`.github/workflows/build.yml` builds one factoidal-core commit (default
branch `main`, else `claude/core-split`) on manual dispatch, on a push here
that changes `requests/build.txt` (that commit; see `requests/README.md`) or
the build scripts, and on an hourly schedule. A commit counts as
built only when all required sets have a release (the three core sets and
the Foafnaut sets supported by that commit); a scheduled run retries a
partly built commit at most once in 24 hours (`scripts/resolve-core.sh`).
Releases are published only for commits on core `main`; a build of any
other commit runs the gates and publishes nothing. Jobs and their gates:

| Job | Builds | Gates (a failure means no artifact, so no release) |
|---|---|---|
| `lean` (Linux), `lean-macos` (macOS arm64; two jobs so no Linux job waits for a macOS runner) | full `lake build`; `l4factoidal`, `l4w3c`, `l4wasm-cli` | every theorem and `#guard`, the HACL\* extern probe, the dispatch and CLI smoke scripts; Linux also the tail-recursion audit and `tests/dataflow/run.sh`. The Lean conformance scoreboard (Linux) is a measurement, not a gate |
| `lean-wasm` (Linux) | `Wasm/build-wasm.sh` with Emscripten 6.0.8 | the build itself and its check that the wasm copies agree. It runs no tests: the npm tests run in `web-gates` |
| `web-gates` (Linux) | nothing; installs the `lean-wasm` module into a checkout | `npm test` in `npm/factoidal` (Node 22), with no skipped test; the OWL package checks; the Touchstone LWS client lab |
| `foafnaut-engines` (Linux, when present) | small Lean WASM engines with the shared runtime cache, including the RDF-driven graph when present | portable engine tests, C coordinate tests, pinned SVG fixture integrity and runner tests; packages a browser runtime only from these fresh tested engines |
| `foafnaut-browser-linux` and `foafnaut-browser-linux-check` (Ubuntu 24.04 x86_64, when present) | downloadable Foafnaut browser executable, SDL window library and embedded Lean WASM engines | separate runner verifies and extracts the actual archive, launches it in Xvfb with Mesa software Vulkan, and checks rendered HTML, pointer and keyboard navigation, live HTTPS, resize and close |
| `foafnaut` (macOS arm64) | three Deno-compiled graphics executables, Cocoa sidecar, launchers and SVG fixtures | requires the Lean gates and engines job; repeats portable tests, relocates the package, checks all compiled CPU engines and native library loading. No GPU/window or SVG visual pass is inferred |
| `publish`, `publish-linux-browser`, `publish-macos` | publish each independently gated set | `web` needs `web-gates`; the Linux browser needs the Linux Lean gates, Foafnaut host tests and the window check for the exact archive |
| `foafnaut-host-tests` (Linux) | nothing; core's `labs/demos/foafnaut/test.sh --skip-build` on the `foafnaut-engines` artifact | every check runs and all failures are listed; gates `foafnaut-web`. The first test result of a run |
| `metrics` (Linux) | the run's timing and cache record (`scripts/ci-metrics.py`) | none: a table in the run summary, artifact `ci-metrics`, and a row per job on the branch `ci-metrics` |

### Caches, cold builds, timing records

Each cache, its key, why a hit is correct and how to read hits in the logs is in core's
[`skills/foafnaut/ci-caching.md`](https://github.com/danbri/factoidal-core/blob/main/skills/foafnaut/ci-caching.md).
In short: `.lake` (Lake rebuilds what changed), an Emscripten ccache in `foafnaut-engines`, and
the leanc object cache (`release-tests/leanc-cache.sh`) in the macOS bundle job. After each
build, `scripts/cache-audit.sh` compiles a random sample again with no cache and fails the job if
an object differs; `tests/test_cache_keys.py` checks that each key changes with its inputs.
Dispatch with `cold=true` for a build that restores no cache. The trend of the last runs:
`python3 scripts/ci-metrics.py trend --n 10 --records <checkout of branch ci-metrics>`.

## Releases

One release per (core commit, set), tagged `build-<12 hex core commit>-<set>`:

| Set | Content (paths relative to a core checkout) |
|---|---|
| `linux-x86_64`, `darwin-arm64` | `bin/<platform>/`: the Lean CLI `l4factoidal`, `l4w3c`, `l4wasm-cli` |
| `web` | the Lean wasm module (`docs/web/hub/assets/l4/`, `npm/factoidal/l4-assets/`, `npm/factoidal-lean/`) and the Lean scoreboard (`lean-scoreboard.json`, `.txt`) |
| `foafnaut-darwin-arm64` (when present) | `foafnaut/`: native UI (springs, layout, vectors, and the RDF-driven FOAFNaut browser when present), Lean-generated still renderer, SVG subset renderer, Cocoa sidecar, `.command` launchers, sample SVGs and source/toolchain provenance |
| `foafnaut-browser-linux-x86_64` (when present) | `foafnaut-linux-x86_64/`: the windowed HTML browser, Linux SDL library, runtime instructions and source/toolchain provenance |
| `foafnaut-browser-linux-arm64` (on request) | `foafnaut-linux-arm64/` contains the AArch64 desktop browser, SDL window library and portable document worker |
| `foafnaut-web` (when the SVG hub page and `SVGStroke.lean` are present) | `docs/web/hub/svg-webgpu/runtime/`: Lean-generated SVG and render-plan WASM plus minimal JS host adapters |

Each release carries `<set>.tar.gz` (deterministic: sorted, mtime 0) and
`build-info.json` (source commit, toolchain versions, run URL, sha256 and
size of every file). In a factoidal-core checkout, `tools/fetch-builds.sh`
picks the newest release whose commit is in your history, checks the
tarball digest and every file, and installs it; `tools/ensure-test-env.sh`
calls it.

The separate Foafnaut archive is extracted into any writable directory;
it is not installed by `tools/fetch-builds.sh`. Open
`foafnaut/Native Demos.command`, `foafnaut/FOAFNaut.command` (when included), or
`foafnaut/SVG Demo.command`. The executables
include Deno and Lean WASM, so users need no Node, Deno or Lean installation.
The UI executable requires its adjacent `libnative-window.dylib` and a macOS
desktop session. Launchers change into their own directory for relative
file permissions. The current UI compiles with FFI permission granted at the
owner's request, so the native surface does not prompt on every launch.
The macOS demo binaries are unsigned and target ARM64.

The Linux browser release tag is `build-<12 hex>-foafnaut-browser-linux-x86_64`
and `latest/foafnaut-browser-linux-x86_64.json` points to the newest published
commit. Extract `foafnaut-browser-linux-x86_64.tar.gz`, then run
`./foafnaut-linux-x86_64/foafnaut` from a Linux desktop session. The bundled
README lists system libraries. Deno and the Lean WASM engines are embedded.
`window-smoke.json` records the result and SHA-256 of the checked archive.
The GUI evidence comes from Ubuntu 24.04 x86_64 using an X11 display and Mesa
software Vulkan. For a branch build, use the download link in the passing
`foafnaut-browser-linux-check` job summary. That run also has the
`foafnaut-browser-linux-evidence` artifact with screenshots and the browser log.

The **Foafnaut Linux ARM64 desktop browser** workflow builds the same core revision and portable
engines as a published x86_64 desktop browser. Supply its full core SHA, or leave it empty for the
latest published x86_64 browser. The original `foafnaut-engines` Actions artifact has a seven-day
retention period. A pull request can pin its test to a published desktop release by putting
`Desktop source: <full lowercase core SHA>` on a line of its description.
The workflow checks the engine bytes against the published x86_64 release,
compiles the browser on Ubuntu ARM64 and launches the extracted archive on a second ARM64 runner.
A manual run on main publishes the exact archive that passed the X11 window test. The separate
`foafnaut-linux-arm64` release contains the headless engine library. [ARM64 desktop launch instructions](docs/linux-arm64-browser.md)

The ARM64 browser archive for core `7d4794f49f5d` is 60,225,931 bytes. Its SHA-256 is
`353cd1219cd8a5baf369aea9323412dada694b4cc2d8f885f1ff4f02dd1d1809`. The native X11 release test
verified the first page 66.067 seconds after launch and the clicked page 0.595 seconds later.
[Download the ARM64 browser](https://github.com/danbri/factoidal-builds/releases/download/build-7d4794f49f5d-foafnaut-browser-linux-arm64/foafnaut-browser-linux-arm64.tar.gz) · [Build provenance](https://github.com/danbri/factoidal-builds/releases/download/build-7d4794f49f5d-foafnaut-browser-linux-arm64/build-info.json) · [Window test receipt](https://github.com/danbri/factoidal-builds/releases/download/build-7d4794f49f5d-foafnaut-browser-linux-arm64/window-smoke.json)

Foafnaut is built automatically for each resolved core commit containing
`labs/demos/foafnaut/build-engines.sh`, through the same dispatch/request/poll
process as the core sets. It gets tag `build-<12 hex>-foafnaut-darwin-arm64`
and `latest/foafnaut-darwin-arm64.json`. An API failure checking source
availability fails the resolver; it does not silently skip the demo gates.
The Linux browser joins the required sets when the core commit contains
`labs/demos/foafnaut/build-linux-browser.sh`. The resolver also requires the
matching window check and engine build sources. A failed demo job withholds
that set and marks the run red; passing core sets can still publish. Only core
main commits publish; PR builds remain validation only.

When the same core commit contains `docs/web/hub/svg-webgpu/index.njk` and
`labs/demos/foafnaut/SVGStroke.lean`, the Linux engine job uploads the
`foafnaut-web` release candidate. This set
contains only the SVG browser runtime under
`docs/web/hub/svg-webgpu/runtime/`; the page, CSS and fixtures stay in
factoidal-core. `publish.sh` checks that the exact core commit is on core
`main`, verifies all runtime files, and records the release build-run URL
before creating the release. The package evidence records a fresh Lean/WASM
build and named source tests, not SVG conformance or GPU correctness. This set
is independent of the native macOS graphics package.

The GPU checks and official SVG visual comparisons require a real GPU run.
The source lab documents its supported SVG profile and the pinned WPT runner;
fixture integrity and CPU acceptance are not SVG conformance. The build uses
Deno 2.9.4 and Emscripten 6.0.8; only the small engines cross jobs, not generated
C, object files or the runtime cache. No demo binary is committed to git.

For cores containing `PolicyBridge.lean`, the relocation smoke also exports a
checked FOAFNaut SVG and its policy report, then passes that exact SVG to the
relocated native SVG executable. The gate requires a valid read-only-storage
artifact, validated application/configuration bounds, accepted nonempty node
reports and the shipped browser policy demo, engines and RDF fixture. These
are CPU/package checks; GPU output and browser execution remain untested here.
Older cores without PolicyBridge keep the existing smoke path. Details:
[checked policy packaging](docs/20261030-foafnaut-policy-packaging.md).

`python3 -m unittest discover -s tests -v` checks release selection, refusal
on missing gates/API errors, main-only publication and archive provenance
with fake GitHub/git commands. `check-scripts.yml` runs those controls on PRs.

## Release tests (full WPT and conformance suites)

`.github/workflows/release-tests.yml` (code: `release-tests/release-tests.py`) runs the
full Web Platform Tests (every name Chrome runs at the WPT commit, no sampling) and the
other conformance suites against released binaries; it builds nothing.

- After each `build.yml` run that publishes releases: macOS WPT (4 shards) and the
  suites. After each `foafnaut-linux.yml` run: Linux WPT (16 shards).
- Four times a day (01:41, 07:41, 13:41, 19:41 UTC): the newest complete release on
  macOS and Linux, also when nothing changed (`repeat_of`). A new aligned WPT
  commit on wpt.fyi makes the trigger `browser-release` and records the other browsers.
- Manual: `gh workflow run release-tests.yml -f release=build-<sha12> -f wpt_commit=<40 hex>`.

Results are on the branch `wpt-scores`: `runs.csv` (one row per run and suite; only
`valid=true`, `kind=full` rows are scores), `rivals.csv`, `differential.csv` (QuickJS,
never a score), `runs/<run_id>/meta.json`; full WPT results are assets of the release
`test-results` (do not delete it). Columns and validity rules: `README.md` on that
branch. `wpt-score.yml` (sampled) is retired: manual smoke check only, nothing recorded.

`.github/workflows/foafnaut-linux.yml` builds the Linux engine library
(`libweb-render.so`, x86_64 and arm64) after each `build.yml` run and publishes
`build-<sha12>-foafnaut-linux-<arch>`; it needs the pinned Lean toolchain at run time
(`foafnaut/README-linux.txt` in the archive).

## Real-page survey

`.github/workflows/realpages.yml` (helper `release-tests/realpages.py`; the survey is core's
`labs/demos/foafnaut/realpages/`, skill `skills/realpages-survey`) measures everyday pages
(Wikipedia desktop and mobile skins, BBC News, GitHub, MDN, a blog, Hacker News, a W3C spec,
core's Spinal Tap page) live on each Foafnaut release. It builds nothing.

- Starts after each run of `build.yml` (`foafnaut-darwin-arm64`), `foafnaut-macos.yml`
  (`foafnaut-engine-darwin-arm64`) and `foafnaut-linux.yml` (`foafnaut-linux-x86_64`, self-contained
  only) that published a release; by hand:
  `gh workflow run realpages.yml -f release=build-<12 hex>-foafnaut-darwin-arm64` (comma list for
  several; `survey_ref` picks the core ref of the survey tools, `only` a few pages).
- Twice on each platform: offline, every page replayed from its snapshot in
  [`third_party/realpages/`](third_party/realpages/README.md) (public pages vendored as fair use
  for testing, with URL, fetch time, header fields, licence and attribution; about 18.6 MB), the
  gate; and live, the pages as they are now, for drift (information only).
- macOS (`macos-15`): `run_html.ts` of the release's own core commit, off screen, on the release's
  library; GPU numbers, idle CPU, script turns, scroll latency, memory, liberal-mode skips, and the
  layout similarity against headless Chrome (the snapshot's picture offline, Chrome now live).
  Linux: Textnaut on the `.so` (load, layout, CPU, memory).
- Results: the job summary (tables with changes against the survey of the previous release, and
  regressions); release assets `realpages-<platform>-<mode>.json` and `.md`; `realpages/trend.csv`,
  `realpages/runs/<run_id>/` and `realpages/latest-|previous-<platform>-<mode>.json` on the branch
  `wpt-scores`. Pictures and logs of each run: artifact `realpages-<platform>-pictures`, 7 days.
- A crash or exit of the browser on a snapshot fails the job; a worse verdict, a number over 1.5
  times the previous one (above a noise floor) or a drop in layout similarity is a warning; an
  unreachable live page is neither.
- Cost: macOS about 40-60 min a release, Linux about 10 min.

## Single-file executables (`exe` set)

`.github/workflows/exe.yml` builds the `factoidal` CLI as one executable file
per platform with `deno compile` (Linux, macOS and Windows on x86_64 and
arm64; the engine wasm included), from the `web` release of a core commit.
It uses core's `tools/build-exe.sh` and `tools/check-exe.sh` at that commit,
so commits without them are skipped. It runs after each successful
`build.yml` run (the commit of `latest/web.json`) and on manual dispatch
(`core_ref`, `force`). Gates: `tools/check-exe.sh` on Linux x86_64 and macOS
arm64 (help, version, a store and a query, `serve` over HTTP, the desktop
WebDAV harness) and on Windows x86_64 with `--quick` (no WebDAV harness).
Release `build-<12 hex>-exe` carries the six files, `SHA256SUMS`,
`exe.tar.gz` and `build-info.json`; `latest/exe.json` points to it. Only
commits on core `main` are published. The files are not signed. Design:
core `docs/designissues/2026-10-28-single-file-app.md`.

## Publishing to npm

`.github/workflows/npm-publish.yml` publishes `@factoidal/core` from a `web`
release, by trusted publishing (OIDC, no token). Manual dispatch only:

```bash
gh workflow run npm-publish.yml --repo danbri/factoidal-builds \
  -f core_ref=<40-hex core commit; required> \
  -f dist_tag=next -f confirm=<version in npm/factoidal/package.json>
```

It refuses a release whose build run's `web-gates` job did not succeed,
installs the release into a core checkout with `tools/fetch-builds.sh`
(sha256 of every file checked), requires `confirm` to equal the package
version and the version to be new on npmjs.com, runs core's
`tools/npm-release-check.mjs` (the version agrees in `package.json`,
`package-lock.json` and `lib/version.mjs`, and `CHANGELOG.md` has a dated
heading for it), sets `repository.url` to
this repository in the packed copy (npm provenance requires it), packs with
`--ignore-scripts`, and refuses a tarball that holds an F\* bundle (`jsoo`,
`ocaml`, `npm-entry`, `hacl-wasm`), lacks `l4-assets/l4factoidal.wasm`, or
whose `l4-assets/version.json` is not stamped with that wasm's sha256 and
the release commit. Since 0.10.0 the package ships no
`l4factoidal-core.wasm`. The package's `prepublishOnly` (`npm test`) does
not run: the pack step skips scripts, and `npm publish` of a tarball runs
none. The suite gate is the `web-gates` job of the build run. The tarball
is a workflow artifact. Use `dist_tag=latest` only to make the version the
default install.

A release is never replaced. A rebuild of a commit (a retry for a missing
set, or `force`) publishes only the sets that have no release yet and keeps
the others as they were published: consumers pin a release by tag and by
the sha256 of its tarball (`@factoidal/core`'s `l4-assets/version.json`,
Textnaut's `foafnaut-web` pin), and a rebuild never has the same bytes. To
replace a bad release, delete it by hand first.
(`scripts/npm-names-release.py` reports which npm versions name a release.)

One-time owner step on npmjs.com before the first run: package
`@factoidal/core` → Settings → Trusted Publisher → GitHub Actions, with
organization `danbri`, repository `factoidal-builds`, workflow filename
`npm-publish.yml`, environment blank, allowed action `npm publish`. After
this change, the old workflow in `danbri/factoidal` can no longer publish.

## Git history here

`main` holds only the workflow, `scripts/`, `legacy-workflows/` (the eleven
workflows moved from `danbri/factoidal`, inactive, with what each needs to be
ported), and `latest/<set>.json` pointers written by the `publish` job.
`toolchain-cache` (F\* binary chunks, KaRaMeL, the Lean wasm work dir) and
`checked-cache` (F\* `.checked` files) are orphan branches read by core's
`tools/install-toolchain-cache.sh`; `build.yml` reads only the Lean wasm work dir
from `toolchain-cache` (the F\* parts are no longer used by any workflow here).

Old releases may be deleted at any time; they are reproducible from the
source commit named in `build-info.json`.

### Lean HTML/CSS browser runtime

When the pinned core includes `docs/web/hub/html-webgpu/index.njk`, the optional
`foafnaut-web` set also builds the targeted Lean HTML/CSS renderer and checks its
actual WASM ABI, deterministic artifacts, reference probes and link picker.
`package-html-runtime.mjs` validates the committed Lean import closure, generated
C and engine hashes before staging the seven runtime files and a manifest.
The reviewed `WebDocument` initializer includes the transitive Lean script
boundary and font request modules in that source witness. The seven-file
runtime remains the scene engine and GPU transport; it does not include the
local browser UI/server or QuickJS dependency.
Only the existing main-ancestry-gated publisher can finalize a development
manifest as a release. The public page uses relative worker/runtime URLs.
These checks establish build identity and named behavior, not full HTML/SVG
conformance, compiler correctness or native GPU presentation. The packager tests
use explicitly synthetic fixture modules; they do not count as rendering tests.

Tracking: https://github.com/danbri/factoidal/issues/1230 .

The capable macOS bundle also stages `lean-html-scene-darwin-arm64`, the actual
Lean native HTML/RDF scene and CPU-pixel CLI, its named source witness and input
fixtures. Clean native packaging installs the pinned Lean toolchain and rebuilds
the small source/proof closure; it does not require a warm developer checkout.
The relocated CLI is exercised on HTML and N-Triples before packaging. This is a
CPU/scene producer, and is explicitly documented separately from a GPU window.
When the source includes `WebDocument.lean`, the bundle also includes a small
document request JSON and checks the CLI's `--document` path after relocation.
Resource bytes and DOM commands must be supplied in that request; the CLI does
not fetch pages or execute scripts. The complete local browser MVP needs its
UI/server, QuickJS reactor and font broker in addition to this CLI.
Remote macOS candidate execution remains necessary before publishing a bundle.

Record: [document closure and native packaging](docs/20261103-html-document-runtime-packaging.md).
