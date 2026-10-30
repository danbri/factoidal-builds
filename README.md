# factoidal-builds

Builds and compiled artifacts for Factoidal. The source is
[danbri/factoidal-core](https://github.com/danbri/factoidal-core): the F\*
tree (`formal/fstar`), the Lean 4 tree (`formal/lean4`) and the experimental
graphics lab (`labs/demos/foafnaut`). This repository owns build automation
and generated releases; application source stays in factoidal-core.

## What runs

`.github/workflows/build.yml` builds one factoidal-core commit (default
branch `main`, else `claude/core-split`) on manual dispatch, on a push here
that changes `requests/build.txt` (that commit; see `requests/README.md`) or
the build scripts, and on an hourly schedule. A commit counts as
built only when all required sets have a release (the three core sets,
plus Foafnaut when that commit contains the lab); a scheduled run retries a
partly built commit at most once in 24 hours (`scripts/resolve-core.sh`).
Releases are published only for commits on core `main`; a build of any
other commit runs the gates and publishes nothing. Jobs and their gates:

| Job | Builds | Gates (a failure means no artifact, so no release) |
|---|---|---|
| `lean` (Linux, macOS arm64) | full `lake build`; `l4factoidal`, `l4w3c`, `l4wasm-cli` | every theorem and `#guard`, the HACL\* extern probe, the dispatch and CLI smoke scripts; Linux also the tail-recursion audit and `tests/dataflow/run.sh`. The Lean conformance scoreboard (Linux) is a measurement, not a gate |
| `lean-wasm` (Linux) | `Wasm/build-wasm.sh` with Emscripten 6.0.8 | the build itself and its check that the wasm copies agree. It runs no tests: the npm tests run in `web-gates` |
| `fstar` (Linux), `fstar-macos` | `build-ocaml.sh extract`, `compile`; Linux also `js`, `wasm`, `npm` | the re-extracted `.ml` equal core's committed `.ml`; Linux runs `build-ocaml.sh test` (W3C suites, dashboard) |
| `web-gates` (Linux) | nothing; installs the `fstar` web products and the `lean-wasm` module into one checkout | `npm test` in `npm/factoidal` (Node 22), with no skipped test; `tests/engine-compare/run.sh`; `tests/known-defects/run.sh`. The `l4diff` differential is a measurement, not a gate |
| `foafnaut-engines` (Linux, when present) | small Lean WASM engines with the shared runtime cache, including the RDF-driven graph when present | portable engine tests, C coordinate tests, pinned SVG fixture integrity and runner tests |
| `foafnaut` (macOS arm64) | three Deno-compiled graphics executables, Cocoa sidecar, launchers and SVG fixtures | requires the Lean gates and engines job; repeats portable tests, relocates the package, checks all compiled CPU engines and native library loading. No GPU/window or SVG visual pass is inferred |
| `publish` | packs each complete set | a set whose jobs did not all pass is not published, and the run is red; the `web` set also needs `web-gates` |

## Releases

One release per (core commit, set), tagged `build-<12 hex core commit>-<set>`:

| Set | Content (paths relative to a core checkout) |
|---|---|
| `linux-x86_64`, `darwin-arm64` | `bin/<platform>/`: the F\* CLI, HTTP server and suite runners, and the Lean CLI `l4factoidal`, `l4w3c`, `l4wasm-cli` |
| `web` | F\* JS and wasm bundles (`docs/fstar-extracted/`, `npm/factoidal/`), the Lean wasm module (`docs/web/hub/assets/l4/`, `npm/factoidal/l4-assets/`, `npm/factoidal-lean/`), the generated F\* dashboard (`docs/test-results/`), and the Lean scoreboard (`lean-scoreboard.json`, `.txt`) |
| `foafnaut-darwin-arm64` (when present) | `foafnaut/`: native UI (springs, layout, vectors, and the RDF-driven FOAFNaut browser when present), Lean-generated still renderer, SVG subset renderer, Cocoa sidecar, `.command` launchers, sample SVGs and source/toolchain provenance |

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
Binaries are currently unsigned, macOS ARM64 only.

Foafnaut is built automatically for each resolved core commit containing
`labs/demos/foafnaut/build-engines.sh`, through the same dispatch/request/poll
process as the core sets. It gets tag `build-<12 hex>-foafnaut-darwin-arm64`
and `latest/foafnaut-darwin-arm64.json`. An API failure checking source
availability fails the resolver; it does not silently skip the demo gates.
Old core commits keep their three-set requirement. A failed demo job withholds
that set and marks the run red; passing core sets can still publish. Only core
main commits publish; PR builds remain validation only.

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

A forced rebuild never replaces a `web` release that a published
`@factoidal/core` version names (`scripts/npm-names-release.py` reads each
version's `l4-assets/version.json`); the run keeps the old release and is
red.

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
`tools/install-toolchain-cache.sh` and by `build.yml`.

Old releases may be deleted at any time; they are reproducible from the
source commit named in `build-info.json`.
