"""Compare native and Chrome object sizes, painted references and resampling differences."""
import json, sys, re
from html import unescape
from pathlib import Path
from PIL import Image, ImageChops
root, fixtures = map(Path,sys.argv[1:])
cases=json.loads((fixtures/'cases.json').read_text()); rows=[]
for arm in ['control','candidate']:
    path=root/arm
    for name, entries in cases.items():
        images=json.loads((path/(name+'.png.json')).read_text())
        boxes={im['id']:im['boxes'][0] if im['boxes'] else None for im in images}
        assert len(boxes)==len(entries)
        pixels=Image.open(path/(name+'.png')).convert('RGB')
        for e in entries:
            box=boxes[e['id']]; expected=e['size']
            ok=box is not None and all(abs(actual-wanted)<=1/16 for actual,wanted in zip(box[2:4],expected))
            rows.append({'arm':arm,'page':name,'id':e['id'],'expected':expected,'box':box,'matches':ok})
            if name.startswith('wpt') and e['id']=='control':
                assert box and ok, (name,arm,box)
                colour=pixels.getpixel((int(box[0]+box[2]/2),int(box[1]+box[3]/2)))
                expected_colour=(0,255,0) if int(name[4:])<11 else (0,0,0)
                assert colour==expected_colour, (name,arm,colour)
    target=Image.open(path/'stripes.png').convert('RGB')
    reference=Image.open(path/'stripe-reference.png').convert('RGB')
    diff=ImageChops.difference(target,reference)
    diffs=sum(pixel!=(0,0,0) for pixel in diff.getdata())
    print(arm,'stripe pixel differences versus explicit reference:',diffs)
    if arm=='candidate':
        assert diffs==0
        assert target.getpixel((4,56))==(255,0,0) and target.getpixel((43,56))==(0,0,255)
        assert target.getpixel((55,56))==(255,255,255)
    else: assert diffs>0
(root/'geometry.json').write_text(json.dumps(rows,indent=2)+'\n')
for arm in ['control','candidate']:
    targets=[r for r in rows if r['arm']==arm and r['id']=='target']
    print(arm,'matches',sum(r['matches'] for r in targets),'of',len(targets),'loaded element-box cases')
    for r in targets: print(r['page'],r['box'],r['matches'])
    if arm=='candidate': assert all(r['matches'] for r in targets)
    else: assert not all(r['matches'] for r in targets)

oracle_html=(root/'chrome-fractional.html').read_text()
match=re.search(r'<pre id="oracle">(.*?)</pre>',oracle_html,re.S)
assert match
oracle=json.loads(unescape(match.group(1)))
native=json.loads((root/'candidate/fractional.png.json').read_text())
assert len(oracle)==len(native)==6
for browser, engine in zip(oracle,native):
    assert browser['loaded'] and browser['selected'] and browser['id']==engine['id']
    assert all(abs(x-y)<=1/16 for x,y in zip(browser['box'][2:4],engine['boxes'][0][2:4])), (browser,engine)
crop=(0,0,160,170)
chrome=Image.open(root/'chrome-stripes.png').convert('RGB').crop(crop)
native=Image.open(root/'candidate/stripes.png').convert('RGB').crop(crop)
chrome_ref=Image.open(root/'chrome-reference.png').convert('RGB').crop(crop)
native_ref=Image.open(root/'candidate/stripe-reference.png').convert('RGB').crop(crop)
assert ImageChops.difference(chrome,chrome_ref).getbbox() is None, 'Chrome density and explicit reference disagree'
# A compositor's reconstruction filter applies to an explicit downscale too.
# Report the actual cross-engine discrepancy and verify it is unchanged with srcset.
cross=ImageChops.difference(chrome,native)
explicit_cross=ImageChops.difference(chrome_ref,native_ref)
assert ImageChops.difference(cross,explicit_cross).getbbox() is None
coords=[(x,y) for y in range(cross.height) for x in range(cross.width) if cross.getpixel((x,y))!=(0,0,0)]
print('Chrome and candidate agree on all six fractional/high-density sizes within 1/16 CSS px.')
print('Both engines paint the density-selected stripes identically to their own explicit-size reference.')
print('Cross-engine pixel differences:',len(coords),'of',cross.width*cross.height,'at bounds',cross.getbbox(),
      'for both responsive and explicit sizing.')
