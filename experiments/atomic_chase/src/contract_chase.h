#ifndef CONTRACT_CHASE_H
#define CONTRACT_CHASE_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct Node {
    struct Node *next;
    uint32_t value;
} Node;

Node *build_pool(size_t count, uint64_t seed);
void free_pool(Node *pool);

int chase_guarded(Node *p, int depth);

#if defined(__GNUC__)
#define NOINLINE __attribute__((noinline))
#else
#define NOINLINE
#endif

NOINLINE int chase_contract(Node *p, int depth);

#ifdef __cplusplus
}
#endif

#endif
