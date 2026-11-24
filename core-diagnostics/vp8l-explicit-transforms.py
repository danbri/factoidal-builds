"""Generate complete small bitstreams that exercise all prediction modes."""
from pathlib import Path
import struct
import sys

out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)

class Bits:
    def __init__(self):
        self.bits = []

    def add(self, n, width):
        self.bits.extend((n >> i) & 1 for i in range(width))

    def group(self, green, red, blue, alpha):
        for n in (green, red, blue, alpha, 0):
            self.add(1, 1)
            self.add(0, 1)
            self.add(n > 1, 1)
            self.add(n, 8 if n > 1 else 1)

    def emit(self, name, width, height):
        content = bytes(sum(bit << j for j, bit in enumerate(self.bits[i:i+8]))
                        for i in range(0, len(self.bits), 8))
        size = (width - 1) + ((height - 1) << 14) + (1 << 28)
        vp8l = bytes([47]) + struct.pack('<I', size) + content
        riff = b'WEBPVP8L' + struct.pack('<I', len(vp8l)) + vp8l + bytes(len(vp8l) % 2)
        (out / (name + '.webp')).write_bytes(b'RIFF' + struct.pack('<I', len(riff)) + riff)

for i in range(14):
    predictor = Bits()
    predictor.add(1, 1)
    predictor.add(0, 6)  # type 0, tile bits 0, sub-image cache off
    predictor.group(i, 0, 0, 255)
    predictor.add(0, 3)  # end transform list, no cache or spatial groups
    predictor.group(154, 15, 34, 5)
    predictor.emit(f'predictor-{i}', 5, 3)

green = Bits()
green.add(1, 1)
green.add(2, 2)
green.add(0, 3)
green.group(18, 246, 254, 255)
green.emit('subtract-green', 3, 2)

color = Bits()
color.add(1, 1)
color.add(1, 2)
color.add(0, 4)
color.group(31, 250, 224, 255)
color.add(0, 3)
color.group(200, 40, 11, 125)
color.emit('negative-color-coefficients', 3, 2)
