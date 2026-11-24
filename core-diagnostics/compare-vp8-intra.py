from pathlib import Path
import hashlib
import re
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
    info = subprocess.check_output(['webpinfo', file], text=True)
    width = int(re.search(r'(?m)^  Width: (\d+)$', info)[1])
    height = int(re.search(r'(?m)^  Height: (\d+)$', info)[1])
    yuv_size = width * height + 2 * ((width+1)//2) * ((height+1)//2)
    alpha_size = width * height if re.search(r'(?m)^Chunk ALPH ', info) else 0
    assert len(reference) == yuv_size + alpha_size, (file, len(reference), yuv_size, alpha_size)
    # The CLI writes planar alpha after V. The intra decoder returns YUV only.
    reference = reference[:yuv_size]
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
