from collections import Counter
from pathlib import Path
import subprocess
import sys
import time

reference, probe, *files = sys.argv[1:]
counts = Counter()
magnitude_counts = Counter()

for file in files:
    start = time.monotonic()
    lean = subprocess.run(['lean', '--run', probe, file], capture_output=True, text=True)
    if lean.returncode:
        raise SystemExit(f'{file}: Lean returned {lean.returncode}\n{lean.stderr}\n{lean.stdout[:1200]}')
    ref = subprocess.run([reference, file, '-ppm', '-o', '-'],
                         stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    if ref.returncode:
        diagnostics = '\n'.join(line for line in ref.stderr.splitlines() if not line.startswith('@'))
        raise SystemExit(f'{file}: libwebp returned {ref.returncode}\n{diagnostics}')
    actual = lean.stdout.splitlines()
    expected = [line for line in ref.stderr.splitlines()
                if line.startswith(('@position ', '@coeff '))]
    if actual != expected:
        last_position = 'before first record'
        for n, (a, b) in enumerate(zip(actual, expected)):
            if a != b:
                raise SystemExit(f'{file}: line {n} after {last_position}:\nLean {a}\nlibwebp {b}')
            if a.startswith('@position '):
                last_position = a
        raise SystemExit(f'{file}: record count Lean {len(actual)}, libwebp {len(expected)} '
                         f'after {last_position}')
    frame = Counter()
    for line in actual:
        tag, *values = line.split()
        if tag == '@position':
            frame['macroblocks'] += 1
            frame['skipped'] += int(values[2])
        else:
            assert len(values) == 16
            frame['blocks'] += 1
            for value in map(int, values):
                frame['samples'] += 1
                if value:
                    magnitude_counts['negative' if value < 0 else 'positive'] += 1
    assert frame['blocks'] == 24 * (frame['macroblocks'] - frame['skipped'])
    counts.update(frame)
    print(f'{Path(file).name}: {dict(frame)}, {time.monotonic()-start:.3f}s incl. both tools')

assert len(files) == 13 and counts['macroblocks'] == 4032 and counts['skipped'] > 0
assert magnitude_counts['positive'] and magnitude_counts['negative']
print(f'{len(files)} frames: {dict(counts)}, nonzero samples {dict(magnitude_counts)}')
