import L4Factoidal.Codec.VP8Control
import Lean

open Lean L4Factoidal.Codec

private def check (src : ByteArray) : Except String Json := do
  let image ← WebP.inspect src
  let result ← VP8.inspect src image
  let c := result.control
  let log := fun (n : Nat) => toJson n
  let b := fun (v : Bool) => log (if v then 1 else 0)
  let segment := match c.segmentation with
    | none => []
    | some s =>
      [("Update map", b s.mapUpdate), ("Update data", b s.dataUpdate)] ++
      (if s.dataUpdate then
        [("Absolute delta", b s.absolute), ("Quantizer", toJson s.quant),
         ("Filter strength", toJson s.filter)] else []) ++
      (if s.mapUpdate then [("Prob segment", toJson s.probabilities)] else [])
  let split := ["DQ Y1 DC","DQ Y2 DC","DQ Y2 AC","DQ UV DC","DQ UV AC"].zip c.quantDeltas.toList
  let fields := Json.mkObj ([
    ("Profile", log result.profile),
    ("Part. 0 length", log result.controlSpan.size),
    ("Width", log image.width), ("Height", log image.height),
    ("Color space", b c.colorSpace), ("Clamp type", b c.unclamped),
    ("Use segment", b c.segmentation.isSome),
    ("Simple filter", b c.simpleFilter), ("Level", log c.filterLevel), ("Sharpness", log c.sharpness),
    ("Use lf delta", b c.modeDeltas.isSome), ("Total partitions", log c.coefficientCount),
    ("Base Q", log c.baseQuant)] ++ segment ++ split.map (fun (k,v) => (k,toJson v)))
  let spans := result.coefficients.map (fun span => (span.offset, span.size))
  return Json.mkObj [("fields", fields), ("partitions", toJson spans)]

def main (args : List String) : IO Unit := do
  for path in args do
    let src ← IO.FS.readBinFile path
    match check src with
    | .error msg => throw (IO.userError (path ++ ": " ++ msg))
    | .ok record =>
      IO.println (Json.mkObj [("file", toJson path), ("result",record)]).compress
