## HotSpot (C2) pointer-chase metrics

| pattern | depth | deref_ops | guards | deopts | ir_nodes |
|---|---:|---:|---:|---:|---:|
| plain | 2 | 2 | 2 | 2 | 2 |
| plain | 3 | 3 | 3 | 3 | 3 |
| plain | 5 | 5 | 5 | 5 | 5 |
| plain | 8 | 8 | 8 | 8 | 8 |
| const | 2 | 4 | 6 | 6 | 6 |
| const | 3 | 6 | 9 | 9 | 9 |
| const | 5 | 10 | 15 | 15 | 15 |
| const | 8 | 16 | 24 | 24 | 24 |
| dyn | 2 | 2 | 6 | 6 | 4 |
| dyn | 3 | 3 | 9 | 9 | 6 |
| dyn | 5 | 5 | 15 | 15 | 10 |
| dyn | 8 | 8 | 24 | 24 | 16 |
| checks | 2 | 2 | 4 | 16 | 12 |
| checks | 3 | 3 | 6 | 24 | 18 |
| checks | 5 | 5 | 10 | 40 | 30 |
| checks | 8 | 8 | 16 | 64 | 48 |

Notes:
- deref_ops: count of bytecode ops `getfield/getstatic` and array loads within the parse for the highest-level compile.
- guards: count of `uncommon_trap` entries with reasons like null/range/type/class checks.
- deopts: total `uncommon_trap` count in the parse (proxy for side-exit points).
- ir_nodes: proxy = total bytecode count in the parse for the highest-level compile.
- For true C2 IR node counts, a fastdebug JVM with `PrintIdealGraphFile` is required.
- Tiered compilation is disabled (`-XX:-TieredCompilation`) to capture a single C2-style compile.
