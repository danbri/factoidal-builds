from pathlib import Path
import sys
temp = Path(sys.argv[1])
width, height = 79, 65
data = bytearray()
for y in range(height):
    for x in range(width):
        base = 60 + 3 * (x // 4) + 3 * (y // 4)
        data += bytes((base+((x+y)%5), base+10, base+20+((x+2*y)%3)))
(temp / 'soft.ppm').write_bytes(f'P6\n{width} {height}\n255\n'.encode() + data)
