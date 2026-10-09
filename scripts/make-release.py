#!/usr/bin/env python3
"""Pack one artifact set and write its build-info.json.

Usage: make-release.py STAGE_DIR SET CORE_SHA CORE_REF OUT_DIR [TOOLCHAINS_JSON...]

STAGE_DIR holds repository-relative files (bin/<platform>/..., npm/...,
docs/...). Writes OUT_DIR/<SET>.tar.gz and OUT_DIR/build-info.json:

{
  "source_repo": "danbri/factoidal-core",
  "source_commit": "<40 hex>", "source_ref": "...",
  "set": "<SET>", "built_at": "...", "run_url": "...",
  "toolchains": {...merged from TOOLCHAINS_JSON files...},
  "artifacts": {"<SET>.tar.gz": {"sha256": "...", "size": N,
      "files": {"<path>": {"sha256": "...", "size": N, "mode": "755"}}}}
}

tools/fetch-builds.sh in core verifies the tarball digest, every listed
file, and that no unlisted file is present, before installing anything.
The tarball is deterministic for a given file set (sorted names, fixed
mtime, uid/gid 0), so two builds of the same bytes give the same digest.
"""
import datetime, hashlib, io, json, os, sys, tarfile, gzip

stage, set_name, sha, ref, out = sys.argv[1:6]
tool_files = sys.argv[6:]

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()

files = {}
paths = []
for dp, dns, fns in os.walk(stage):
    dns.sort()
    for fn in sorted(fns):
        p = os.path.join(dp, fn)
        if os.path.islink(p):
            continue
        rel = os.path.relpath(p, stage)
        st = os.stat(p)
        files[rel] = {'sha256': sha256(p), 'size': st.st_size,
                      'mode': oct(st.st_mode & 0o777)[2:]}
        paths.append(rel)
if not paths:
    sys.exit(f'make-release: {stage} is empty')
paths.sort()

os.makedirs(out, exist_ok=True)
tar_path = os.path.join(out, f'{set_name}.tar.gz')
raw = io.BytesIO()
with tarfile.open(fileobj=raw, mode='w', format=tarfile.PAX_FORMAT) as tf:
    for rel in paths:
        ti = tf.gettarinfo(os.path.join(stage, rel), arcname=rel)
        ti.uid = ti.gid = 0
        ti.uname = ti.gname = ''
        ti.mtime = 0
        with open(os.path.join(stage, rel), 'rb') as f:
            tf.addfile(ti, f)
with open(tar_path, 'wb') as f:
    with gzip.GzipFile(fileobj=f, mode='wb', mtime=0, compresslevel=9) as gz:
        gz.write(raw.getvalue())

toolchains = {}
for t in tool_files:
    if os.path.exists(t):
        toolchains.update(json.load(open(t)))

server = os.environ.get('GITHUB_SERVER_URL', 'https://github.com')
repo = os.environ.get('GITHUB_REPOSITORY', '')
run = os.environ.get('GITHUB_RUN_ID', '')
info = {
    'source_repo': os.environ.get('CORE_REPO', 'danbri/factoidal-core'),
    'source_commit': sha,
    'source_ref': ref,
    'set': set_name,
    'built_at': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    'run_url': f'{server}/{repo}/actions/runs/{run}' if run else '',
    'toolchains': toolchains,
    'artifacts': {
        f'{set_name}.tar.gz': {
            'sha256': sha256(tar_path),
            'size': os.path.getsize(tar_path),
            'files': files,
        }
    },
}
with open(os.path.join(out, 'build-info.json'), 'w') as f:
    json.dump(info, f, indent=1, sort_keys=True)
print(f'make-release: {set_name}: {len(paths)} files, '
      f'{os.path.getsize(tar_path) / 1e6:.1f} MB compressed', file=sys.stderr)
