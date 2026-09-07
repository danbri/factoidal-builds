# factoidal-builds

Compiled artifacts for [danbri/factoidal](https://github.com/danbri/factoidal).
Nothing here is source, and nothing here is edited by hand. Each
successful `W3C Test Suite` run on the source repository's `claude/main`
publishes one release per platform, tagged
`build-<12-hex source commit>-<platform>`, carrying
`factoidal-bin-<platform>.tar.gz` (the whole `bin/<platform>` set:
`factoidal`, `w3c_runner` and the per-suite runners) and
`build-info.json` (the source commit, the F\*, OCaml and opam versions
of the build, and a sha256 and size for every file). The git history of
this repository holds only `latest/<platform>.json`, one small pointer
file per platform, so a clone stays a few megabytes however many builds
accumulate.

To use a build, run `tools/fetch-builds.sh` inside a checkout of the
source repository: it finds the newest release matching that checkout's
history, verifies the payload against `build-info.json`, and installs it
into `bin/<platform>/`. `tools/ensure-test-env.sh` calls it, so the
usual entry point is that script. Downloading a release by hand works
too — the tarball unpacks straight into `bin/<platform>/` — but then the
sha256 check is yours to run.

Old releases may be deleted at any time; they are reproducible from the
source commit named in `build-info.json`.
