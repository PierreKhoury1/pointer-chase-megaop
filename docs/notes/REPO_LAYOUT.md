# Repository Layout (Strict)

## Top-level
- `experiments/`: all benchmark code, measurement scripts, raw data, processed data, logs, and plots.
- `analysis/`: cross-experiment merged outputs and summary narratives.
- `slides/`: deck sources and exported PDFs.
- `docs/`: working notes and screenshots.

## Experiments

### `experiments/aot/`
- `scripts/`: AOT/JIT extraction + plotting pipeline scripts.
- `asm/`: emitted assembly snapshots.
- `generated/`: generated C sources.
- `data/raw/`: CSV outputs.
- `data/processed/`: markdown summaries.
- `plots/`: chart outputs.
- `logs/`: parser/compiler logs.
- `hotspot_bridge/`: bridge artifacts used in cross-layer AOT vs HotSpot comparisons.

### `experiments/hotspot/`
- `src/`: Java benchmark implementations.
- `scripts/`: HotSpot measurement scripts.
- `jni/`: JNI sources.
- `data/raw/`: CSV outputs.
- `data/processed/`: markdown summaries.
- `plots/`: chart outputs.
- `logs/`: compiler/runtime/perf logs.

### `experiments/atomic_chase/`
- `src/`: C sources and headers.
- `scripts/`: perf/callgrind/plot scripts.
- `data/raw/`: CSV/TXT/callgrind dumps.
- `data/processed/`: markdown summaries.
- `plots/`: generated visualizations.
- `analysis/ir_megaop/`: IR-focused analysis artifacts.
- `docs/`: experiment-local notes.

## Analysis + Docs
- `analysis/data/`: merged CSV tables.
- `analysis/reports/`: markdown/txt narrative summaries.
- `analysis/metadata/`: host/system metadata.
- `docs/notes/`: Codex handoff and design notes.
- `docs/screenshots/`: reference images.

## Cleanup policy
Removed as non-essential tracked artifacts:
- Java `.class` files.
- Benchmark executables and shared libs.
- LaTeX aux outputs (`.aux`, `.nav`, `.out`, `.snm`, `.toc`, `.vrb`, `.fls`, `.fdb_latexmk`).
