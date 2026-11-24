import L4Factoidal.Codec.VP8Control

open L4Factoidal.Codec VP8

private def modeList (modes : Array IntraMode) : String :=
  String.intercalate " " (modes.toList.map (toString ∘ IntraMode.index))

private def printPrediction (src : ByteArray) : Except String (List String) := do
  let image ← WebP.inspect src
  let result ← VP8.inspectPrediction src image
  let entropy := "@prob " ++ String.intercalate " "
    (result.entropy.probabilities.toList.map toString)
  let skip := "@skip " ++ (result.entropy.skipProbability.map toString).getD "-1"
  let modes := result.macroblocks.toList.map fun b =>
    let luma := match b.luma with
      | .whole mode => #[mode]
      | .subblocks modes => modes
    s!"@mb {b.segment} {if b.skipCoefficients then 1 else 0} {b.chroma.index} {modeList luma}"
  return entropy :: skip :: modes

def main (args : List String) : IO Unit := do
  for file in args do
    let src ← IO.FS.readBinFile file
    match printPrediction src with
    | .error err => throw (IO.userError (file ++ ": " ++ err))
    | .ok lines => for line in lines do IO.println line
