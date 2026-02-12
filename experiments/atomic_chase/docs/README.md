# Atomic Chase (Proof-of-Concept)

This folder models a semantic "mega-instruction" for pointer chasing by
collapsing multi-step dereferences into a single speculative region.
It is intentionally small and benchmark-focused.

## What "atomic chase" means

`chase_atomic` first performs *all* null checks for a fixed depth and
then executes a straight-line dataflow region (no branches) that performs
the chained dereferences and returns the final value.

This models a hypothetical instruction that treats the entire chase as
one speculative unit: checks are separated from the dataflow, and the
dataflow has a single return point.

## Files

- `chase.h` / `chase.c`: baseline and atomic chase implementations
- `bench.c`: tight-loop benchmark harness
- `Makefile`: builds `bench` with `-O2` and `bench_O3` with `-O3`

## Build

```sh
make
```

## Run perf

```sh
perf stat -e instructions,cycles,branches,branch-misses ./bench
```

## Targeted runs

You can benchmark a single depth or a single mode:

```sh
./bench 5
./bench_naive 5
./bench_atomic 5
```

## What to expect (no guarantees)

- `chase_atomic` should reduce dynamic branches vs `chase_naive`
- fewer branches can reduce branch misses
- instruction count may drop due to the collapsed control flow

This is a proof-of-concept for control-flow collapse, not a production library.

## Note on depth

The benchmark uses depths {2, 3, 5, 8}. The chain builder allocates
`depth + 1` nodes so that `depth` dereferences are valid.
