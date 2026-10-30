#!/usr/bin/env python3
"""Print true/false for a file at an exact core commit; API failures fail closed.

Walk small, non-recursive Git trees instead of mistaking a failed contents
request for an old core commit without the optional lab.
"""
import json
import subprocess
import sys


def has_path(repo, revision, path, fetch):
    parts = path.split("/")
    for index, part in enumerate(parts):
        tree = fetch(f"repos/{repo}/git/trees/{revision}")
        if tree.get("truncated"):
            raise ValueError("Git tree response is truncated")
        entry = next((e for e in tree["tree"] if e["path"] == part), None)
        if entry is None:
            return False
        if index == len(parts) - 1:
            return entry["type"] == "blob" and entry["mode"] in ("100644", "100755")
        if entry["type"] != "tree":
            return False
        revision = entry["sha"]
    return False


def fetch(endpoint):
    result = subprocess.run(["gh", "api", endpoint], check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


if __name__ == "__main__":
    try:
        print(str(has_path(*sys.argv[1:4], fetch)).lower())
    except (subprocess.CalledProcessError, ValueError, KeyError, TypeError) as error:
        sys.exit(f"Cannot determine core file availability: {error}")
