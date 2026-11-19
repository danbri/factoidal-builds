#!/usr/bin/env python3
"""Bind the portable browser engines to the receipts of an existing desktop release."""
import argparse
import hashlib
import json
from pathlib import Path
import re


X86_SET = "foafnaut-browser-linux-x86_64"
ENGINE_FILES = (
    "engines/render-plan.mjs", "engines/render-plan.wasm",
    "web-render/engines/web-render.mjs", "web-render/engines/web-render.wasm",
)


def digest(path):
    with path.open("rb") as stream:
        h = hashlib.sha256()
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
        return h.hexdigest()


def verify(build, receipt, commit, repository, run_id):
    if not re.fullmatch(r"[0-9a-f]{40}", commit) or not re.fullmatch(r"[1-9][0-9]*", run_id):
        raise ValueError("An exact source commit and engine run ID are required")
    if (receipt["set"] != X86_SET or receipt["source_repo"] != "danbri/factoidal-core"
            or receipt["source_commit"] != commit
            or receipt["run_url"] != f"https://github.com/{repository}/actions/runs/{run_id}"):
        raise ValueError("The published desktop release identifies different inputs")
    if (build / "web-render/engines/libweb-render.so").exists():
        raise ValueError("The portable engine artifact contains a native worker")
    # Match the exact path order and sha256sum format of core's build-linux-browser.sh.
    inventory = "".join(f"{digest(build / path)}  {path}\n" for path in ENGINE_FILES).encode()
    checks = {"engine-SHA256SUMS": hashlib.sha256(inventory).hexdigest(),
              "source-SHA256SUMS": digest(build / "source-SHA256SUMS"),
              "tool-versions.txt": digest(build / "tool-versions.txt")}
    files = receipt["artifacts"][X86_SET + ".tar.gz"]["files"]
    for name, actual in checks.items():
        if actual != files["foafnaut-linux-x86_64/" + name]["sha256"]:
            raise ValueError(f"{name} differs from the published desktop browser")
    return checks


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("build", type=Path)
    p.add_argument("receipt", type=Path)
    p.add_argument("commit")
    p.add_argument("repository")
    p.add_argument("run_id")
    args = p.parse_args()
    print(json.dumps(verify(args.build, json.loads(args.receipt.read_text()), args.commit,
                            args.repository, args.run_id), sort_keys=True))
