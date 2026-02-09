public class ContractBenchObj {
  static class Node {
    Node next;
    int value;
  }

  static volatile int sink;

  static Node[] buildRing(int nodes) {
    Node[] pool = new Node[nodes];
    for (int i = 0; i < nodes; i++) {
      Node n = new Node();
      n.value = i;
      pool[i] = n;
    }

    int[] perm = new int[nodes];
    for (int i = 0; i < nodes; i++) {
      perm[i] = i;
    }

    long rng = 0x9e3779b97f4a7c15L;
    for (int i = nodes - 1; i > 0; i--) {
      rng ^= (rng >>> 12);
      rng ^= (rng << 25);
      rng ^= (rng >>> 27);
      long r = rng * 2685821657736338717L;
      int j = (int) (Math.floorMod(r, i + 1));
      int tmp = perm[i];
      perm[i] = perm[j];
      perm[j] = tmp;
    }

    for (int i = 0; i < nodes; i++) {
      int cur = perm[i];
      int nxt = perm[(i + 1) % nodes];
      pool[cur].next = pool[nxt];
    }
    return pool;
  }

  static int chaseGuarded(Node p, int depth) {
    for (int i = 0; i < depth; i++) {
      if (p == null) {
        return -1;
      }
      p = p.next;
    }
    if (p == null) {
      return -1;
    }
    return p.value;
  }

  static int chaseContract(Node p, int depth) {
    for (int i = 0; i < depth; i++) {
      p = p.next;
    }
    return p.value;
  }

  static int runGuarded(Node[] pool, int depth, int iters) {
    int acc = 0;
    int idx = 0;
    int stride = 1315423911 % pool.length;
    if (stride == 0) {
      stride = 1;
    }
    for (int i = 0; i < iters; i++) {
      idx += stride;
      if (idx >= pool.length) {
        idx -= pool.length;
      }
      acc ^= chaseGuarded(pool[idx], depth);
    }
    return acc;
  }

  static int runContract(Node[] pool, int depth, int iters) {
    int acc = 0;
    int idx = 0;
    int stride = 1315423911 % pool.length;
    if (stride == 0) {
      stride = 1;
    }
    for (int i = 0; i < iters; i++) {
      idx += stride;
      if (idx >= pool.length) {
        idx -= pool.length;
      }
      acc ^= chaseContract(pool[idx], depth);
    }
    return acc;
  }

  static void warmup(Node[] pool, int depth, int iters) {
    int acc = 0;
    for (int i = 0; i < 3; i++) {
      acc ^= runGuarded(pool, depth, iters / 10);
      acc ^= runContract(pool, depth, iters / 10);
    }
    sink = acc;
  }

  public static void main(String[] args) {
    if (args.length < 4) {
      System.err.println("usage: ContractBenchObj <mode> <depth> <nodes> <iters>");
      System.err.println("  mode: guarded | contract");
      System.exit(1);
    }
    String mode = args[0];
    int depth = Integer.parseInt(args[1]);
    int nodes = Integer.parseInt(args[2]);
    int iters = Integer.parseInt(args[3]);

    if (depth <= 0 || nodes <= 0 || iters <= 0) {
      System.err.println("invalid args");
      System.exit(1);
    }

    Node[] pool = buildRing(nodes);
    warmup(pool, depth, iters);

    int acc = 0;
    if ("guarded".equals(mode)) {
      acc ^= runGuarded(pool, depth, iters);
    } else if ("contract".equals(mode)) {
      acc ^= runContract(pool, depth, iters);
    } else {
      System.err.println("unknown mode: " + mode);
      System.exit(1);
    }
    sink = acc;
    if (sink == 42) {
      System.out.println("unreachable");
    }
  }
}
