"""Generate small complete VP8L files with nonliteral tokens and a spatial map."""
import json
import pathlib
import struct
import sys

class Bits:
    def __init__(self):
        self.bits = []

    def put(self, value, size):
        assert 0 <= value < 2 ** size
        self.bits.extend(value >> bit & 1 for bit in range(size))

    def simple(self, first, second=None):
        self.put(1, 1)
        self.put(second is not None, 1)
        self.put(first > 1, 1)
        self.put(first, 8 if first > 1 else 1)
        if second is not None:
            self.put(second, 8)

    def sparse_pair(self, high_symbol):
        # Two length-one symbols, zero and high_symbol. Each zero run is a token.
        remaining = high_symbol - 1
        runs = []
        while remaining > 138:
            run = min(138, remaining - 11)
            runs.append(run)
            remaining -= run
        runs.append(remaining)
        self.put(0, 1)
        self.put(0, 4)
        for length in (0, 1, 0, 1):
            self.put(length, 3)
        self.put(1, 1)
        self.put(1, 3)
        self.put(len(runs), 4)
        self.put(0, 1)
        for run in runs:
            self.put(1, 1)
            self.put(run-11, 7)
        self.put(0, 1)

    def channels(self, distance=0):
        for value in (32, 9, 125, distance):
            self.simple(value)

    def bytes(self):
        return bytes(sum(v << i for i, v in enumerate(self.bits[j:j+8]))
                     for j in range(0, len(self.bits), 8))

def emit(name, width, height, greens, bits):
    assert len(greens) == width * height
    packed = (width-1) + ((height-1) << 14) + (1 << 28)
    payload = b'\x2f' + struct.pack('<I', packed) + bits.bytes()
    riff = b'WEBPVP8L' + struct.pack('<I', len(payload)) + payload + bytes(len(payload) % 2)
    (out / (name + '.webp')).write_bytes(b'RIFF' + struct.pack('<I', len(riff)) + riff)
    expected[name] = [channel for g in greens for channel in (32, g, 9, 125)]

out = pathlib.Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
expected = {}

repeat = Bits()
repeat.put(0, 3)
repeat.sparse_pair(258)
repeat.channels(1)
first_symbol = len(repeat.bits)
repeat.put(0, 1)
repeat.put(1, 1)
emit('overlapping-lz', 4, 1, [0] * 4, repeat)

cache = Bits()
cache.put(0, 1)
cache.put(1, 1)
cache.put(1, 4)
cache.put(0, 1)
pixel = (125 << 24) + (32 << 16) + 9
slot = ((0x1e35a7bd * pixel) & 0xffffffff) >> 31
cache.sparse_pair(280 + slot)
cache.channels()
cache.put(0, 1)
cache.put(1, 1)
emit('color-cache', 2, 1, [0, 0], cache)

spatial = Bits()
spatial.put(0, 2)
spatial.put(1, 1)
spatial.put(0, 3)
spatial.put(0, 1)
spatial.simple(0, 1)
for value in (0, 0, 255, 0):
    spatial.simple(value)
spatial.put(0, 1)
spatial.put(1, 1)
for green in (100, 200):
    spatial.simple(green)
    spatial.channels()
emit('spatial-groups', 8, 4, ([100] * 4 + [200] * 4) * 4, spatial)

duplicate = Bits()
duplicate.put(0, 3)
duplicate.simple(174, 174)
duplicate.channels()
emit('duplicate-singleton', 1, 1, [174], duplicate)

invalid = bytearray((out / 'overlapping-lz.webp').read_bytes())
byte = 25 + first_symbol // 8
invalid[byte] |= 1 << (first_symbol % 8)
(out / 'invalid.backref').write_bytes(invalid)

print(json.dumps(expected))
