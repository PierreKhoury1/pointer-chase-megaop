#include "contract_chase.h"

#include <inttypes.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    Node *pool;
    size_t nodes;
    int depth;
    uint64_t iters;
    int mode; // 0 = guarded, 1 = contract
    uint64_t acc;
} ThreadCtx;

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

static void *thread_main(void *arg) {
    ThreadCtx *ctx = (ThreadCtx *)arg;
    if (ctx->mode == 0) {
        ctx->acc = run_guarded(ctx->pool, ctx->nodes, ctx->depth, ctx->iters);
    } else {
        ctx->acc = run_contract(ctx->pool, ctx->nodes, ctx->depth, ctx->iters);
    }
    return NULL;
}

static void usage(const char *prog) {
    fprintf(stderr, "usage: %s <mode> <depth> <nodes> <iters> <threads>\n", prog);
    fprintf(stderr, "  mode: guarded | contract\n");
}

int main(int argc, char **argv) {
    if (argc < 6) {
        usage(argv[0]);
        return 1;
    }

    const char *mode_str = argv[1];
    int depth = atoi(argv[2]);
    size_t nodes = (size_t)strtoull(argv[3], NULL, 10);
    uint64_t iters = (uint64_t)strtoull(argv[4], NULL, 10);
    int threads = atoi(argv[5]);

    if (depth <= 0 || nodes == 0 || iters == 0 || threads <= 0) {
        usage(argv[0]);
        return 1;
    }

    int mode = -1;
    if (strcmp(mode_str, "guarded") == 0) {
        mode = 0;
    } else if (strcmp(mode_str, "contract") == 0) {
        mode = 1;
    } else {
        usage(argv[0]);
        return 1;
    }

    ThreadCtx *ctx = (ThreadCtx *)calloc((size_t)threads, sizeof(ThreadCtx));
    pthread_t *tids = (pthread_t *)calloc((size_t)threads, sizeof(pthread_t));
    if (!ctx || !tids) {
        fprintf(stderr, "allocation failed\n");
        return 1;
    }

    for (int i = 0; i < threads; i++) {
        ctx[i].pool = build_pool(nodes, (uint64_t)(0x12345678ULL + (uint64_t)i * 97ULL));
        if (!ctx[i].pool) {
            fprintf(stderr, "failed to allocate pool\n");
            return 1;
        }
        ctx[i].nodes = nodes;
        ctx[i].depth = depth;
        ctx[i].iters = iters;
        ctx[i].mode = mode;
        ctx[i].acc = 0;
    }

    for (int i = 0; i < threads; i++) {
        if (pthread_create(&tids[i], NULL, thread_main, &ctx[i]) != 0) {
            fprintf(stderr, "pthread_create failed\n");
            return 1;
        }
    }

    uint64_t acc = 0;
    for (int i = 0; i < threads; i++) {
        pthread_join(tids[i], NULL);
        acc ^= ctx[i].acc;
    }
    sink = acc;

    for (int i = 0; i < threads; i++) {
        free_pool(ctx[i].pool);
    }
    free(ctx);
    free(tids);

    if (sink == 42) {
        printf("unreachable\n");
    }
    return 0;
}
