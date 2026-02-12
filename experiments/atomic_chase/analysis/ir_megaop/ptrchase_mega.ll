; Minimal IR that models a fused pointer-chase mega-op as a single node.
; The intrinsic is hypothetical and represents a single semantic operation.

%struct.Node = type { ptr, i32 }

declare ptr @llvm.ptrchase(ptr, i32)

define ptr @chase_mega(ptr %p, i32 %depth) {
entry:
  %q = call ptr @llvm.ptrchase(ptr %p, i32 %depth)
  ret ptr %q
}
