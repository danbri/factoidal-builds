import L4Factoidal.Codec.VP8Color

open L4Factoidal.Codec VP8

private def decode (src : ByteArray) (alpha : Option ByteArray) : Except String RgbaImage := do
  let image ← WebP.inspect src
  VP8.decodeColor src image alpha

def main (args : List String) : IO Unit := do
  let input :: output :: alphaFile := args | throw (IO.userError "usage: probe input.webp output.rgba [decoded.alpha]")
  let src ← IO.FS.readBinFile input
  let alpha ← match alphaFile with
    | [] => pure none
    | [path] => some <$> IO.FS.readBinFile path
    | _ => throw (IO.userError "too many alpha files")
  match decode src alpha with
  | .error err => throw (IO.userError (input ++ ": " ++ err))
  | .ok result => IO.FS.writeBinFile output result.pixels
