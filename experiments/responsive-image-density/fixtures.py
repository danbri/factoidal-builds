"""Build native paint inputs from the exact WPT markup and original image bytes."""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
from urllib.parse import unquote_to_bytes
import base64, hashlib, json, shutil, struct, sys, zlib

web, source, destination = map(Path, sys.argv[1:])
destination.mkdir(exist_ok=True, parents=True)
imgs = destination / 'images'
imgs.mkdir(exist_ok=True)
green = web / 'images/green-256x256.png'
shutil.copyfile(green, imgs / green.name)
class Images(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            self.images.append(dict(attrs))
parser = Images(); parser.feed(source.read_text())
assert len(parser.images) == 14
jobs = []; cases = {}
def page(name, entries):
    tags = []
    cases[name] = []
    for ident, attrs, wh in entries:
        values = ' '.join(f'{k}="{escape(v, quote=True)}"' for k,v in attrs.items())
        tags.append(f'<img id="{ident}" {values}>')
        cases[name].append({'id': ident, 'size': wh})
    (destination / (name+'.html')).write_text(
        '<!doctype html><meta charset=utf-8><style>body{margin:0;background:white}img{display:block}</style>'+''.join(tags))
    jobs.append({'url': 'http://127.0.0.1:8030/'+name+'.html','width': 600,'height': 800,'file': name+'.png'})
for idx, original in enumerate(parser.images):
    attrs = original.copy(); width = int(attrs.pop('data-expect'))
    if idx < 11:
        src = '/images/green-256x256.png'; control = [256,256]
    else:
        url,descriptor = attrs['srcset'].rsplit(' ',1)
        data = unquote_to_bytes(url.split(',',1)[1])
        src = '/images/wpt-'+str(idx)+'.svg'; (destination / src[1:]).write_bytes(data)
        attrs['srcset'] = src+' '+descriptor
        control = [20,20]
    page(f'wpt-{idx:02}', [('control',{'src':src},control),('target',attrs,[width,width])])
def chunk(kind,payload):
    return struct.pack('>I',len(payload))+kind+payload+struct.pack('>I',zlib.crc32(kind+payload))
def stripe(name,width,height):
    half=width//2
    raw=(b'\0'+bytes([255,0,0])*half+bytes([0,0,255])*(width-half))*height
    contents=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',width,height,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(raw))+chunk(b'IEND',b'')
    (imgs/name).write_bytes(contents)
stripe('stripe.png',96,48)
stripe('odd.png',101,51)
src='/images/stripe.png'
page('stripes',[('plain',{'src':src},[96,48]),('twice',{'srcset':src+' 2x'},[48,24]),
                ('explicit',{'srcset':src+' 10000x','style':'width:96px'},[96,48]),
                ('fallback',{'src':src,'srcset':'/images/other.png 2x'},[96,48])])
shutil.copyfile(imgs/'stripe.png',imgs/'other.png')
page('stripe-reference',[('plain',{'src':src},[96,48]),
     ('twice',{'src':src,'style':'width:48px;height:24px'},[48,24]),
     ('explicit',{'src':src,'style':'width:96px'},[96,48]),
     ('fallback',{'src':src},[96,48])])
page('fractional',[('half',{'srcset':'/images/odd.png 2x'},[50.5,25.5]),
                   ('third',{'srcset':'/images/odd.png 3x'},[101/3,17]),
                   ('small',{'srcset':'/images/odd.png 1000x'},[.101,.051]),
                   ('width',{'srcset':'/images/odd.png 200w','sizes':'50px'},[25.25,12.75]),
                   ('minimum-width',{'srcset':'/images/odd.png 10000x','style':'min-width:101px'},[101,51]),
                   ('minimum-height',{'srcset':'/images/odd.png 10000x','style':'min-height:51px'},[101,51])])
# The Chrome HTML records completed image loads and actual CSS rectangles.
probe=(destination/'fractional.html').read_text()+"""<pre id=oracle>waiting</pre>
<script>window.addEventListener('load',()=>{document.querySelector('#oracle').textContent=JSON.stringify([...document.images].map(im=>{
const r=im.getBoundingClientRect(); return {id:im.id,loaded:im.complete,selected:!!im.currentSrc,
natural:[im.naturalWidth,im.naturalHeight],box:[r.x,r.y,r.width,r.height]};}))});</script>"""
(destination/'chrome-fractional.html').write_text(probe)
(destination/'jobs.jsonl').write_text(''.join(json.dumps(j)+'\n' for j in jobs))
(destination/'cases.json').write_text(json.dumps(cases,indent=2))
(destination/'images.sha256').write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+f.name+'\n' for f in sorted(imgs.iterdir())))
