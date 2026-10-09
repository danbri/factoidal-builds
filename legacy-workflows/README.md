# Workflows moved from danbri/factoidal (inactive)

These eleven workflows built, tested, published or deployed binaries in the
single `danbri/factoidal` repository. The 2026-10-09 split moved build work
here (`docs/designissues/2026-10-09-core-builds-split.md` in
`danbri/factoidal-core`). They are kept here as files, NOT under
`.github/workflows/`, so they do not run: each still assumes the old layout
(binaries committed under `bin/<platform>/`, a push back to `claude/main`).

| Workflow | Replaced by / what porting needs |
|---|---|
| `w3c-tests.yml` | `.github/workflows/build.yml` (build, gates, releases) |
| `beyond-w3c.yml`, `conformance-rerun.yml`, `dashboard-refresh.yml` | the `build-ocaml.sh test` step and the Lean scoreboard in `build.yml`; the dashboard now ships in the `web` release |
| `npm-publish.yml`, `npm-publish-lean.yml` | port needs an owner step on npmjs.com: the trusted publisher must name repository `factoidal-builds` and this workflow file |
| `deploy-pages.yml` | port needs a decision on where the site is served from (Pages of this repository, or of `danbri/factoidal`) |
| `fly-deploy.yml` | port needs a `FLY_API_TOKEN` secret in this repository |
| `ukparliament-bench.yml` (+ `ukparliament_bench_diff.py`) | port: run against a release instead of committed binaries |
| `clean-room-build.yml`, `debug-bytecode-build.yml` | port: check out factoidal-core instead of this repository |
