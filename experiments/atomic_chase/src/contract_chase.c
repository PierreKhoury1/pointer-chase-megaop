#include "contract_chase.h"

#include <stdlib.h>

static uint64_t xorshift64star(uint64_t *state) {
    uint64_t x = *state;
    x ^= x >> 12;
    x ^= x << 25;
    x ^= x >> 27;
    *state = x;
    return x * 2685821657736338717ULL;
}

Node *build_pool(size_t count, uint64_t seed) {
    if (count == 0) {
        return NULL;
    }

    Node *nodes = (Node *)malloc(count * sizeof(Node));
    if (!nodes) {
        return NULL;
    }

    uint32_t *perm = (uint32_t *)malloc(count * sizeof(uint32_t));
    if (!perm) {
        free(nodes);
        return NULL;
    }

    for (size_t i = 0; i < count; i++) {
        nodes[i].value = (uint32_t)i;
        nodes[i].next = NULL;
        perm[i] = (uint32_t)i;
    }

    uint64_t rng = seed ? seed : 0x9e3779b97f4a7c15ULL;
    for (size_t i = count - 1; i > 0; i--) {
        uint64_t r = xorshift64star(&rng);
        size_t j = (size_t)(r % (i + 1));
        uint32_t tmp = perm[i];
        perm[i] = perm[j];
        perm[j] = tmp;
    }

    for (size_t i = 0; i < count; i++) {
        size_t cur = perm[i];
        size_t next = perm[(i + 1) % count];
        nodes[cur].next = &nodes[next];
    }

    free(perm);
    return nodes;
}

void free_pool(Node *pool) {
    free(pool);
}

int chase_guarded(Node *p, int depth) {
    for (int i = 0; i < depth; i++) {
        if (!p) {
            return -1;
        }
        p = p->next;
    }
    if (!p) {
        return -1;
    }
    return (int)p->value;
}

NOINLINE int chase_contract(Node *p, int depth) {
    for (int i = 0; i < depth; i++) {
        p = p->next;
    }
    return (int)p->value;
}
