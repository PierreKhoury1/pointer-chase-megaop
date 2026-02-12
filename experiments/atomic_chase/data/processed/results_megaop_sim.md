## Mega-op simulator (fixed-latency op)

- baseline model: guarded pointer-chase loop
- baseline fixed overhead: `2.0` cycles
- baseline per-hop overhead: guard `2.0` + loop `1.0` cycles
- mega-op overhead: `2.0` cycles
- per-hop memory latency assumptions (cycles):
  - L1: 4.0
  - L2: 12.0
  - L3: 40.0
  - DRAM: 200.0

| workset | depth | baseline cycles/iter | mega-op cycles/iter | speedup |
|---|---:|---:|---:|---:|
| L1 | 2 | 16.000 | 10.000 | 1.600 |
| L1 | 3 | 23.000 | 14.000 | 1.643 |
| L1 | 5 | 37.000 | 22.000 | 1.682 |
| L1 | 8 | 58.000 | 34.000 | 1.706 |
| L2 | 2 | 32.000 | 26.000 | 1.231 |
| L2 | 3 | 47.000 | 38.000 | 1.237 |
| L2 | 5 | 77.000 | 62.000 | 1.242 |
| L2 | 8 | 122.000 | 98.000 | 1.245 |
| L3 | 2 | 88.000 | 82.000 | 1.073 |
| L3 | 3 | 131.000 | 122.000 | 1.074 |
| L3 | 5 | 217.000 | 202.000 | 1.074 |
| L3 | 8 | 346.000 | 322.000 | 1.075 |
| DRAM | 2 | 408.000 | 402.000 | 1.015 |
| DRAM | 3 | 611.000 | 602.000 | 1.015 |
| DRAM | 5 | 1017.000 | 1002.000 | 1.015 |
| DRAM | 8 | 1626.000 | 1602.000 | 1.015 |

### Avg speedup by workset

| workset | avg speedup |
|---|---:|
| L1 | 1.658 |
| L2 | 1.239 |
| L3 | 1.074 |
| DRAM | 1.015 |
