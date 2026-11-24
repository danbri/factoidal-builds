import L4Factoidal.Codec.VP8Alpha

open L4Factoidal.Codec

def main (args : List String) : IO Unit := do
  let [input, output] := args | throw (IO.userError "usage: probe input.webp output.rgba")
  let src ← IO.FS.readBinFile input
  match VP8.decode src with
  | .error err => throw (IO.userError (input ++ ": " ++ err))
  | .ok result => IO.FS.writeBinFile output result.pixels
