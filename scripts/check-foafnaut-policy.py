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


def wire_integer(value, minimum, maximum, label):
    """The Float storage ABI serializes integral fields as JSON ints or floats."""
    require(type(value) in (int, float) and math.isfinite(value) and
            value == int(value) and minimum <= value <= maximum, f'invalid {label}')
    return int(value)


def validate_storage(data, count):
    """Check NativeSVG.Primitive.rows, including every variable-sized tail.

    The five fixed vec4 rows are followed by polygon points or path edges,
    five rows per stroke/dash piece, an optional two-row inverse transform,
    then three rows per clip. The mode packs cap + 2*transform + 4*clipCount.
    This validates the wire cursor and fields, not SVG or shader semantics.
    """
    offset = 8
    for _ in range(count):
        require(offset+20 <= len(data), 'truncated storage record')
        tag = wire_integer(data[offset+4], 1, 6, 'geometry tag')
        points = wire_integer(data[offset+5], 0, 131072, 'geometry point/edge count')
        require(points >= 3 if tag == 5 else tag == 6 or points == 0,
                'invalid geometry point count')
        wire_integer(data[offset+6], 0, 1, 'fill rule')
        mode = wire_integer(data[offset+7], 0, 4*(262144//12)+3, 'primitive mode')
        pieces = wire_integer(data[offset+18], 0, 262144//20, 'stroke piece count')
        active = wire_integer(data[offset+19], 0, 1, 'stroke piece flag')
        require(active == 1 or pieces == 0, 'stroke pieces without active flag')
        require(all(0 <= value <= 1 for value in data[offset+8:offset+16]), 'invalid paint color/alpha')
        require(data[offset+16] >= 0 and 0 <= data[offset+17] <= 1, 'invalid stroke width/opacity')
        tail = points*4 if tag == 6 else ((2*points+3)//4)*4
        end = offset+20+tail+pieces*20+(8 if mode % 4 >= 2 else 0)+(mode//4)*12
        require(end <= len(data), 'truncated storage payload')
        cursor = offset+20+tail
        if tag == 5 and points % 2:
            require(data[cursor-2:cursor] == [0, 0], 'invalid polygon padding')
        for _ in range(pieces):
            piece = data[cursor:cursor+20]
            kind = wire_integer(piece[4], 2, 7, 'stroke piece tag')
            require(kind in (2, 4, 7), 'invalid stroke piece tag')
            require(piece[5:8] == [0, 0, 0] and piece[12:16] == [0, 0, 0, 0] and
                    piece[16] >= 0 and piece[17:20] == [0, 0, 0], 'invalid stroke piece fields')
            require(piece[10:12] == [0, 0] if kind == 7 else piece[8:12] == [0, 0, 0, 0],
                    'invalid stroke piece padding')
            cursor += 20
        if mode % 4 >= 2:
            require(data[cursor+3] == 0 and data[cursor+7] == 0, 'invalid affine padding')
            cursor += 8
        for _ in range(mode//4):
            clip = data[cursor:cursor+12]
            clip_active = wire_integer(clip[3], 0, 1, 'clip active flag')
            require(clip[7] == 0, 'invalid clip padding')
            require(clip[10] > 0 and clip[11] > 0 if clip_active else clip[8:12] == [0, 0, 0, 0],
                    'invalid clip bounds')
            cursor += 12
        require(cursor == end, 'storage cursor mismatch')
        offset = end
    require(offset == len(data), 'storage record count/length mismatch')


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
    # SceneSVG serializes each nonblank glyph as one compound path. Its many
    # cells/contours are one retained paint, as are stroke backend pieces.
    painted = sum(1 for e in svg.iter() if e.tag in {
        '{http://www.w3.org/2000/svg}' + tag for tag in ('rect', 'circle', 'ellipse', 'line', 'polygon', 'path')})
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
    validate_storage(data, count)
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
