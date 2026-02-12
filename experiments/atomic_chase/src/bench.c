#include "chase.h"

#include <stdio.h>
#include <stdlib.h>

#define ITERS 10000000

static volatile int sink;

static int run_naive(Node *head, int depth) {
    int acc = 0;
    for (int i = 0; i < ITERS; i++) {
        acc ^= chase_naive(head, depth);
    }
    return acc;
}

static int run_atomic(Node *head, int depth) {
    int acc = 0;
    for (int i = 0; i < ITERS; i++) {
        acc ^= chase_atomic(head, depth);
    }
    return acc;
}

static void run_depth(int depth) {
    Node *head = build_chain(depth);
    int acc = 0;
#if defined(ONLY_NAIVE)
    acc ^= run_naive(head, depth);
#elif defined(ONLY_ATOMIC)
    acc ^= run_atomic(head, depth);
#else
    acc ^= run_naive(head, depth);
    acc ^= run_atomic(head, depth);
#endif
    sink = acc;
}

int main(int argc, char **argv) {
    int depths[] = {2, 3, 5, 8};
    if (argc > 1) {
        int depth = atoi(argv[1]);
        run_depth(depth);
    } else {
        for (unsigned i = 0; i < sizeof(depths) / sizeof(depths[0]); i++) {
            run_depth(depths[i]);
        }
    }
    if (sink == 42) {
        printf("unreachable\n");
    }
    return 0;
}
