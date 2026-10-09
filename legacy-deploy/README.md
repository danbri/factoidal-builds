# Deployment files moved from danbri/factoidal (inactive)

`Dockerfile`, `.dockerignore`, `fly.toml`, `serve-lifesci-demo.sh`,
`deploy/` and `experiments/` from `danbri/factoidal` at `36f84a0c4969`.
They deploy the F\* HTTP server (`factoidal-http`) to Fly.io and serve the
life-science demo. They assume the old single repository (binaries under
`bin/linux-x86_64/`, repository root as build context). Porting them needs a
build context made of a factoidal-core checkout plus an installed
`linux-x86_64` release (`tools/fetch-builds.sh`), and a `FLY_API_TOKEN`
secret here. See `legacy-workflows/README.md` for `fly-deploy.yml`.
