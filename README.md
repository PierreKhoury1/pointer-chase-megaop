# Pointer Chasing Mega-Instruction Study

This repository studies pointer-chase behavior across AOT, HotSpot, and native C experiments, then compares structural effects (loads, branches, checks) against measured latency behavior.

## Strict Layout

- `experiments/aot/`: AOT generation, assembly, cross-layer merge, and AOT plots.
- `experiments/hotspot/`: Java sources, HotSpot scripts, logs, data, and plots.
- `experiments/atomic_chase/`: native C pointer-chase prototype with perf/callgrind data and plots.
- `analysis/`: cross-experiment summary tables/reports and metadata.
- `slides/`: presentation decks (`.tex/.pdf`) and slide assets (`plots/`, `tables/`).
- `docs/notes/`: handoff and working notes.
- `docs/screenshots/`: reference screenshots.

## Experiment Substructure

Each experiment area uses the same pattern where possible:

- `src/`: source code
- `scripts/`: measurement/plotting scripts
- `data/raw/`: CSV/TXT/raw counter outputs
- `data/processed/`: markdown summaries
- `plots/`: generated figures
- `logs/`: runtime/compiler logs (when applicable)

## Important Paths

### AOT
- Scripts: `experiments/aot/scripts/`
- Assembly: `experiments/aot/asm/`
- Generated source: `experiments/aot/generated/generated_pointer_chase.c`
- Data: `experiments/aot/data/raw/`, `experiments/aot/data/processed/`
- Plots: `experiments/aot/plots/`

### HotSpot
- Java: `experiments/hotspot/src/`
- Scripts: `experiments/hotspot/scripts/`
- JNI: `experiments/hotspot/jni/`
- Logs: `experiments/hotspot/logs/`
- Data: `experiments/hotspot/data/raw/`, `experiments/hotspot/data/processed/`
- Plots: `experiments/hotspot/plots/`

### Atomic Chase (C)
- Sources: `experiments/atomic_chase/src/`
- Scripts: `experiments/atomic_chase/scripts/`
- Data: `experiments/atomic_chase/data/raw/`, `experiments/atomic_chase/data/processed/`
- Plots: `experiments/atomic_chase/plots/`
- IR analysis: `experiments/atomic_chase/analysis/ir_megaop/`

## Reproduce (high level)

### AOT
```bash
python3 experiments/aot/scripts/measure_pointer_chasing.py
python3 experiments/aot/scripts/plot_results.py
python3 experiments/aot/scripts/combine_aot_hotspot.py
```

### HotSpot
```bash
python3 experiments/aot/scripts/measure_hotspot.py
# and/or
python3 experiments/hotspot/scripts/measure_contract_jit_perf.py
```

### Atomic Chase
```bash
cd experiments/atomic_chase
make
python3 scripts/measure_callgrind.py
python3 scripts/measure_perf.py
```

## Notes

- Generated binaries (`.class`, `.so`, benchmark executables) are not kept in the tracked layout.
- LaTeX auxiliary files are ignored; only slide sources and final PDFs are retained.
