import L4Factoidal.Codec.WebP
import L4Factoidal.Codec.VP8LPrefix

open L4Factoidal.Codec

private def testPixels (count : Nat) : BitM (Array Nat) := do
  if (← readBits 3) != 0 then throw "literal fixture requires zero feature flags"
  let codes ← VP8L.readGroup 0
  let mut out := #[]
  for _ in [0:count] do
    let green := (← VP8L.readSymbol codes.green).val
    let red := (← VP8L.readSymbol codes.red).val
    let blue := (← VP8L.readSymbol codes.blue).val
    let alpha := (← VP8L.readSymbol codes.alpha).val
    out := out.push red |>.push green |>.push blue |>.push alpha
  return out

private def check (src : ByteArray) : Except String (Array Nat) := do
  let image ← WebP.inspect src
  if image.encoding != .vp8l then throw "expected VP8L"
  let span := image.pixels
  let (pixels, _) ← (testPixels (image.width * image.height)).run
    {data := src.extract (span.offset + 5) (span.offset + span.size), pos := 0}
  return pixels

def main (args : List String) : IO Unit := do
  for path in args do
    let src ← IO.FS.readBinFile path
    match check src with
    | .error msg => throw (IO.userError (path ++ ": " ++ msg))
    | .ok pixels =>
      IO.println (path ++ "\t" ++ String.intercalate "," (pixels.toList.map toString))
