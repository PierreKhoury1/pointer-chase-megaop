## Codex Continuation Handoff

### Project scope
Pointer-chase study across:
- AOT structural extraction
- HotSpot/JIT structural proxies and runtime measurements
- Native C atomic-chase prototype
- Slide-ready summaries and plots

### Current organized layout
- `experiments/aot/`
- `experiments/hotspot/`
- `experiments/atomic_chase/`
- `analysis/`
- `slides/`
- `docs/`

### Key files by area

#### AOT
- Scripts: `experiments/aot/scripts/*.py`
- Generated source: `experiments/aot/generated/generated_pointer_chase.c`
- Assembly snapshots: `experiments/aot/asm/*.s`
- Data: `experiments/aot/data/raw/*.csv`, `experiments/aot/data/processed/*.md`
- Plots: `experiments/aot/plots/`

#### HotSpot
- Java sources: `experiments/hotspot/src/*.java`
- Scripts: `experiments/hotspot/scripts/*.py`
- JNI: `experiments/hotspot/jni/ptrchase.c`
- Logs: `experiments/hotspot/logs/`
- Data: `experiments/hotspot/data/raw/*.csv`, `experiments/hotspot/data/processed/*.md`
- Plots: `experiments/hotspot/plots/`

#### Atomic chase (C)
- Sources: `experiments/atomic_chase/src/*`
- Scripts: `experiments/atomic_chase/scripts/*.py`
- Data: `experiments/atomic_chase/data/raw/*`, `experiments/atomic_chase/data/processed/*`
- Plots: `experiments/atomic_chase/plots/`
- IR analysis: `experiments/atomic_chase/analysis/ir_megaop/`

#### Cross-layer analysis
- Data: `analysis/data/*.csv`
- Reports: `analysis/reports/*`
- Metadata: `analysis/metadata/system_info.json`

### Reproduce key outputs

```bash
python3 experiments/aot/scripts/measure_pointer_chasing.py
python3 experiments/aot/scripts/plot_results.py
python3 experiments/aot/scripts/combine_aot_hotspot.py
python3 experiments/aot/scripts/measure_hotspot.py
```

```bash
cd experiments/atomic_chase
make
python3 scripts/measure_callgrind.py
python3 scripts/measure_perf.py
```

### Environment notes
- Linux/WSL with: `gcc`, `clang`, `python3`, `matplotlib`, `valgrind`.
- For slides: `texlive-latex-recommended`, `texlive-latex-extra`.
- HotSpot: OpenJDK 21.

### Known constraints
- WSL often lacks reliable hardware perf counters; callgrind is used as fallback.
- HotSpot structural metrics are proxy-based unless using debug JVM internals.
