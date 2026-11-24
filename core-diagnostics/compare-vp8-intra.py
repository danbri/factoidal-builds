from pathlib import Path
import hashlib
import subprocess
import sys
import time

probe, directory, *files = sys.argv[1:]
temp = Path(directory)
actual_path = temp / 'actual.yuv'
total = 0
for file in files:
    start = time.monotonic()
    subprocess.run(['lean', '--run', probe, file, str(actual_path)], check=True)
    reference = subprocess.check_output(['dwebp', '-quiet', '-nofilter', '-yuv', file, '-o', '-'])
    actual = actual_path.read_bytes()
    if actual != reference:
        first = next((i for i, (a,b) in enumerate(zip(actual, reference)) if a != b),
                     min(len(actual), len(reference)))
        raise SystemExit(f'{file}: first mismatch byte {first}, actual '
                         f'{actual[first:first+8].hex()}, libwebp {reference[first:first+8].hex()}, '
                         f'sizes {len(actual)}/{len(reference)}')
    total += len(actual)
    print(f'{Path(file).name}: {len(actual)} equal YUV bytes, '
          f'{hashlib.sha256(actual).hexdigest()}, {time.monotonic()-start:.3f}s incl. both tools')
assert len(files) == 14
print(f'{len(files)} images, {total} identical YUV bytes')
