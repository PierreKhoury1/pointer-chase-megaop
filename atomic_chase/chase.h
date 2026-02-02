#ifndef ATOMIC_CHASE_H
#define ATOMIC_CHASE_H

#ifdef __cplusplus
extern "C" {
#endif

typedef struct Node {
    struct Node *next;
    int value;
} Node;

Node *build_chain(int depth);
int chase_naive(Node *p, int depth);

#if defined(__GNUC__)
#define NOINLINE __attribute__((noinline))
#else
#define NOINLINE
#endif

NOINLINE int chase_atomic(Node *p, int depth);

#ifdef __cplusplus
}
#endif

#endif
