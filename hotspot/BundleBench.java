import java.lang.reflect.Field;
import jdk.internal.misc.PtrChase;
import jdk.internal.misc.Unsafe;

public class BundleBench {
  static class Node {
    Node next;
    int value;
  }

  static volatile int sink;
  static final Unsafe U;
  static final long NEXT_OFF;
  static final long VALUE_OFF;

  static {
    try {
      Field f = Unsafe.class.getDeclaredField("theUnsafe");
      f.setAccessible(true);
      U = (Unsafe) f.get(null);
      Field nextField = Node.class.getDeclaredField("next");
      Field valueField = Node.class.getDeclaredField("value");
      NEXT_OFF = U.objectFieldOffset(nextField);
      VALUE_OFF = U.objectFieldOffset(valueField);
    } catch (Exception e) {
      throw new RuntimeException(e);
    }
  }

  static int chaseContract(Node p, int depth) {
    for (int i = 0; i < depth; i++) {
      p = p.next;
    }
    return p.value;
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

  static native int chase8(Node p);
  static native void initIDs(Class<?> nodeClass);

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

  static int runBundle(Node[] pool, int iters) {
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
      acc ^= chase8(pool[idx]);
    }
    return acc;
  }

  static int runIntrinsic(Node[] pool, int iters) {
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
      acc ^= PtrChase.chase8(pool[idx], NEXT_OFF, VALUE_OFF);
    }
    return acc;
  }

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

  static void warmup(Node[] pool, int depth, int iters, boolean includeBundle, boolean includeIntrinsic) {
    int acc = 0;
    for (int i = 0; i < 3; i++) {
      acc ^= runGuarded(pool, depth, iters / 10);
      acc ^= runContract(pool, depth, iters / 10);
      if (includeBundle) {
        acc ^= runBundle(pool, iters / 10);
      }
      if (includeIntrinsic) {
        acc ^= runIntrinsic(pool, iters / 10);
      }
    }
    sink = acc;
  }

  public static void main(String[] args) {
    if (args.length < 4) {
      System.err.println("usage: BundleBench <mode> <depth> <nodes> <iters>");
      System.err.println("  mode: guarded | contract | bundle | intrinsic");
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

    boolean includeBundle = false;
    boolean includeIntrinsic = false;
    if ("bundle".equals(mode)) {
      String lib = System.getProperty("ptrchase.lib");
      if (lib != null && !lib.isEmpty()) {
        System.load(lib);
      } else {
        System.loadLibrary("ptrchase");
      }
      initIDs(Node.class);
      includeBundle = true;
    }

    if ("intrinsic".equals(mode)) {
      includeIntrinsic = true;
    }

    warmup(pool, depth, iters, includeBundle, includeIntrinsic);

    int acc = 0;
    long t0 = System.nanoTime();
    if ("guarded".equals(mode)) {
      acc ^= runGuarded(pool, depth, iters);
    } else if ("contract".equals(mode)) {
      acc ^= runContract(pool, depth, iters);
    } else if ("bundle".equals(mode)) {
      if (depth != 8) {
        System.err.println("bundle mode only supports depth=8");
        System.exit(2);
      }
      acc ^= runBundle(pool, iters);
    } else if ("intrinsic".equals(mode)) {
      if (depth != 8) {
        System.err.println("intrinsic mode only supports depth=8");
        System.exit(2);
      }
      acc ^= runIntrinsic(pool, iters);
    } else {
      System.err.println("unknown mode: " + mode);
      System.exit(1);
    }
    long t1 = System.nanoTime();

    sink = acc;
    if (sink == 42) {
      System.out.println("unreachable");
    }
    double ms = (t1 - t0) / 1e6;
    System.out.printf("mode=%s depth=%d nodes=%d iters=%d time_ms=%.3f\n", mode, depth, nodes, iters, ms);
  }
}
