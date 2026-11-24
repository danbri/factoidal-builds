import L4Factoidal.Codec.WebP

open L4Factoidal.Codec.WebP

def main (paths : List String) : IO Unit := do
  for path in paths do
    let bytes ← IO.FS.readBinFile path
    match inspect bytes with
    | .error err => throw (IO.userError s!"{path}: {err}")
    | .ok image =>
      IO.println s!"{path}\t{repr image.encoding}\t{image.width}\t{image.height}\t{image.alpha.isSome}"
