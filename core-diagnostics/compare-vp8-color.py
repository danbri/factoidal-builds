from pathlib import Path
import hashlib
import re
import subprocess
import sys
import time

probe, directory, *files = sys.argv[1:]
temp = Path(directory)
actual_path = temp / 'actual.rgba'
alpha_path = temp / 'reference.alpha'
total = 0
with_alpha = 0

for file in files:
    start = time.monotonic()
    pam = subprocess.check_output(['dwebp', '-quiet', '-pam', file, '-o', '-'])
    header, payload = pam.split(b'ENDHDR\n', maxsplit=1)
    fields = dict(line.split(maxsplit=1) for line in header.splitlines()
                  if line and not line.startswith(b'#') and line != b'P7')
    width, height, depth = (int(fields[key]) for key in (b'WIDTH', b'HEIGHT', b'DEPTH'))
    assert fields[b'MAXVAL'] == b'255' and len(payload) == width * height * depth
    assert depth in (3, 4), (file, depth)
    args = ['lean', '--run', probe, file, str(actual_path)]
    if depth == 4:
        info = subprocess.check_output(['webpinfo', file], text=True)
        alphas = payload[3::4]
        if re.search(r'(?m)^Chunk ALPH ', info):
            with_alpha += 1
            alpha_path.write_bytes(alphas)
            args.append(str(alpha_path))
        else:
            assert all(value == 255 for value in alphas), file
        reference = payload
    else:
        reference = bytearray([255]) * (width * height * 4)
        for channel in range(3):
            reference[channel::4] = payload[channel::3]
    subprocess.run(args, check=True)
    actual = actual_path.read_bytes()
    if actual != reference:
        first = next((i for i, (a,b) in enumerate(zip(actual, reference)) if a != b),
                     min(len(actual), len(reference)))
        raise SystemExit(f'{file}: first mismatch byte {first} '
                         f'pixel ({first//4%width},{first//4//width}), channel {first%4}, '
                         f'actual {actual[first:first+12].hex()}, libwebp {reference[first:first+12].hex()}')
    total += len(actual)
    print(f'{Path(file).name}: {width}x{height}, {len(actual)} equal RGBA bytes, '
          f'{hashlib.sha256(actual).hexdigest()}, {time.monotonic()-start:.3f}s incl. both tools')
assert len(files) == 17 and with_alpha == 1
print(f'{len(files)} images, {total} identical RGBA bytes, {with_alpha} reference alpha plane supplied')
