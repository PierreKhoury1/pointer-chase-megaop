# Pointer Chasing Mega-Instruction Study

This repo investigates how pointer chasing expands into loads, guards, and control flow in both AOT compilers and JITs, and then prototypes a semantic "mega-instruction" model (atomic chase) to motivate structural collapse.

## What is here

### 1) AOT evidence (C -> GCC/Clang)
We generate structurally comparable pointer-chase variants and count:
- load instructions
- branches
- basic blocks
- total instruction count

Key outputs:
- `build/results_aot.csv`, `build/results_aot.md`
- `build/graphs/combined_graphs/*.png`

### 2) HotSpot/JVM evidence
We mirror the same depth/pattern matrix in Java and log JIT data. Since product JVMs do not expose C2 IR nodes, we use bytecode parse proxies and `uncommon_trap` counts:
- deref ops (getfield/array loads)
- guards (null/type/range)
- deopts (uncommon_trap)
- IR proxy counts

Key outputs:
- `build/hotspot/results_hotspot.csv`, `build/hotspot/results_hotspot.md`
- `build/graphs/aot_vs_hotspot_graphs/*.png`

### 3) Atomic chase prototype (C)
We define a semantic "mega-instruction" model:
- **Naive**: pointer chase in a loop.
- **Atomic**: upfront null checks + straight-line dataflow + single return.

Code lives in `atomic_chase/` with:
- `chase.c/h` (implementations)
- `bench.c` (tight loop harness)
- `Makefile` (O2/O3, naive/atomic binaries)

### 4) Callgrind (WSL-safe) estimates
Because hardware perf counters are unavailable in WSL, we use Valgrind/Callgrind to estimate:
- instruction references (Ir)
- conditional branches (Bc)
- branch mispredicts (Bcm)

Key outputs:
- `atomic_chase/results_callgrind.csv`
- `atomic_chase/graphs_callgrind/*.png`

## Slides
The current narrative and graphs are compiled into:
- `slides/pointer_chase_slides.pdf`

Source:
- `slides/pointer_chase_slides.tex`

## How to reproduce (high level)

### AOT
```
python3 measure_pointer_chasing.py
python3 plot_results.py
python3 combine_aot_hotspot.py
```

### HotSpot
```
python3 measure_hotspot.py
```

### Atomic chase + Callgrind (WSL-safe)
```
# in WSL
make
python3 measure_callgrind.py
```

## Why this approach?
We want structural proof (not just timing):
- AOT shows the compiler's emitted structure.
- JIT shows guards/deopts that inflate the chase.
- If both scale as O(depth), a single semantic unit is justified.

The atomic chase prototype isolates control-flow collapse without changing algorithms.

## Current status
- AOT tables + graphs: done
- HotSpot proxy tables + graphs: done
- Atomic chase prototype: done
- Callgrind estimates: done
- Hardware perf (native Linux): pending

## Next steps
1. Run perf on native Linux and add true hardware counter graphs.
2. (Optional) fastdebug JVM for true C2 IR node counts.
3. Update slides with hardware-counter results.

