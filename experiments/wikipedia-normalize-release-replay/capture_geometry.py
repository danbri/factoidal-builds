"""Add receipt-only observation at the CPU renderer’s existing decoded answer."""
import hashlib
from pathlib import Path
import sys

path = Path(sys.argv[1])
data = path.read_bytes()
assert hashlib.sha256(data).hexdigest() == sys.argv[2]
code = data.decode()
marker = "  const k=scene.pixelsSection;"
assert code.count(marker) == 1
observation = """
  const layout=scene.webRender as {boxes?:number[][];glyphRuns?:unknown[];links?:unknown[]}|undefined;
  if(!layout||!Array.isArray(layout.boxes))throw new Error("CPU answer has no layout boxes");
  await Deno.writeTextFile(`${outDir}/geometry.json`, JSON.stringify({
    width:job.width,height:job.height,
    boxes:layout.boxes,glyphRuns:layout.glyphRuns??[],links:layout.links??[],
  }));
"""
path.write_text(code.replace(marker, observation + marker))
