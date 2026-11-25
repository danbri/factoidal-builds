"""Materialize the locked replay source and its exact font files without Git."""
import concurrent.futures
import hashlib
from pathlib import Path
import re
import sys
from urllib.parse import quote
from urllib.request import urlopen

sha, lock_arg, out_arg = sys.argv[1:]
assert re.fullmatch(r"[a-f0-9]{40}", sha)
lock = Path(lock_arg)
out = Path(out_arg)
base = f"https://raw.githubusercontent.com/danbri/factoidal-core/{sha}/"


def fetch(record):
    expected, name = record.split("  ", 1)
    relative = Path(name)
    assert not relative.is_absolute() and ".." not in relative.parts, name
    target = out / relative
    if target.exists():
        contents = target.read_bytes()
    else:
        with urlopen(base + quote(name), timeout=40) as response:
            contents = response.read()
    digest = hashlib.sha256(contents).hexdigest()
    assert digest == expected, (name, digest, expected)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(contents)


records = lock.read_text().splitlines()
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    list(pool.map(fetch, records))
print(f"Verified {len(records)} pinned source and font files")
