import L4Factoidal.Codec.VP8LPlane
import L4Factoidal.Codec.WebP

open L4Factoidal.Codec

private def check (src : ByteArray) : Except String (Array Nat) := do
  let info ← WebP.inspect src
  if info.encoding != .vp8l then throw "expected a VP8L file"
  let span := info.pixels
  let read := do
    if (← readBit) != 0 then throw "plane probe needs a file with no transforms"
    VP8L.readPlane info.width info.height true
  let (image, _) ← read.run {data := src.extract (span.offset+5) (span.offset+span.size), pos := 0}
  return image.pixels.foldl (fun bytes pixel =>
    let x := pixel.toNat
    bytes.push (x / 65536 % 256) |>.push (x / 256 % 256) |>.push (x % 256) |>.push (x / 16777216)) #[]

def main (args : List String) : IO Unit := do
  for path in args do
    let src ← IO.FS.readBinFile path
    match check src with
    | .error err => throw (IO.userError (path ++ ": " ++ err))
    | .ok bytes => IO.println (path ++ "\t" ++ String.intercalate "," (bytes.toList.map toString))
