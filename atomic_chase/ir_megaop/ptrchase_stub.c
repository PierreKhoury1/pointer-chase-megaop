#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

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

__attribute__((noinline))
Node *chase_mega_stub(Node *p, int depth) {
    // Stub "mega-op" lowered to the same loop for now.
    for (int i = 0; i < depth; i++) {
        p = p->next;
    }
    return p;
}

static volatile int sink;

static int run(Node *head, int depth, int iters, int use_stub) {
    int acc = 0;
    Node *p = head;
    for (int i = 0; i < iters; i++) {
        Node *q;
#if defined(ONLY_NORMAL)
        (void)use_stub;
        q = chase_normal(p, depth);
#elif defined(ONLY_STUB)
        (void)use_stub;
        q = chase_mega_stub(p, depth);
#else
        q = use_stub ? chase_mega_stub(p, depth) : chase_normal(p, depth);
#endif
        acc ^= q->value;
        p = p->next;
    }
    return acc;
}

__attribute__((noinline))
static Node *build_chain(int depth) {
    if (depth <= 0) {
        return NULL;
    }
    Node *head = NULL;
    Node *cur = NULL;
    for (int i = 0; i <= depth; i++) {
        Node *n = (Node *)malloc(sizeof(Node));
        n->value = rand();
        n->next = NULL;
        if (!head) {
            head = n;
        } else {
            cur->next = n;
        }
        cur = n;
    }
    cur->next = head;
    return head;
}

int main(int argc, char **argv) {
    int depth = 8;
    int iters = 10000000;
    int use_stub = 0;
    if (argc > 1) {
        use_stub = argv[1][0] == 's';
    }
    if (argc > 2) {
        depth = atoi(argv[2]);
    }
    if (argc > 3) {
        iters = atoi(argv[3]);
    }
    srand((unsigned)time(NULL));
    Node *head = build_chain(depth);
    sink = run(head, depth, iters, use_stub);
    if (sink == 42) {
        puts("unreachable");
    }
    return 0;
}
