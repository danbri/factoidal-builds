import json
import re
import subprocess
import sys
from pathlib import Path

records = [json.loads(line) for line in Path(sys.argv[1]).read_text().splitlines()]
assert records, "no frames to compare"
for frame in records:
    result = frame["result"]
    reference = subprocess.check_output(["webpinfo", "-bitstream_info", frame["file"]], text=True)
    observed = {}
    for field, value in re.findall(r"^\s+([^:\n]+):[ \t]+(-?\d+(?: +-?\d+)*)[ \t]*$", reference, re.M):
        numbers = list(map(int, value.split()))
        observed[field.strip()] = numbers if len(numbers) > 1 else numbers[0]
    differences = {key: [value, observed.get(key)] for key, value in result["fields"].items()
                   if observed.get(key) != value}
    assert not differences, (frame["file"], differences)
    assert len(result["partitions"]) == observed["Total partitions"]
    data = Path(frame["file"]).read_bytes()
    chunk_offset = 12
    while data[chunk_offset:chunk_offset+4] != b"VP8 ":
        size = int.from_bytes(data[chunk_offset+4:chunk_offset+8], "little")
        chunk_offset += 8 + size + (size % 2)
    start = chunk_offset + 8
    end = start + int.from_bytes(data[chunk_offset+4:start], "little")
    table = start + 10 + observed["Part. 0 length"]
    count = observed["Total partitions"]
    cursor = table + 3 * (count - 1)
    want = []
    for i in range(count):
        size = end - cursor if i == count - 1 else int.from_bytes(data[table+3*i:table+3*i+3], "little")
        want.append([cursor, size])
        cursor += size
    assert cursor == end and result["partitions"] == want, (frame["file"], want)
print(f"Matched VP8 control fields against libwebp for all {len(records)} files.")
