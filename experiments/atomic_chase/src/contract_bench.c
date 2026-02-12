#include "contract_chase.h"

#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>

static volatile uint64_t sink;

static uint64_t run_guarded(Node *pool, size_t nodes, int depth, uint64_t iters) {
    uint64_t acc = 0;
    size_t idx = 0;
    size_t stride = 1315423911ULL % nodes;
    if (stride == 0) {
        stride = 1;
    }
    for (uint64_t i = 0; i < iters; i++) {
        idx += stride;
        if (idx >= nodes) {
            idx -= nodes;
        }
        acc ^= (uint64_t)chase_guarded(&pool[idx], depth);
    }
    return acc;
}

static uint64_t run_contract(Node *pool, size_t nodes, int depth, uint64_t iters) {
    uint64_t acc = 0;
    size_t idx = 0;
    size_t stride = 1315423911ULL % nodes;
    if (stride == 0) {
        stride = 1;
    }
    for (uint64_t i = 0; i < iters; i++) {
        idx += stride;
        if (idx >= nodes) {
            idx -= nodes;
        }
        acc ^= (uint64_t)chase_contract(&pool[idx], depth);
    }
    return acc;
}

static void usage(const char *prog) {
    fprintf(stderr, "usage: %s [depth] [nodes] [iters]\n", prog);
}

int main(int argc, char **argv) {
    int depth = 8;
    size_t nodes = (size_t)1 << 20;
    uint64_t iters = 2000000;

    if (argc > 1) {
        depth = atoi(argv[1]);
    }
    if (argc > 2) {
        nodes = (size_t)strtoull(argv[2], NULL, 10);
    }
    if (argc > 3) {
        iters = (uint64_t)strtoull(argv[3], NULL, 10);
    }
    if (depth <= 0 || nodes == 0 || iters == 0) {
        usage(argv[0]);
        return 1;
    }

    if ((size_t)depth >= nodes) {
        depth = (int)(nodes - 1);
    }

    Node *pool = build_pool(nodes, 0x12345678ULL);
    if (!pool) {
        fprintf(stderr, "failed to allocate pool\n");
        return 1;
    }

    uint64_t acc = 0;
#if defined(ONLY_GUARDED)
    acc ^= run_guarded(pool, nodes, depth, iters);
#elif defined(ONLY_CONTRACT)
    acc ^= run_contract(pool, nodes, depth, iters);
#else
    acc ^= run_guarded(pool, nodes, depth, iters);
    acc ^= run_contract(pool, nodes, depth, iters);
#endif
    sink = acc;

    if (sink == 42) {
        printf("unreachable\n");
    }

    free_pool(pool);
    return 0;
}
