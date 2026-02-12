## Executed Summary

### Formation trend (JVM proxies)
- plain: d2: deref=2, guards=2, deopts=2; d3: deref=3, guards=3, deopts=3; d5: deref=5, guards=5, deopts=5; d8: deref=8, guards=8, deopts=8
- checks: d2: deref=2, guards=4, deopts=16; d3: deref=3, guards=6, deopts=24; d5: deref=5, guards=10, deopts=40; d8: deref=8, guards=16, deopts=64

### Latency manifestation trend (Callgrind proxy)
- O2:
  - d2: atomic/naive Ir=1.158, Bc=1.750
  - d3: atomic/naive Ir=1.125, Bc=1.800
  - d5: atomic/naive Ir=0.966, Bc=1.333
  - d8: atomic/naive Ir=1.176, Bc=1.857
- O3:
  - d2: atomic/naive Ir=1.158, Bc=1.750
  - d3: atomic/naive Ir=1.125, Bc=1.800
  - d5: atomic/naive Ir=0.966, Bc=1.333
  - d8: atomic/naive Ir=1.176, Bc=1.857
