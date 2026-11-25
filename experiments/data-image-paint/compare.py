from pathlib import Path
import json
import sys

out = Path(sys.argv[1])
roles = ['baseline', 'candidate']

def digests(role):
    rows = [json.loads(s[len('__done '):]) for s in (out / f'{role}.log').read_text().splitlines() if s.startswith('__done ')]
    assert len(rows) == 9 and all(r['status'] == 'ok' for r in rows), rows
    return {r['file']: r['sha'] for r in rows}

before, after = map(digests, roles)
assert before.keys() == after.keys()
stems = ['object-fit-fill-svg-with-natural-size-and-viewbox', 'object-fit-none-svg-width-only', 'object-fit-svg-no-natural-dimensions']
compared = {r: {s: data[s + '.png'] == data[s + '-ref.png'] for s in stems} for r, data in zip(roles, (before, after))}
receipt = {'baseline': before, 'candidate': after, 'wpt_reftests': compared}
(out / 'compare.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(compared))
assert before['base64.png'] == after['base64.png']
assert before['empty.png'] == after['empty.png']
assert before['base64.png'] != before['empty.png']
assert before['percent.png'] != before['base64.png']
assert after['percent.png'] == after['base64.png']
assert all(not passed or compared['candidate'][stem] for stem, passed in compared['baseline'].items())
