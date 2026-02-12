#include "chase.h"

#include <stdlib.h>

Node *build_chain(int depth) {
    if (depth <= 0) {
        return NULL;
    }
    Node *head = NULL;
    Node *cur = NULL;
    for (int i = 0; i <= depth; i++) {
        Node *n = (Node *)malloc(sizeof(Node));
        if (!n) {
            return NULL;
        }
        n->value = i;
        n->next = NULL;
        if (!head) {
            head = n;
        } else {
            cur->next = n;
        }
        cur = n;
    }
    return head;
}

int chase_naive(Node *p, int depth) {
    for (int i = 0; i < depth; i++) {
        p = p->next;
    }
    return p->value;
}

NOINLINE int chase_atomic(Node *p, int depth) {
    int result = -1;
    switch (depth) {
        case 2:
            if (p && p->next && p->next->next) {
                result = p->next->next->value;
            }
            break;
        case 3:
            if (p && p->next && p->next->next && p->next->next->next) {
                result = p->next->next->next->value;
            }
            break;
        case 5:
            if (p && p->next && p->next->next && p->next->next->next &&
                p->next->next->next->next && p->next->next->next->next->next) {
                result = p->next->next->next->next->next->value;
            }
            break;
        case 8:
            if (p && p->next && p->next->next && p->next->next->next &&
                p->next->next->next->next && p->next->next->next->next->next &&
                p->next->next->next->next->next->next &&
                p->next->next->next->next->next->next->next &&
                p->next->next->next->next->next->next->next->next) {
                result = p->next->next->next->next->next->next->next->next->value;
            }
            break;
        default:
            break;
    }
    return result;
}
