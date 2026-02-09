## perf stat (detailed stalls)

- perf binary: `/usr/bin/perf`
- taskset: `-c 0`
- depth: `8`

### L1 (nodes=2048, iters=5000000)

| metric | guarded | contract |
|---|---:|---:|
| cycles | 141.564M | 77.879M |
| instructions | 353.892M | 202.544M |
| branches | 108.778M | 41.799M |
| branch-misses | 48.856k | 40.017k |
| stalled-cycles-frontend | n/a | n/a |
| stalled-cycles-backend | n/a | n/a |
| cache-references | 599.951k | 538.041k |
| cache-misses | 50.876k | 16.321k |
| LLC-loads | 36.751k | 27.970k |
| LLC-load-misses | 5.695k | 2.856k |
| L1-dcache-loads | 60.662M | 65.975M |
| L1-dcache-load-misses | 3.041M | 473.061k |
| dTLB-loads | 59.825M | 65.309M |
| dTLB-load-misses | 1.714k | 655.000 |

| derived metric | guarded | contract |
|---|---:|---:|
| IPC | 2.500 | 2.601 |
| % frontend stalls | n/a | n/a |
| % backend stalls | n/a | n/a |
| branch miss rate | 0.04% | 0.10% |
| cache miss rate | 8.48% | 3.03% |
| L1d miss rate | 5.01% | 0.72% |
| LLC miss rate | 15.50% | 10.21% |
| dTLB miss rate | 0.00% | 0.00% |
| cycles per LLC miss | 24.858k | 27.269k |

### L2 (nodes=16384, iters=3000000)

| metric | guarded | contract |
|---|---:|---:|
| cycles | 178.592M | 152.134M |
| instructions | 211.958M | 130.925M |
| branches | 61.336M | 26.829M |
| branch-misses | 45.354k | 53.359k |
| stalled-cycles-frontend | n/a | n/a |
| stalled-cycles-backend | n/a | n/a |
| cache-references | 24.386M | 19.914M |
| cache-misses | 220.693k | 224.310k |
| LLC-loads | 5.715M | 5.680M |
| LLC-load-misses | 16.870k | 22.700k |
| L1-dcache-loads | 40.161M | 40.047M |
| L1-dcache-load-misses | 26.365M | 26.205M |
| dTLB-loads | 38.982M | 38.783M |
| dTLB-load-misses | 742.000 | 1.639k |

| derived metric | guarded | contract |
|---|---:|---:|
| IPC | 1.187 | 0.861 |
| % frontend stalls | n/a | n/a |
| % backend stalls | n/a | n/a |
| branch miss rate | 0.07% | 0.20% |
| cache miss rate | 0.90% | 1.13% |
| L1d miss rate | 65.65% | 65.44% |
| LLC miss rate | 0.30% | 0.40% |
| dTLB miss rate | 0.00% | 0.00% |
| cycles per LLC miss | 10.586k | 6.702k |

### L3 (nodes=524288, iters=1000000)

| metric | guarded | contract |
|---|---:|---:|
| cycles | 346.089M | 376.199M |
| instructions | 107.250M | 82.326M |
| branches | 26.027M | 14.611M |
| branch-misses | 58.156k | 79.784k |
| stalled-cycles-frontend | n/a | n/a |
| stalled-cycles-backend | n/a | n/a |
| cache-references | 28.953M | 26.873M |
| cache-misses | 9.911M | 13.508M |
| LLC-loads | 8.922M | 9.698M |
| LLC-load-misses | 3.010M | 5.040M |
| L1-dcache-loads | 20.299M | 21.381M |
| L1-dcache-load-misses | 12.877M | 12.592M |
| dTLB-loads | 20.086M | 19.289M |
| dTLB-load-misses | 2.511M | 2.711M |

| derived metric | guarded | contract |
|---|---:|---:|
| IPC | 0.310 | 0.219 |
| % frontend stalls | n/a | n/a |
| % backend stalls | n/a | n/a |
| branch miss rate | 0.22% | 0.55% |
| cache miss rate | 34.23% | 50.26% |
| L1d miss rate | 63.44% | 58.89% |
| LLC miss rate | 33.74% | 51.97% |
| dTLB miss rate | 12.50% | 14.06% |
| cycles per LLC miss | 114.969 | 74.643 |

### DRAM (nodes=4194304, iters=500000)

| metric | guarded | contract |
|---|---:|---:|
| cycles | 858.473M | 797.728M |
| instructions | 372.394M | 347.353M |
| branches | 53.725M | 46.334M |
| branch-misses | 163.393k | 146.000k |
| stalled-cycles-frontend | n/a | n/a |
| stalled-cycles-backend | n/a | n/a |
| cache-references | 49.124M | 44.891M |
| cache-misses | 32.136M | 28.995M |
| LLC-loads | 12.661M | 12.391M |
| LLC-load-misses | 6.856M | 6.839M |
| L1-dcache-loads | 58.834M | 57.799M |
| L1-dcache-load-misses | 24.369M | 25.499M |
| dTLB-loads | 59.218M | 54.505M |
| dTLB-load-misses | 5.300M | 5.693M |

| derived metric | guarded | contract |
|---|---:|---:|
| IPC | 0.434 | 0.435 |
| % frontend stalls | n/a | n/a |
| % backend stalls | n/a | n/a |
| branch miss rate | 0.30% | 0.32% |
| cache miss rate | 65.42% | 64.59% |
| L1d miss rate | 41.42% | 44.12% |
| LLC miss rate | 54.15% | 55.20% |
| dTLB miss rate | 8.95% | 10.45% |
| cycles per LLC miss | 125.215 | 116.636 |

