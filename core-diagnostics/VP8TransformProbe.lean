import L4Factoidal.Codec.VP8Transform

open L4Factoidal.Codec VP8

private def coefficientLine (block : CoefficientBlock) : String :=
  "@coeff " ++ String.intercalate " " (block.toArray.toList.map toString)

private def residualLines (lines : Array String) (_ : Control) (row column : Nat)
    (_ : Macroblock) (residual : Option SpatialResidual) : Except String (Array String) := do
  let mut lines := lines.push s!"@position {row} {column} {if residual.isNone then 1 else 0}"
  let some blocks := residual | return lines
  for block in blocks.toArray do
    lines := lines.push (coefficientLine block)
  return lines

private def decode (src : ByteArray) : Except String (Array String) := do
  let image ← WebP.inspect src
  VP8.foldSpatialResiduals src image #[] residualLines

def main (args : List String) : IO Unit := do
  for file in args do
    let src ← IO.FS.readBinFile file
    match decode src with
    | .error err => throw (IO.userError (file ++ ": " ++ err))
    | .ok lines =>
      for line in lines do
        IO.println line
