## Execution Attempts

- Updated: 2026-02-05T14:33:23Z

### measure_pointer_chasing
- command: `python3 measure_pointer_chasing.py`
- exit_code: 0
- note: completed in WSL after toolchain install

### measure_hotspot
- command: `python3 measure_hotspot.py`
- exit_code: 0
- note: completed in WSL (OpenJDK 21)

### plot_results
- command: `python3 plot_results.py`
- exit_code: 0
- note: completed in WSL (matplotlib present)

### combine_aot_hotspot
- command: `python3 combine_aot_hotspot.py`
- exit_code: 0
- note: completed in WSL (matplotlib present)

### atomic_callgrind
- command: `cd atomic_chase && make clean && make && python3 measure_callgrind.py`
- exit_code: 0
- note: completed; regenerated callgrind csv/md/graphs

### atomic_perf
- command: `cd atomic_chase && python3 measure_perf.py`
- exit_code: 1
- note: failed: `perf` binary not found in current WSL image

