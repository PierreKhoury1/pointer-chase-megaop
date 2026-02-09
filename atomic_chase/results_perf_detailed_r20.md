## perf stat (detailed stalls)

- perf binary: `/usr/bin/perf`
- taskset: `-c 0`
- depth: `8`
- repeats: `20`

### L3 (nodes=524288, iters=1000000)

| metric | guarded | contract |
|---|---:|---:|
| cycles | 344.933M | 237.295M |
| instructions | 109.897M | 79.651M |
| branches | 26.960M | 14.031M |
| branch-misses | 69.325k | 61.196k |
| stalled-cycles-frontend | n/a | n/a |
| stalled-cycles-backend | n/a | n/a |
| cache-references | 29.402M | 27.374M |
| cache-misses | 11.428M | 9.142M |
| LLC-loads | 9.335M | 9.225M |
| LLC-load-misses | 3.630M | 3.071M |
| L1-dcache-loads | 21.311M | 21.135M |
| L1-dcache-load-misses | 12.272M | 12.079M |
| dTLB-loads | 19.825M | 19.654M |
| dTLB-load-misses | 2.464M | 2.366M |
| iTLB-loads | 2.204k | 1.604k |
| iTLB-load-misses | 5.380k | 3.703k |

| derived metric | guarded | contract |
|---|---:|---:|
| IPC | 0.319 | 0.336 |
| % frontend stalls | n/a | n/a |
| % backend stalls | n/a | n/a |
| branch miss rate | 0.26% | 0.44% |
| cache miss rate | 38.87% | 33.40% |
| L1d miss rate | 57.58% | 57.15% |
| LLC miss rate | 38.89% | 33.29% |
| dTLB miss rate | 12.43% | 12.04% |
| cycles per LLC miss | 95.026 | 77.264 |
| cycles stddev | 7.623M | 2.705M |

### DRAM (nodes=4194304, iters=500000)

| metric | guarded | contract |
|---|---:|---:|
| cycles | 751.625M | 628.670M |
| instructions | 367.832M | 355.524M |
| branches | 52.767M | 46.725M |
| branch-misses | 141.196k | 136.571k |
| stalled-cycles-frontend | n/a | n/a |
| stalled-cycles-backend | n/a | n/a |
| cache-references | 48.577M | 45.064M |
| cache-misses | 31.588M | 29.216M |
| LLC-loads | 11.956M | 11.860M |
| LLC-load-misses | 6.289M | 6.110M |
| L1-dcache-loads | 61.347M | 59.640M |
| L1-dcache-load-misses | 23.645M | 23.590M |
| dTLB-loads | 59.928M | 58.300M |
| dTLB-load-misses | 5.247M | 5.264M |
| iTLB-loads | 22.368k | 22.338k |
| iTLB-load-misses | 49.322k | 48.356k |

| derived metric | guarded | contract |
|---|---:|---:|
| IPC | 0.489 | 0.566 |
| % frontend stalls | n/a | n/a |
| % backend stalls | n/a | n/a |
| branch miss rate | 0.27% | 0.29% |
| cache miss rate | 65.03% | 64.83% |
| L1d miss rate | 38.54% | 39.55% |
| LLC miss rate | 52.60% | 51.52% |
| dTLB miss rate | 8.75% | 9.03% |
| cycles per LLC miss | 119.514 | 102.894 |
| cycles stddev | 30.366M | 5.407M |

