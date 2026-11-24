from collections import Counter
from pathlib import Path
import os
import subprocess
import sys
import time

reference, probe, *files = sys.argv[1:]
total_blocks = 0
segments = Counter()
luma_shapes = Counter()
skip_config = Counter()
for file in files:
    start = time.monotonic()
    result = subprocess.run(['lean', '--run', probe, file], check=True,
                            capture_output=True, text=True, env=os.environ)
    reference_result = subprocess.run([reference, file, '-ppm', '-o', '-'],
                                      stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
                                      text=True)
    if reference_result.returncode:
        diagnostics = '\n'.join(line for line in reference_result.stderr.splitlines()
                                if not line.startswith('@'))
        raise SystemExit(f'{file}: libwebp exited {reference_result.returncode}\n{diagnostics}')
    actual = result.stdout.splitlines()
    expected = [line for line in reference_result.stderr.splitlines() if line.startswith('@')]
    if actual != expected:
        for index, (left, right) in enumerate(zip(actual, expected)):
            if left != right:
                i = next((i for i, (a, b) in enumerate(zip(left.split(), right.split()))
                          if a != b), 0)
                raise SystemExit(f'{file}: record {index}, word {i}: '
                                 f'Lean={left.split()[i:i+3]} libwebp={right.split()[i:i+3]}')
        raise SystemExit(f'{file}: Lean={len(actual)} libwebp={len(expected)} records')
    assert len(actual[0].split()) == 1057
    blocks = [line.split() for line in actual[2:]]
    assert blocks and all(len(b) in (5, 20) for b in blocks)
    skip_config[actual[1] != '@skip -1'] += 1
    for block in blocks:
        segments[block[1]] += 1
        luma_shapes[len(block) - 4] += 1
    total_blocks += len(blocks)
    print(f'{Path(file).name}: {len(blocks)} equivalent records, {time.monotonic()-start:.3f}s incl. both tools')
assert len(files) == 12 and len(segments) >= 2 and len(luma_shapes) == 2
print(f'{len(files)} frames, {total_blocks} macroblocks, 1056 probabilities per frame')
print(f'segments {dict(sorted(segments.items()))}, luma 4x4 blocks per record '
      f'(1 indicates a single 16x16 mode) {dict(sorted(luma_shapes.items()))}, '
      f'skip probability present {dict(sorted(skip_config.items()))}')
