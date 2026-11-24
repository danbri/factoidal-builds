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

    def with_zero_run(self):
        # Three tokens give five actual lengths. The rest of the alphabet is zero.
        self.put(0, 1)
        self.put(0, 4)
        for length in (1, 0, 0, 1):  # code-length symbols 17, 18, 0, 1
            self.put(length, 3)
        self.put(1, 1)
        self.put(0, 3)
        self.put(1, 2)
        self.put(1, 1)  # canonical second code is repeat-zero (17)
        self.put(0, 3)
        self.put(0, 1)  # canonical first code is literal length one
        self.put(0, 1)

    def bytes(self):
        return bytes(sum(b << i for i, b in enumerate(self.bits[j:j+8]))
                     for j in range(0, len(self.bits), 8))

def write_case(name, greens, make_green):
    bits = Bits()
    bits.put(0, 3)  # no transforms, no cache, a single entropy group
    make_green(bits)
    for color in (32, 9, 125, 0):
        bits.simple(color)
    if len(greens) == 2:
        bits.put(0, 1)
        bits.put(1, 1)
    width_and_alpha = len(greens) - 1 + 2**28
    payload = b'\x2f' + struct.pack('<I', width_and_alpha) + bits.bytes()
    riff_data = b'WEBPVP8L' + struct.pack('<I', len(payload)) + payload
    riff_data += b'\0' * (len(payload) % 2)
    (out / (name + '.webp')).write_bytes(b'RIFF' + struct.pack('<I', len(riff_data)) + riff_data)
    expected[name] = [channel for g in greens for channel in (32, g, 9, 125)]

out = pathlib.Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
expected = {}
write_case('singleton', [174], lambda b: b.simple(174))
write_case('two-literals', [20, 55], lambda b: b.simple(55, 20))
write_case('normal-repeat', [3, 4], Bits.with_zero_run)
print(json.dumps(expected))
