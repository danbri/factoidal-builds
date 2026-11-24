"""Generate the minimal cases for the HTML-to-SVG author cascade (core issue 918)."""
import json
import pathlib
import sys

out = pathlib.Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
frame = '<svg class="icon" width="64" height="64" viewBox="0 0 64 64">{}</svg>'
circle = '<circle id="disc" class="disc" cx="32" cy="32" r="24" {}/>'
blue = '#d2e2f1'
red = '#e02424'
cases = [
    ('presentation', '', circle.format(f'fill="{blue}"'), blue),
    ('descendant', f'.icon .disc {{fill:{blue}}}', circle.format(f'fill="{red}"'), blue),
    ('specificity', f'#disc {{fill:{blue}}} .icon .disc {{fill:{red}}}', circle.format(''), blue),
    ('order', f'.icon .disc {{fill:{red}}} .icon .disc {{fill:{blue}}}', circle.format(''), blue),
    ('author-important', f'.icon .disc {{fill:{blue}!important}}',
     circle.format(f'style="fill:{red}"'), blue),
    ('inline-important', f'.icon .disc {{fill:{red}!important}}',
     circle.format(f'style="fill:{blue}!important"'), blue),
    ('higher-layer', f'@layer base,theme; @layer theme {{.disc {{fill:{blue}}}}} '
     f'@layer base {{#disc {{fill:{red}}}}}', circle.format(''), blue),
    ('earlier-important-layer', f'@layer base,theme; @layer base {{.disc {{fill:{blue}!important}}}} '
     f'@layer theme {{#disc {{fill:{red}!important}}}}', circle.format(''), blue),
    ('svg-style-wins', f'.icon .disc {{fill:{red}}}',
     f'<style>.icon .disc {{fill:{blue}}}</style>{circle.format("")}', blue),
    ('html-specificity-wins', f'#disc {{fill:{blue}}}',
     f'<style>.disc {{fill:{red}}}</style>{circle.format("")}', blue),
    ('styled-group-inheritance', f'.icon .arrow {{fill:{blue}}}',
     f'<g class="arrow">{circle.format("")}</g>', blue),
    ('html-color-to-currentcolor', f'body {{color:{blue}}} .icon .disc {{fill:currentColor}}',
     circle.format(''), blue),
    ('var-and-media', f'body {{--brand:{blue}}} @media (min-width:70px) {{.icon .disc {{fill:var(--brand)}}}}',
     circle.format(''), blue),
]
with (out / 'cases.json').open('w') as listing:
    json.dump([{'id': name, 'want': color} for name, _, _, color in cases], listing)
for name, css, children, color in cases:
    source = ('<!doctype html><style>body{margin:0;background:white}'
              + css + '</style>' + frame.format(children)
              + '<script>const sample=document.createElement("output");'
              + 'sample.id="result";sample.textContent=getComputedStyle(document.querySelector("#disc")).fill;'
              + 'document.body.append(sample)</script>')
    (out / f'{name}.html').write_text(source)
