import L4Factoidal.Codec.VP8Intra

open L4Factoidal.Codec VP8

private def appendCrop (output : ByteArray) (plane : ByteArray) (stride width height : Nat) :
    ByteArray := Id.run do
  let mut bytes := output
  for row in [:height] do
    bytes := plane.copySlice (row*stride) bytes bytes.size width false
  return bytes

private def decode (src : ByteArray) : Except String ByteArray := do
  let image ← WebP.inspect src
  let frame ← VP8.reconstruct src image
  if frame.y.size != frame.rows*frame.columns*256 ||
      frame.u.size != frame.rows*frame.columns*64 || frame.v.size != frame.u.size then
    throw "unexpected padded VP8 plane size"
  let uvWidth := (image.width+1)/2
  let uvHeight := (image.height+1)/2
  let bytes := ByteArray.emptyWithCapacity (image.width*image.height+2*uvWidth*uvHeight)
  let bytes := appendCrop bytes frame.y (16*frame.columns) image.width image.height
  let bytes := appendCrop bytes frame.u (8*frame.columns) uvWidth uvHeight
  return appendCrop bytes frame.v (8*frame.columns) uvWidth uvHeight

def main (args : List String) : IO Unit := do
  let [input, output] := args | throw (IO.userError "usage: probe input.webp output.yuv")
  let src ← IO.FS.readBinFile input
  match decode src with
  | .error err => throw (IO.userError (input ++ ": " ++ err))
  | .ok bytes => IO.FS.writeBinFile output bytes
