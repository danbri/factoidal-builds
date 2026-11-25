"""Build paired image-transfer variants from one checked browser host."""
from pathlib import Path
import sys

source = Path(sys.argv[1])
text = source.read_text()

def replace(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new)

start = text.index("export async function fetchImageBytes(")
end = text.index("\nfunction base64(", start)
prefix, original, suffix = text[:start], text[start:end], text[end:]

# Time the existing network wait separately from deterministic fingerprinting.
baseline = replace(original, "  const read:", "  const started=performance.now();\n  const read:")
baseline = replace(baseline, "  const images:", "  const transferMs=performance.now()-started;\n  const images:")
baseline = replace(baseline, "  return images;", """  if(wanted.length){
    const applied=[];
    for(const {key,bytes} of images)applied.push([key,await sha256Hex(bytes)]);
    const fingerprint=await sha256Hex(new TextEncoder().encode(JSON.stringify(applied)));
    console.log(JSON.stringify({type:"startup-image-batch",wanted:wanted.length,
      loaded:images.length,bytes:total,transferMs,fingerprint,t:performance.now()}));
  }
  return images;""")

source.write_text(prefix + baseline + suffix)
