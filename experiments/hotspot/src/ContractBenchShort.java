public class ContractBenchShort {
  static volatile int sink;

  static short[] buildRing(int nodes) {
    if (nodes > 65535) {
      System.err.println("short index graph supports up to 65535 nodes");
      System.exit(1);
    }
    short[] next = new short[nodes];
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
      next[cur] = (short) nxt;
    }
    return next;
  }

  static int chaseGuarded(short[] next, int idx, int depth) {
    int n = next.length;
    for (int i = 0; i < depth; i++) {
      if (idx < 0 || idx >= n) {
        return -1;
      }
      idx = next[idx] & 0xFFFF;
    }
    if (idx < 0 || idx >= n) {
      return -1;
    }
    return idx;
  }

  static int chaseContract(short[] next, int idx, int depth) {
    for (int i = 0; i < depth; i++) {
      idx = next[idx] & 0xFFFF;
    }
    return idx;
  }

  static int runGuarded(short[] next, int depth, int iters) {
    int acc = 0;
    int idx = 0;
    int stride = 1315423911 % next.length;
    if (stride == 0) {
      stride = 1;
    }
    for (int i = 0; i < iters; i++) {
      idx += stride;
      if (idx >= next.length) {
        idx -= next.length;
      }
      acc ^= chaseGuarded(next, idx, depth);
    }
    return acc;
  }

  static int runContract(short[] next, int depth, int iters) {
    int acc = 0;
    int idx = 0;
    int stride = 1315423911 % next.length;
    if (stride == 0) {
      stride = 1;
    }
    for (int i = 0; i < iters; i++) {
      idx += stride;
      if (idx >= next.length) {
        idx -= next.length;
      }
      acc ^= chaseContract(next, idx, depth);
    }
    return acc;
  }

  static void warmup(short[] next, int depth, int iters) {
    int acc = 0;
    for (int i = 0; i < 3; i++) {
      acc ^= runGuarded(next, depth, iters / 10);
      acc ^= runContract(next, depth, iters / 10);
    }
    sink = acc;
  }

  public static void main(String[] args) {
    if (args.length < 4) {
      System.err.println("usage: ContractBenchShort <mode> <depth> <nodes> <iters>");
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

    short[] next = buildRing(nodes);
    warmup(next, depth, iters);

    int acc = 0;
    if ("guarded".equals(mode)) {
      acc ^= runGuarded(next, depth, iters);
    } else if ("contract".equals(mode)) {
      acc ^= runContract(next, depth, iters);
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
