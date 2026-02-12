CC ?= cc
CFLAGS_COMMON = -std=c11 -Wall -Wextra -Wpedantic

.PHONY: all clean

all: bench bench_O3 bench_naive bench_atomic bench_naive_O3 bench_atomic_O3 \
	contract_guarded contract_contract contract_guarded_O3 contract_contract_O3 \
	contract_guarded_mt contract_contract_mt contract_guarded_mt_O3 contract_contract_mt_O3

bench:
	$(CC) $(CFLAGS_COMMON) -O2 -o bench chase.c bench.c

bench_O3:
	$(CC) $(CFLAGS_COMMON) -O3 -o bench_O3 chase.c bench.c

bench_naive:
	$(CC) $(CFLAGS_COMMON) -O2 -DONLY_NAIVE -o bench_naive chase.c bench.c

bench_atomic:
	$(CC) $(CFLAGS_COMMON) -O2 -DONLY_ATOMIC -o bench_atomic chase.c bench.c

bench_naive_O3:
	$(CC) $(CFLAGS_COMMON) -O3 -DONLY_NAIVE -o bench_naive_O3 chase.c bench.c

bench_atomic_O3:
	$(CC) $(CFLAGS_COMMON) -O3 -DONLY_ATOMIC -o bench_atomic_O3 chase.c bench.c

clean:
	rm -f bench bench_O3 bench_naive bench_atomic bench_naive_O3 bench_atomic_O3 \
		contract_guarded contract_contract contract_guarded_O3 contract_contract_O3 \
		contract_guarded_mt contract_contract_mt contract_guarded_mt_O3 contract_contract_mt_O3

contract_guarded:
	$(CC) $(CFLAGS_COMMON) -O2 -DONLY_GUARDED -o contract_guarded contract_chase.c contract_bench.c

contract_contract:
	$(CC) $(CFLAGS_COMMON) -O2 -DONLY_CONTRACT -o contract_contract contract_chase.c contract_bench.c

contract_guarded_O3:
	$(CC) $(CFLAGS_COMMON) -O3 -DONLY_GUARDED -o contract_guarded_O3 contract_chase.c contract_bench.c

contract_contract_O3:
	$(CC) $(CFLAGS_COMMON) -O3 -DONLY_CONTRACT -o contract_contract_O3 contract_chase.c contract_bench.c

contract_guarded_mt:
	$(CC) $(CFLAGS_COMMON) -O2 -pthread -o contract_guarded_mt contract_chase.c contract_bench_mt.c

contract_contract_mt:
	$(CC) $(CFLAGS_COMMON) -O2 -pthread -o contract_contract_mt contract_chase.c contract_bench_mt.c

contract_guarded_mt_O3:
	$(CC) $(CFLAGS_COMMON) -O3 -pthread -o contract_guarded_mt_O3 contract_chase.c contract_bench_mt.c

contract_contract_mt_O3:
	$(CC) $(CFLAGS_COMMON) -O3 -pthread -o contract_contract_mt_O3 contract_chase.c contract_bench_mt.c
