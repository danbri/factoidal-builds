from pathlib import Path
import sys

path = Path(sys.argv[1])
source = path.read_text()
old = "  let scrollAt=-Infinity,pageChanged:number|undefined;"
stamps = "awaitingShift:{kind:number;at:number}[]=[],awaitingBand:{kind:number;at:number}[]=[]"
assert source.count(old) == 1 and source.count(stamps) == 1
source = source.replace(stamps + ",", "")
source = source.replace(old, old + "\n  let " + stamps + ";")
old = "    return scrollFirst({now,scrollAt,changedAt:pageChanged===undefined?undefined:Math.max(pageChanged,shownAt??-Infinity),shownAt});"
assert source.count(old) == 1
source = source.replace(old, """    const waitingForBand=(awaitingShift.length>0||awaitingBand.length>0)&&canShift();
    // A queued scroll has not gone quiet until it reaches the screen. The existing
    // changedAt deadline still bounds the wait for script updates.
    return scrollFirst({now,scrollAt:waitingForBand?now:scrollAt,
      changedAt:pageChanged===undefined?undefined:Math.max(pageChanged,shownAt??-Infinity),shownAt});""")
path.write_text(source)
