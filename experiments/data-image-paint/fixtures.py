from base64 import b64encode
from hashlib import sha256
from html import escape
from pathlib import Path
from urllib.parse import unquote_to_bytes
import re
import sys

css_path, out = map(Path, sys.argv[1:])
css = css_path.read_bytes()
assert sha256(css).hexdigest() == '2703d78ea35e2be2cab02ee71ca50aa4c0d22e074589da2aa055f77de049c9ca'
icons = re.findall(r'url\("(data:image/svg\+xml,[^"]+)"\)', css.decode())
assert len(icons) == 2
icons.append('data:image/svg+xml,%3Csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20width=%2720%27%20height=%2720%27%3E%3Crect%20width=%2720%27%20height=%2720%27%20fill=%27%2300ff00%27/%3E%3C/svg%3E')

def base64_variant(uri):
    data = unquote_to_bytes(uri.partition(',')[2])
    return 'data:image/svg+xml;base64,' + b64encode(data).decode('ascii')

def page(urls):
    icons = ''.join(f'<div style="background-image:url(&quot;{escape(url)}&quot;)"></div>' if url else '<div></div>'
                    for url in urls[:2])
    icon = f'<img src="{escape(urls[2])}" alt="">' if urls[2] else '<div></div>'
    return ('<!doctype html><meta charset=utf-8><style>body{margin:0;background:#fff}'
            'div,img{display:block;width:40px;height:40px;background-position:center;background-size:contain;'
            'background-repeat:no-repeat;margin:0 0 8px}img{object-fit:contain}</style>'
            + icons + icon)

out.mkdir(parents=True, exist_ok=True)
for name, variant in {'percent': icons, 'base64': [base64_variant(x) for x in icons], 'empty': ['', '', '']}.items():
    (out / (name + '.html')).write_text(page(variant), encoding='utf-8')
