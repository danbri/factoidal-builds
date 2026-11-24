from pathlib import Path
import sys

path = Path(sys.argv[1])
s = path.read_text()
def replace_once(old: str, new: str):
    global s
    assert s.count(old) == 1, old
    s = s.replace(old, new)

replace_once("      if(layered&&worker?.alive&&!prefetching&&motion&&current&&canShift()&&!dirty&&!rendering&&!loading&&!graphBusy()&&worker.pending===0){",
"""      if (motion && current && motion.at !== diagnosedScrollAt) {
        diagnosedScrollAt = motion.at;
        const band = current.layers.layers;
        const target = prefetchTarget(band, scroll, motion, {
          marginRows: PREFETCH_MARGIN_ROWS, horizonMs: 2 * FRAME_MS + bandMs, limit: scrollLimit(),
        });
        trace("native-html-scroll-gate", {
          scroll, target: target ?? null, keepFrom: band.keepFrom, keepTo: band.keepTo,
          canShift: canShift(), dirty, rendering: Boolean(rendering), loading,
          graphBusy: graphBusy(), pending: worker?.pending ?? null,
          prefetched: Boolean(prefetched), prefetching: Boolean(prefetching),
          deferredChange: pageChanged !== undefined, bandMs,
        });
      }
      if(layered&&worker?.alive&&!prefetching&&motion&&current&&canShift()&&!dirty&&!rendering&&!loading&&!graphBusy()&&worker.pending===0){""")
replace_once("  let holdTraced=false;", "  let holdTraced=false, diagnosedScrollAt=-Infinity;")
replace_once("      const sentWidth=width,sentHeight=height;", """      trace("native-html-scroll-diagnostic-frame", {
        scroll, pending: worker?.pending ?? null, deferredChange: pageChanged !== undefined,
      });
      const sentWidth=width,sentHeight=height;""")
if len(sys.argv) > 2:
    replace_once('&&!graphBusy()&&worker.pending===0){', '&&!graphBusy()){')
path.write_text(s)
