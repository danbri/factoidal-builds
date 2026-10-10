# Build requests

`build.txt` names the factoidal-core commit to build. A push to `main` that
changes it starts `.github/workflows/build.yml` for that exact commit
(`scripts/resolve-core.sh` reads the first line that is not a comment).

Why this file exists: scheduled runs of the workflow have not started in this
repository (0 scheduled runs since it was created on 2026-10-09, with the
cron set first to four times a day and then hourly), and a push to
danbri/factoidal-core cannot start a workflow here without a cross-repository
token, which only the owner can create. Each change to `build.txt` is
therefore a request with its own history: which core commit was asked for,
and when.

Format: one 40-hex commit of danbri/factoidal-core, optionally followed by
the branch name; lines starting with `#` are comments.

To start builds from core pushes instead: add a fine-grained token with
`actions:write` on danbri/factoidal-builds as a secret in factoidal-core,
and a core workflow that calls this workflow's `workflow_dispatch`.
