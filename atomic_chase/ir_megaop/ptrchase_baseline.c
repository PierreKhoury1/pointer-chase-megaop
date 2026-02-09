#include <stdint.h>

typedef struct Node {
    struct Node *next;
    int value;
} Node;

__attribute__((noinline))
Node *chase_normal(Node *p, int depth) {
    for (int i = 0; i < depth; i++) {
        p = p->next;
    }
    return p;
}
