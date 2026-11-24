from pathlib import Path
from struct import pack, unpack_from
from subprocess import run
import sys

out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
width, height = 37, 29

def chunks(webp):
    assert webp[:4] == b'RIFF' and webp[8:12] == b'WEBP'
    i = 12
    while i < len(webp):
        size = unpack_from('<I', webp, i+4)[0]
        yield webp[i:i+4], webp[i+8:i+8+size]
        i += 8 + size + size % 2
    assert i == len(webp)

def chunk(tag, payload):
    return tag + pack('<I', len(payload)) + payload + bytes(len(payload) % 2)

def wrap(alpha_header, alpha):
    header = bytes([0x10, 0, 0, 0]) + (width-1).to_bytes(3,'little') + (height-1).to_bytes(3,'little')
    body = b'WEBP' + chunk(b'VP8X', header) + chunk(b'ALPH', bytes([alpha_header])+alpha) + chunk(b'VP8 ', vp8)
    return b'RIFF' + pack('<I',len(body)) + body

def ppm(path, data):
    path.write_bytes(f'P6\n{width} {height}\n255\n'.encode() + bytes(data))

colour, alpha = [], []
for y in range(height):
    for x in range(width):
        colour.extend(((11*x+3*y)%256, (x*x+y*7)%256, (7*x+13*y)%256))
        alpha.append((20*x*x + 17*y*(y//2) + 31*x*y) % 256)

colour_ppm = out/'alpha-colour.ppm'
colour_webp = out/'alpha-colour.webp'
ppm(colour_ppm, colour)
run(['cwebp','-quiet','-q','74',str(colour_ppm),'-o',str(colour_webp)],check=True)
vp8 = dict(chunks(colour_webp.read_bytes()))[b'VP8 ']

def filter_alpha(mode):
    result=[]
    for y in range(height):
        for x in range(width):
            idx = y*width+x
            if mode == 0 or (x==0 and y==0): predictor=0
            elif y==0: predictor=alpha[idx-1]
            elif x==0 or mode==2: predictor=alpha[idx-width]
            elif mode==1: predictor=alpha[idx-1]
            else:
                predictor=max(0,min(255,alpha[idx-1]+alpha[idx-width]-alpha[idx-width-1]))
            result.append((alpha[idx]-predictor)%256)
    return bytes(result)

for mode in range(4):
    residual = filter_alpha(mode)
    (out/f'alpha-raw-{mode}.webp').write_bytes(wrap(4*mode,residual))
    green_ppm = out/'residual-green.ppm'
    green_webp = out/'residual-green.webp'
    ppm(green_ppm,[c for g in residual for c in (0,g,0)])
    run(['cwebp','-quiet','-lossless','-z','3',str(green_ppm),'-o',str(green_webp)],check=True)
    vp8l = dict(chunks(green_webp.read_bytes()))[b'VP8L']
    assert vp8l[0]==0x2f
    (out/f'alpha-compressed-{mode}.webp').write_bytes(wrap(1+4*mode,vp8l[5:]))
(out/'alpha-expected.raw').write_bytes(bytes(alpha))
(out/'invalid-alpha.webp').write_bytes(wrap(2,b'\x00'))
