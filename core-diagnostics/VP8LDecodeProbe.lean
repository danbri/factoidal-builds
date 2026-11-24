import L4Factoidal.Codec.VP8LDecode

open L4Factoidal.Codec

def main (args : List String) : IO Unit := do
  for path in args do
    let bytes ← IO.FS.readBinFile path
    match VP8L.decode bytes with
    | .error err => throw (IO.userError (path ++ ": " ++ err))
    | .ok image =>
      IO.FS.writeBinFile (path ++ ".lean.rgba") image.rgba
      IO.println s!"{path}\t{image.width}\t{image.height}\t{image.rgba.size}"
