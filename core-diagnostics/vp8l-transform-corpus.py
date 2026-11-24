"""A reproducible set of RGBA inputs to the libwebp encoder."""
import pathlib
import random
import sys

out = pathlib.Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)

def make(name, width, height, pixel):
    header = f"P7\nWIDTH {width}\nHEIGHT {height}\nDEPTH 4\nMAXVAL 255\nTUPLTYPE RGB_ALPHA\nENDHDR\n"
    body = bytes(value & 255 for y in range(height) for x in range(width) for value in pixel(x, y))
    (out / (name + '.pam')).write_bytes(header.encode() + body)

random.seed(142)
make('single', 1, 1, lambda x,y: (14,255,40,9))
make('vertical', 1, 37, lambda x,y: (y,2*y,7*y,255))
make('row', 53, 1, lambda x,y: (x,2*x,7*x,255))
make('noise', 61, 43, lambda x,y: tuple(random.randrange(256) for _ in range(4)))
make('smooth', 73, 57, lambda x,y: (x*2+y,73+x+y*2,15+x+y,255))
make('texture', 61, 97, lambda x,y: (x*y, x*4+y*13, x*9-y*y, x+y))
make('transparent', 18, 45, lambda x,y: (x*y, x*4+y*13, x*9-y*y, 0))
for n in (2, 4, 16, 17, 49, 256):
    make(f'palette-{n}', 21+n//10, 19, lambda x,y:
         ((x+y*17)%n*31, (x+y*17)%n*183, (x+y*17)%n*19, (x+y*17)%n*53))
