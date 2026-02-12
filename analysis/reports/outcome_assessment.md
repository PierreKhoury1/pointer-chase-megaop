## Outcome Assessment (Current executed run)

- Toolchain now available for GCC/Clang/JDK/Valgrind/Matplotlib.
- `perf` is still unavailable under current WSL image, so hardware-counter claims remain pending.

### O2 atomic vs naive
- depth 2: Ir ratio=1.158, Bc ratio=1.750.
- depth 3: Ir ratio=1.125, Bc ratio=1.800.
- depth 5: Ir ratio=0.966, Bc ratio=1.333.
- depth 8: Ir ratio=1.176, Bc ratio=1.857.

### O3 atomic vs naive
- depth 2: Ir ratio=1.158, Bc ratio=1.750.
- depth 3: Ir ratio=1.125, Bc ratio=1.800.
- depth 5: Ir ratio=0.966, Bc ratio=1.333.
- depth 8: Ir ratio=1.176, Bc ratio=1.857.

### Interpretation
- With current C implementations, atomic mode increases conditional branches across depths in Callgrind.
- JVM-side structural evidence still shows depth-scaled guards/deopts, supporting chain prevalence analysis.
- Need native Linux + perf to validate true backend stalls/MLP behavior.
