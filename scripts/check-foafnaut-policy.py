#!/usr/bin/env python3
"""Validate checked-export packaging evidence; no GPU/pixel equivalence claim."""
import hashlib
import json
import math
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

WEB_FILES = (
    'web/policy-demo.html', 'web/policy-demo.mjs', 'web/policy_engine.mjs',
    'web/foafnaut_transport.mjs', 'web/foaf/fixtures/people.ttl',
    'web/.build/engines/foafnaut-engine.mjs', 'web/.build/engines/foafnaut-engine.wasm',
    'web/.build/engines/layout-policy-engine.mjs', 'web/.build/engines/layout-policy-engine.wasm',
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def integer(value, minimum, maximum, label):
    require(type(value) is int and minimum <= value <= maximum, f'invalid {label}')
    return value


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f'duplicate JSON key: {key}')
        result[key] = value
    return result


def read_json(path, limit):
    require(path.stat().st_size <= limit, f'oversized evidence: {path.name}')
    return json.loads(path.read_text(), object_pairs_hook=unique_object)


def validate(root):
    root = Path(root)
    for relative in WEB_FILES:
        path = root / relative
        require(path.is_file() and path.stat().st_size > 0, f'missing web asset: {relative}')
        if path.suffix == '.wasm':
            with path.open('rb') as stream:
                require(stream.read(8) == b'\0asm\x01\0\0\0', f'invalid WASM asset: {relative}')
    svg_path = root / 'checked.svg'
    require(0 < svg_path.stat().st_size <= 4194304, 'invalid checked SVG file size')
    svg = ET.parse(svg_path).getroot()
    require(svg.tag == '{http://www.w3.org/2000/svg}svg', 'checked export is not SVG')
    width = integer(int(svg.attrib['width']), 1, 4096, 'SVG width')
    height = integer(int(svg.attrib['height']), 1, 4096, 'SVG height')
    painted = sum(1 for e in svg.iter() if e.tag in {
        '{http://www.w3.org/2000/svg}' + tag for tag in ('rect', 'circle', 'ellipse', 'line', 'polygon')})
    require(painted > 0, 'checked SVG has no painted primitives')

    report = read_json(root / 'checked.svg.policy.json', 4194304)
    require(report['profile'] == 'experimental-graph-browser-v1', 'unknown policy profile')
    require(report['metric'] == 'viewport-clipped node bounding boxes; sum of pairwise intersections', 'wrong policy metric')
    require(report['timing'] == 'checked at export; no scheduling claim', 'wrong export timing claim')
    require(report['enforced'] is True and report['withinBudget'] is True, 'export is not checked/accepted')
    app, cfg = report['policy']['application'], report['policy']['configuration']
    lo = integer(app['minOverlapBps'], 300, 700, 'minimum overlap')
    hi = integer(app['maxOverlapBps'], lo, 700, 'maximum overlap')
    hz_lo = integer(app['minCheckHz'], 12, 24, 'minimum check Hz')
    hz_hi = integer(app['maxCheckHz'], hz_lo, 24, 'maximum check Hz')
    bps = integer(cfg['overlapBps'], lo, hi, 'chosen overlap')
    hz = integer(cfg['checkHz'], hz_lo, hz_hi, 'chosen check Hz')
    require(integer(report['thresholdBasisPoints'], lo, hi, 'reported overlap') == bps and
            integer(report['targetCheckHz'], hz_lo, hz_hi, 'reported check Hz') == hz, 'report/config mismatch')
    nodes = report['nodes']
    require(isinstance(nodes, list) and 0 < len(nodes) <= 16, 'expected nonempty FOAFNaut node report')
    people, boxes = set(), []
    for node in nodes:
        person = integer(node['person'], 0, 15, 'person index')
        require(person not in people, 'duplicate person index')
        people.add(person)
        bounds = node['bounds']
        require(isinstance(bounds, list) and len(bounds) == 4, 'invalid node box')
        l, t, r, b = (integer(v, 0, width if i % 2 == 0 else height, 'clipped box edge') for i, v in enumerate(bounds))
        require(l < r and t < b, 'node box has no positive area')
        require(integer(node['area'], 1, width * height, 'node area') == (r-l)*(b-t), 'node area/box mismatch')
        boxes.append((l, t, r, b))
    # Independent evidence check, not runtime layout enforcement or a union area.
    for i, (node, (l, t, r, b)) in enumerate(zip(nodes, boxes)):
        overlap = sum(max(0, min(r, rr)-max(l, ll))*max(0, min(b, bb)-max(t, tt))
                      for j, (ll, tt, rr, bb) in enumerate(boxes) if i != j)
        require(integer(node['overlapUpperBound'], 0, 15*width*height, 'overlap sum') == overlap, 'overlap evidence mismatch')
        require(node['withinBudget'] is True and 10000*overlap <= bps*node['area'], 'node exceeds chosen budget')

    artifact = read_json(root / 'checked-native.json', 16777216)
    require(artifact['abi'] == 'lean-svg-v1' and artifact['profile'] == 'painted-primitives-experiment', 'wrong SVG artifact ABI/profile')
    require(artifact['binding'] == 'read-only-storage', 'SVG artifact must use storage binding')
    require(type(artifact['width']) is int and type(artifact['height']) is int and
            (artifact['width'], artifact['height']) == (width, height), 'SVG artifact viewport mismatch')
    count = integer(artifact['primitiveCount'], 1, 12288, 'primitive count')
    require(count == painted, 'compiled primitive count differs from exported SVG')
    data = artifact['data']
    require(isinstance(data, list) and 8 <= len(data) <= 262144 and len(data) % 4 == 0, 'invalid storage length')
    require(all(type(v) in (int, float) and math.isfinite(v) and abs(v) <= 3.402823466e38 for v in data), 'invalid storage float')
    require(data[6:8] == [width, height], 'storage viewport header mismatch')
    offset = 8
    for _ in range(count):
        require(offset+20 <= len(data), 'truncated storage record')
        tag, points = data[offset+4:offset+6]
        require(tag == int(tag) and 1 <= tag <= 5, 'invalid geometry tag')
        require(points == int(points) and 0 <= points <= 131072, 'invalid polygon count')
        tag, points = int(tag), int(points)
        require(points >= 3 if tag == 5 else points == 0, 'invalid geometry point count')
        offset += 20 + ((2*points+3)//4)*4
    require(offset == len(data), 'storage record count/length mismatch')
    shader = artifact['wgsl']
    require(isinstance(shader, str) and 0 < len(shader) <= 1048576 and 'var<storage,read>' in shader, 'missing storage shader')
    probes = artifact['checks']
    require(isinstance(probes, list) and probes, 'missing Lean CPU reference probes')
    for probe in probes:
        integer(probe['x'], 0, width-1, 'probe x')
        integer(probe['y'], 0, height-1, 'probe y')
        require(isinstance(probe['rgb'], list) and len(probe['rgb']) == 3, 'invalid probe color')
        for value in probe['rgb']:
            integer(value, 0, 255, 'probe color component')
    return {'svg_sha256': hashlib.sha256(svg_path.read_bytes()).hexdigest(), 'nodes': len(nodes),
            'primitives': count, 'storage_floats': len(data), 'application': app, 'configuration': cfg}


if __name__ == '__main__':
    print('Checked SVG export/storage/package validation: ' + json.dumps(validate(sys.argv[1]), sort_keys=True))
    print('No GPU rendering, pixel equivalence or scheduling guarantee claimed')
