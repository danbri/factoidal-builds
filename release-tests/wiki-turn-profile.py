import collections
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

lab, engine, out = map(Path, sys.argv[1:])
textnaut = lab / 'textnaut/textnaut.ts'
source = textnaut.read_text()
anchor = '      take(await synced(engine, engine.scriptSession("", { action: "advance", session: script.session, ms })));'
assert source.count(anchor) == 1
probe = '''      const targetClock = turn.clock + ms;
      const started = performance.now();
      console.error(JSON.stringify({type:"wiki-profile-start",targetClock}));
'''+anchor+'''
      console.error(JSON.stringify({type:"wiki-profile-end",targetClock,actualClock:turn.clock,
        elapsed:Math.round(performance.now()-started),layouts:turn.layouts,reads:turn.reads}));
'''
textnaut.write_text(source.replace(anchor, probe))

command = [
    'deno','run','--no-prompt','--preload',str(lab/'realpages/replay.ts'),
    '--allow-read','--allow-ffi','--allow-net','--allow-env','--import-map='+str(lab/'textnaut/import_map.json'),
    str(textnaut),'--dump','--timing','--width','160','--engine',str(engine),
    'https://en.wikipedia.org/wiki/United_States',
]
def capture(arm, profile):
    log_path, output = out / f'{arm}.log', out / f'{arm}.dump'
    samplers = {}
    timing = {}
    with output.open('wb') as data, log_path.open('w') as log, subprocess.Popen(
        command, stdout=data, stderr=subprocess.PIPE, text=True, bufsize=1,
    ) as proc:
        for line in proc.stderr:
            log.write(line)
            if not line.startswith('{"type":"wiki-profile-'):
                continue
            row = json.loads(line)
            clock = row['targetClock']
            if row['type'] == 'wiki-profile-end':
                timing[clock] = row
            elif profile and clock in {7852, 7856}:
                assert clock not in samplers
                file = out / f'turn-{clock}.sample'
                with (out / f'turn-{clock}.sampler.log').open('w') as capture_log:
                    samplers[clock] = subprocess.Popen(
                        ['sudo','sample',str(proc.pid),'6','2','-file',str(file)],
                        stdout=capture_log, stderr=subprocess.STDOUT,
                    )
        assert proc.wait() == 0, log_path
    for clock, sampler in samplers.items():
        assert sampler.wait() == 0, clock
    result = hashlib.sha256(output.read_bytes()).hexdigest()
    output.unlink()
    return result,timing,samplers

baseline, controls, _ = capture('control', False)
profiled, timings, samplers = capture('profile', True)
assert baseline == profiled, (baseline, profiled)
assert set(samplers) == {7852,7856}, timings
assert all(timings[t]['elapsed'] > 6000 and timings[t]['layouts'] > 0 for t in samplers), timings

categories = {
    'layout': ('L4Factoidal_Rendering_Layout_',),
    'cascade': ('Rendering_Generated_styled','Rendering_CSS_computeAll'),
    'matching': ('Rendering_CSS_matchEntry','Rendering_CSS_matchGroupedEntry','DOM_Selectors'),
    'style application': ('Rendering_CSS_apply',),
    'text shaping': ('SfntShape_','WebDocument_shapeKept','bitmapOutline'),
    'visited URL state': ('WebDocument_elementState',),
    'JavaScript interpreter': ('L4Factoidal_JS_vmLoop',),
    'geometry answer': ('WebDocument_readAnswer',),
}
def counts(path):
    levels = []
    tally = collections.Counter()
    active = False
    for line in path.read_text().splitlines():
        if 'com.apple.main-thread' in line:
            active = True
            continue
        if not active:
            continue
        item = re.match(r'^([ +!|:-]*)(\d+)\s+(\S+)',line)
        if not item:
            continue
        depth, total, symbol = len(item[1]), int(item[2]), item[3]
        if symbol.startswith('Thread_'):
            break
        while levels and levels[-1][0] >= depth:
            levels.pop()
        group = {name for name, needles in categories.items() if any(n in symbol for n in needles)}
        inherited = levels[-1][1] if levels else set()
        for name in group - inherited:
            tally[name] += total
        levels.append((depth, group | inherited))
    assert tally['layout'] or tally['cascade'], path
    return dict(tally)
report = {'sha256':baseline,'control':controls, 'profiled':timings,
          'inclusiveSamples':{t:counts(out / f'turn-{t}.sample') for t in samplers}}
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
