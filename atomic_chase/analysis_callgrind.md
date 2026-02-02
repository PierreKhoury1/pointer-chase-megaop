## Callgrind analysis (WSL-safe)

Key observations from `results_callgrind.csv` (Valgrind/Callgrind):

- **Branches increase in the atomic variant.**  
  Example (O2, depth 8):  
  - naive Bc = 70,025,310  
  - atomic Bc = 130,025,310 (≈ 1.86×)

- **Instruction references (Ir) are also higher for atomic.**  
  Example (O2, depth 8):  
  - naive Ir = 340,134,350  
  - atomic Ir = 400,134,350 (≈ 1.18×)

- **Mispredicts are low and nearly constant.**  
  Bcm stays ≈ 3.3k across depths and modes, indicating highly predictable
  branches in this synthetic benchmark.

Interpretation:
- The C-level “atomic” version **does not** reduce dynamic branches because
  each upfront null check is still a branch. The loop branch removed in the
  naive version is outweighed by the many explicit checks.
- This reinforces the core thesis: **structural collapse would need an ISA/JIT
  primitive** (or hardware support) to avoid per-check branch cost.

How to use this result:
- Treat Callgrind as a *software baseline* showing that “mega-instruction”
  semantics are not realized by source-level refactoring alone.
- The expected win remains at the architectural/semantic level, not in C code.
