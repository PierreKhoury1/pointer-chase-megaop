# Path Migration Map

## Top-level moves
- `atomic_chase/` -> `experiments/atomic_chase/`
- `hotspot/` -> `experiments/hotspot/`
- `build/` + `scripts/aot/` -> `experiments/aot/`
- `results/` -> `analysis/`
- `metadata/` -> `analysis/metadata/`
- `CODEX_CONTINUATION.md` -> `docs/notes/CODEX_CONTINUATION.md`
- `info.txt` -> `docs/notes/info.txt`

## Example file moves
- `measure_pointer_chasing.py` -> `experiments/aot/scripts/measure_pointer_chasing.py`
- `measure_hotspot.py` -> `experiments/aot/scripts/measure_hotspot.py`
- `hotspot/ContractBench.java` -> `experiments/hotspot/src/ContractBench.java`
- `atomic_chase/results_perf.csv` -> `experiments/atomic_chase/data/raw/results_perf.csv`
- `atomic_chase/graphs/contract/*.png` -> `experiments/atomic_chase/plots/contract/*.png`
