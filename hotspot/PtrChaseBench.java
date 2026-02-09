public class PtrChaseBench {
  static class Node { Node next; int value; }
  static volatile int sink;

  static Node[] buildRing(int n) {
    Node[] pool = new Node[n];
    for (int i = 0; i < n; i++) {
      pool[i] = new Node();
      pool[i].value = i;
    }
    for (int i = 0; i < n; i++) {
      pool[i].next = pool[(i + 1) % n];
    }
    return pool;
  }

  static int chaseContract(Node p, int depth) {
    for (int i = 0; i < depth; i++) {
      p = p.next;            // implicit null check
    }
    return p.value;
  }

  static int chaseGuarded(Node p, int depth) {
    for (int i = 0; i < depth; i++) {
      if (p == null) return -1;  // explicit check
      p = p.next;
    }
    if (p == null) return -1;
    return p.value;
  }

  static int runContract(Node[] pool, int depth, int iters) {
    int acc = 0, idx = 0;
    int stride = 1315423911 % pool.length; if (stride == 0) stride = 1;
    for (int i = 0; i < iters; i++) {
      idx += stride; if (idx >= pool.length) idx -= pool.length;
      acc ^= chaseContract(pool[idx], depth);
    }
    return acc;
  }

  static int runGuarded(Node[] pool, int depth, int iters) {
    int acc = 0, idx = 0;
    int stride = 1315423911 % pool.length; if (stride == 0) stride = 1;
    for (int i = 0; i < iters; i++) {
      idx += stride; if (idx >= pool.length) idx -= pool.length;
      acc ^= chaseGuarded(pool[idx], depth);
    }
    return acc;
  }

  public static void main(String[] args) {
    int depth = Integer.parseInt(args[0]);
    int nodes = Integer.parseInt(args[1]);
    int iters = Integer.parseInt(args[2]);
    Node[] pool = buildRing(nodes);

    for (int i = 0; i < 3; i++) {
      sink ^= runContract(pool, depth, iters / 10);
      sink ^= runGuarded(pool, depth, iters / 10);
    }

    long t0 = System.nanoTime();
    sink ^= runContract(pool, depth, iters);
    long t1 = System.nanoTime();
    System.out.println("contract ms=" + (t1 - t0)/1e6);

    t0 = System.nanoTime();
    sink ^= runGuarded(pool, depth, iters);
    t1 = System.nanoTime();
    System.out.println("guarded  ms=" + (t1 - t0)/1e6);
  }
}
