#!/usr/bin/env python3
"""Experiment with a bounded quiet period for post-paint network turns."""
import sys
from pathlib import Path

path = Path(sys.argv[1])
source = path.read_text()

def patch(old, new):
    global source
    assert source.count(old) == 1, old
    source = source.replace(old, new)

patch(
    "  const pageChangedNow=()=>{\n    const now=performance.now();",
    """  let networkQuietUntil=-Infinity;
  const pageChangedNow=(network=false)=>{
    const now=performance.now();
    if(network&&firstShown.has(document)&&now-inputAt>120){
      pageChanged??=now;
      networkQuietUntil=Math.min(pageChanged+250,now+100);
      trace("native-html-network-paint-hold",{delayMs:Math.max(0,networkQuietUntil-now)});
      return;
    }
    networkQuietUntil=-Infinity;""",
)
patch(
    "      if(page===document)pageChangedNow();\n      // What elements made or changed",
    '      if(page===document)pageChangedNow(cause==="net");\n      // What elements made or changed',
)
patch(
    "      if(pageChanged!==undefined&&(firstShown.has(document)||!rendering)&&!scrollHolds(performance.now())&&!scriptsHold(performance.now()))",
    """      const paintNow=performance.now();
      if(pageChanged!==undefined&&(paintNow>=networkQuietUntil||paintNow-inputAt<=120)&&
          (firstShown.has(document)||!rendering)&&!scrollHolds(paintNow)&&!scriptsHold(paintNow))""",
)
path.write_text(source)
