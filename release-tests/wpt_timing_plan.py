"""Build and validate an opt-in Linux BubblePop WPT assignment."""
import gzip
import hashlib
import heapq
import json
from pathlib import Path

FORMAT = "factoidal-wpt-timing-plan-v1"
TIMING_FORMAT = "factoidal-wpt-timing-v1"
PLATFORM = "linux-x86_64"
ENGINE = "bubblepop"
SHARDS = 12
JOBS = 3
PLAN = "wpt-timing-plan.json"


def list_bytes(names):
    return ("\n".join(names) + "\n").encode() if names else b""


def digest(data):
    return hashlib.sha256(data).hexdigest()


def balance(names, weights, default):
    """Assign longest first with exact round-robin capacities and stable ties."""
    worker_count = SHARDS * JOBS
    workers = [[] for _ in range(worker_count)]
    capacities = [len(range(shard + worker * SHARDS, len(names), worker_count))
                  for shard in range(SHARDS) for worker in range(JOBS)]
    queue = [(0, 0, i) for i, count in enumerate(capacities) if count]
    heapq.heapify(queue)
    for name in sorted(names, key=lambda name: (-weights.get(name, default), name)):
        load, count, worker = heapq.heappop(queue)
        workers[worker].append(name)
        if count + 1 < capacities[worker]:
            heapq.heappush(queue, (load + weights.get(name, default), count + 1, worker))
    lists = []
    for shard in range(SHARDS):
        parts = [sorted(part) for part in workers[shard * JOBS:(shard + 1) * JOBS]]
        lists.append([part[i] for i in range(max(map(len, parts))) for part in parts if i < len(part)])
    return lists


def validate_lists(names, lists):
    if len(lists) != SHARDS or len(names) != len(set(names)):
        raise ValueError("invalid WPT shard or input name count")
    planned = [name for shard in lists for name in shard]
    if len(planned) != len(names) or set(planned) != set(names):
        raise ValueError("WPT plan must assign each input name exactly once")
    for i, shard in enumerate(lists):
        expected = names[i::SHARDS]
        for j in range(JOBS):
            worker = shard[j::JOBS]
            if len(worker) != len(expected[j::JOBS]) or worker != sorted(worker):
                raise ValueError(f"invalid WPT worker capacity or order in shard {i}, worker {j}")


def create(directory, timing_file, timing_sha, full_list_sha, wpt_commit):
    directory = Path(directory)
    source = Path(timing_file).read_bytes()
    if digest(source) != timing_sha:
        raise ValueError("WPT timing artifact SHA-256 mismatch")
    table = json.loads(gzip.decompress(source))
    if (table["format"], table["platform"], table["script_engine"]) != (TIMING_FORMAT, PLATFORM, ENGINE):
        raise ValueError("WPT timing artifact format, platform or engine mismatch")
    weights, default = table["weights_half_ms"], table["default_half_ms"]
    if not table["sources"] or type(default) is not int or default <= 0:
        raise ValueError("WPT timing artifact requires sources and a positive default")
    if any(type(weight) is not int or weight <= 0 for weight in weights.values()):
        raise ValueError("WPT estimated durations must be positive integers")
    raw = (directory / "full.list").read_bytes()
    if digest(raw) != full_list_sha:
        raise ValueError("WPT full.list SHA-256 mismatch")
    names = raw.decode().splitlines()
    lists = balance(names, weights, default)
    validate_lists(names, lists)
    checksums = []
    for i, shard in enumerate(lists):
        ordered = list_bytes(shard)
        (directory / f"wpt-timing-shard-{i}.list").write_bytes(ordered)
        checksums.append(digest(ordered))
    meta = {
        "format": FORMAT,
        "platform": PLATFORM,
        "script_engine": ENGINE,
        "shards": SHARDS,
        "jobs": JOBS,
        "wpt_commit": wpt_commit,
        "full_list_sha256": full_list_sha,
        "timing_sha256": timing_sha,
        "timing_sources": table["sources"],
        "default_half_ms": default,
        "names_without_timing": sum(name not in weights for name in names),
        "shard_sha256": checksums,
    }
    (directory / "wpt-timing-source.json.gz").write_bytes(source)
    (directory / PLAN).write_text(json.dumps(meta, indent=2) + "\n")
    return digest((directory / PLAN).read_bytes())


def load(directory, inputs, names, shards, jobs):
    directory = Path(directory)
    manifest = (directory / PLAN).read_bytes()
    if digest(manifest) != inputs["timing_plan_sha256"]:
        raise ValueError("WPT timing plan SHA-256 mismatch")
    meta = json.loads(manifest)
    context = (meta["format"], meta["platform"], meta["script_engine"], meta["shards"], meta["jobs"])
    if context != (FORMAT, PLATFORM, ENGINE, shards, jobs) or (shards, jobs) != (SHARDS, JOBS):
        raise ValueError("WPT timing plan requires 12 Linux BubblePop shards with 3 workers each")
    if (meta["wpt_commit"] != inputs["wpt_commit"] or meta["full_list_sha256"] != inputs["full_list_sha256"]
            or digest((directory / "full.list").read_bytes()) != inputs["full_list_sha256"]):
        raise ValueError("WPT timing plan input revision or full.list SHA-256 mismatch")
    checksums = meta["shard_sha256"]
    if len(checksums) != shards:
        raise ValueError("WPT timing plan shard SHA-256 count mismatch")
    lists = []
    for i, checksum in enumerate(checksums):
        ordered = (directory / f"wpt-timing-shard-{i}.list").read_bytes()
        if digest(ordered) != checksum:
            raise ValueError(f"WPT timing plan shard {i} SHA-256 mismatch")
        lists.append(ordered.decode().splitlines())
    validate_lists(names, lists)
    return lists, meta
