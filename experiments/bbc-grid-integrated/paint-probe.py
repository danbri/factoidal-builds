from pathlib import Path

runner = Path("core/tests/browser-wpt/reftest-render.ts")
source = runner.read_text()
anchor = "  const rgba=new Uint8Array(buffer,offset,length);"
assert source.count(anchor) == 1
probe = """

  const inspected = engine.inspect(source,{...options,url:page.url,liberal:true}) as unknown as
      {images?: {key:string}[]};
  if (!Array.isArray(inspected.images) || !Array.isArray(options.heldImages)) {
    throw new Error("missing image declarations or held bytes");
  }
  const held = Object.fromEntries((options.heldImages as {key:string;sha256:string}[]).map(item => [item.key,item.sha256]));
  await Deno.writeTextFile("out/document-image-keys.json", JSON.stringify({
    pictures: inspected.images.map(item => item.key), held,
  }, null, 2));
  const byteView = (key: string) => {
    const n = scene[key];
    if (typeof n !== "number") throw new Error(`no ${key}`);
    const [offset, length] = sections[n];
    return new DataView(buffer, offset, length);
  };
  const tile = byteView("tilesSection");
  const data = byteView("dataSection");
  const uint = (i: number) => tile.getUint32(i * 4, true);
  const tileCount = uint(1) * uint(2);
  const entryBegin = 4 + tileCount;
  const entryCount = uint(3 + tileCount);
  const lastTile = tile.byteLength / 4 - 1;
  const paintStart = lastTile - uint(lastTile);
  const rows = new Set<number>();
  for (let i = 0; i < entryCount; i++) rows.add(uint(entryBegin + i));
  const float = (i: number) => data.getFloat32(i * 4, true);
  const paint = (i: number) => tile.getFloat32(i * 4, true);
  const images = [];
  for (const row of rows) {
    for (const field of [2, 3]) {
      const pos = (row + field) * 4;
      if (float(pos + 3) >= -1.5) continue;
      const r = paintStart + float(pos);
      const width = Math.abs(paint(r + 3));
      const height = Math.abs(paint(r + 7));
      const pixels = paintStart + paint(r + 8);
      if (!Number.isSafeInteger(width) || !Number.isSafeInteger(height) ||
          pixels < r + 9 || pixels + width * height > lastTile) {
        throw new Error(`invalid bitmap header at ${r}`);
      }
      if (width < 80 || height < 60) continue;
      const map = [paint(r), paint(r + 1), paint(r + 2), paint(r + 4), paint(r + 5), paint(r + 6)];
      const bounds = [float(row * 4), float(row * 4 + 1), float(row * 4 + 2), float(row * 4 + 3)];
      const rgba = new Uint8Array(tile.buffer, tile.byteOffset + pixels * 4, width * height * 4);
      const key = `${job.file}-${row}-${field}`;
      const digest = await crypto.subtle.digest("SHA-256", rgba);
      const sha256 = Array.from(new Uint8Array(digest), x => x.toString(16).padStart(2, "0")).join("");
      images.push({key, bounds, map, width, height, sha256});
    }
  }
  await Deno.writeTextFile(`out/${job.file}-paint-bitmap.json`, JSON.stringify(images, null, 2));
"""
runner.write_text(source.replace(anchor, anchor + probe))
