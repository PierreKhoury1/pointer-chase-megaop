## perf stat (detailed stalls)

- perf binary: `/usr/bin/perf`
- taskset: `-c 0`
- depth: `8`
- repeats: `1`

### L1 (nodes=2048, iters=5000000)

| metric | guarded | contract |
|---|---:|---:|
| cycles | 108.266M | 73.153M |
| instructions | 348.172M | 205.343M |
| branches | 104.584M | 42.069M |
| branch-misses | 48.347k | 41.339k |
| stalled-cycles-frontend | n/a | n/a |
| stalled-cycles-backend | n/a | n/a |
| cache-references | 641.421k | 559.835k |
| cache-misses | 120.205k | 58.663k |
| LLC-loads | 28.343k | 21.736k |
| LLC-load-misses | 10.690k | 6.856k |
| L1-dcache-loads | 62.817M | 63.129M |
| L1-dcache-load-misses | 521.783k | 441.535k |
| dTLB-loads | 63.029M | 64.694M |
| dTLB-load-misses | 561.000 | 167.000 |
| iTLB-loads | 782.000 | 1.073k |
| iTLB-load-misses | 473.000 | 307.000 |

| derived metric | guarded | contract |
|---|---:|---:|
| IPC | 3.216 | 2.807 |
| % frontend stalls | n/a | n/a |
| % backend stalls | n/a | n/a |
| branch miss rate | 0.05% | 0.10% |
| cache miss rate | 18.74% | 10.48% |
| L1d miss rate | 0.83% | 0.70% |
| LLC miss rate | 37.72% | 31.54% |
| dTLB miss rate | 0.00% | 0.00% |
| cycles per LLC miss | 10.128k | 10.670k |

### L2 (nodes=16384, iters=3000000)

| metric | guarded | contract |
|---|---:|---:|
| cycles | 184.086M | 133.152M |
| instructions | 221.379M | 138.782M |
| branches | 65.164M | 28.758M |
| branch-misses | 46.455k | 44.182k |
| stalled-cycles-frontend | n/a | n/a |
| stalled-cycles-backend | n/a | n/a |
| cache-references | 25.370M | 24.685M |
| cache-misses | 119.745k | 172.430k |
| LLC-loads | 7.438M | 6.472M |
| LLC-load-misses | 6.443k | 3.126k |
| L1-dcache-loads | 36.453M | 35.853M |
| L1-dcache-load-misses | 24.547M | 23.647M |
| dTLB-loads | 37.885M | 35.858M |
| dTLB-load-misses | 162.000 | 487.000 |
| iTLB-loads | 1.477k | 864.000 |
| iTLB-load-misses | 481.000 | 403.000 |

| derived metric | guarded | contract |
|---|---:|---:|
| IPC | 1.203 | 1.042 |
| % frontend stalls | n/a | n/a |
| % backend stalls | n/a | n/a |
| branch miss rate | 0.07% | 0.15% |
| cache miss rate | 0.47% | 0.70% |
| L1d miss rate | 67.34% | 65.96% |
| LLC miss rate | 0.09% | 0.05% |
| dTLB miss rate | 0.00% | 0.00% |
| cycles per LLC miss | 28.572k | 42.595k |

### L3 (nodes=524288, iters=1000000)

| metric | guarded | contract |
|---|---:|---:|
| cycles | 305.287M | 235.774M |
| instructions | 112.279M | 83.061M |
| branches | 28.666M | 14.347M |
| branch-misses | 64.635k | 69.133k |
| stalled-cycles-frontend | n/a | n/a |
| stalled-cycles-backend | n/a | n/a |
| cache-references | 29.263M | 28.419M |
| cache-misses | 9.229M | 8.641M |
| LLC-loads | 8.793M | 9.596M |
| LLC-load-misses | 2.841M | 3.009M |
| L1-dcache-loads | 19.612M | 20.106M |
| L1-dcache-load-misses | 11.783M | 12.092M |
| dTLB-loads | 16.761M | 19.197M |
| dTLB-load-misses | 2.299M | 2.324M |
| iTLB-loads | 542.000 | 1.970k |
| iTLB-load-misses | 2.910k | 3.914k |

| derived metric | guarded | contract |
|---|---:|---:|
| IPC | 0.368 | 0.352 |
| % frontend stalls | n/a | n/a |
| % backend stalls | n/a | n/a |
| branch miss rate | 0.23% | 0.48% |
| cache miss rate | 31.54% | 30.41% |
| L1d miss rate | 60.08% | 60.14% |
| LLC miss rate | 32.31% | 31.36% |
| dTLB miss rate | 13.72% | 12.11% |
| cycles per LLC miss | 107.473 | 78.347 |

### DRAM (nodes=4194304, iters=500000)

| metric | guarded | contract |
|---|---:|---:|
| cycles | 685.112M | 611.754M |
| instructions | 345.516M | 340.255M |
| branches | 50.544M | 45.159M |
| branch-misses | 139.229k | 128.804k |
| stalled-cycles-frontend | n/a | n/a |
| stalled-cycles-backend | n/a | n/a |
| cache-references | 45.770M | 46.473M |
| cache-misses | 30.247M | 30.017M |
| LLC-loads | 11.217M | 11.865M |
| LLC-load-misses | 5.938M | 6.024M |
| L1-dcache-loads | 63.799M | 65.361M |
| L1-dcache-load-misses | 23.786M | 23.099M |
| dTLB-loads | 54.487M | 58.193M |
| dTLB-load-misses | 5.533M | 5.074M |
| iTLB-loads | 22.199k | 21.725k |
| iTLB-load-misses | 44.544k | 57.316k |

| derived metric | guarded | contract |
|---|---:|---:|
| IPC | 0.504 | 0.556 |
| % frontend stalls | n/a | n/a |
| % backend stalls | n/a | n/a |
| branch miss rate | 0.28% | 0.29% |
| cache miss rate | 66.08% | 64.59% |
| L1d miss rate | 37.28% | 35.34% |
| LLC miss rate | 52.93% | 50.78% |
| dTLB miss rate | 10.15% | 8.72% |
| cycles per LLC miss | 115.386 | 101.547 |

