import jdk.internal.misc.PtrChase;
import java.util.SplittableRandom;

public class PtrChaseIntrinsicBench {
  static volatile PtrChase.Node sink;
  static volatile Object sinkObj;
  static volatile int sinkInt;

  static void blackhole(Object o) {
    sinkObj = o;
  }

  static int predicate_from_data(PtrChase.Node p) {
    // Use identity hash to introduce data-dependent branch noise.
    int h = System.identityHashCode(p);
    sinkInt = h;
    return h & 1;
  }

  static PtrChase.Node[] buildPermutation(int n, long seed) {
    PtrChase.Node[] nodes = new PtrChase.Node[n];
    for (int i = 0; i < n; i++) {
      nodes[i] = new PtrChase.Node();
    }

    int[] idx = new int[n];
    for (int i = 0; i < n; i++) idx[i] = i;

    SplittableRandom rnd = new SplittableRandom(seed);
    for (int i = n - 1; i > 0; i--) {
      int j = rnd.nextInt(i + 1);
      int tmp = idx[i];
      idx[i] = idx[j];
      idx[j] = tmp;
    }

    for (int i = 0; i < n; i++) {
      nodes[idx[i]].next = nodes[idx[(i + 1) % n]];
    }
    return nodes;
  }

  // Explicit null checks at each hop.
  static PtrChase.Node chase8_guarded(PtrChase.Node p) {
    if (p == null) return null;
    p = p.next; if (p == null) return null;
    p = p.next; if (p == null) return null;
    p = p.next; if (p == null) return null;
    p = p.next; if (p == null) return null;
    p = p.next; if (p == null) return null;
    p = p.next; if (p == null) return null;
    p = p.next; if (p == null) return null;
    p = p.next;
    return p;
  }

  // Unrolled, no explicit checks; sticky-null via NPE catch.
  static PtrChase.Node chase8_contract(PtrChase.Node p) {
    try {
      p = p.next;
      p = p.next;
      p = p.next;
      p = p.next;
      p = p.next;
      p = p.next;
      p = p.next;
      p = p.next;
      return p;
    } catch (NullPointerException e) {
      return null;
    }
  }

  // Guarded variant with explicit check + side-effect before deref (predictable branch).
  static PtrChase.Node chase8_guarded_g1(PtrChase.Node p) {
    if (p == null) return null;
    blackhole(p);
    p = p.next; if (p == null) return null;
    blackhole(p);
    p = p.next; if (p == null) return null;
    blackhole(p);
    p = p.next; if (p == null) return null;
    blackhole(p);
    p = p.next; if (p == null) return null;
    blackhole(p);
    p = p.next; if (p == null) return null;
    blackhole(p);
    p = p.next; if (p == null) return null;
    blackhole(p);
    p = p.next; if (p == null) return null;
    blackhole(p);
    p = p.next;
    return p;
  }

  // Guarded variant with data-dependent branch to force unpredictability,
  // but without changing sticky-null semantics.
  static PtrChase.Node chase8_guarded_g2(PtrChase.Node p) {
    if (p == null) return null;
    if ((predicate_from_data(p) & 1) == 0) { sinkInt = sinkInt + 1; } else { sinkInt = sinkInt - 1; }
    p = p.next; if (p == null) return null;
    if ((predicate_from_data(p) & 1) == 0) { sinkInt = sinkInt + 1; } else { sinkInt = sinkInt - 1; }
    p = p.next; if (p == null) return null;
    if ((predicate_from_data(p) & 1) == 0) { sinkInt = sinkInt + 1; } else { sinkInt = sinkInt - 1; }
    p = p.next; if (p == null) return null;
    if ((predicate_from_data(p) & 1) == 0) { sinkInt = sinkInt + 1; } else { sinkInt = sinkInt - 1; }
    p = p.next; if (p == null) return null;
    if ((predicate_from_data(p) & 1) == 0) { sinkInt = sinkInt + 1; } else { sinkInt = sinkInt - 1; }
    p = p.next; if (p == null) return null;
    if ((predicate_from_data(p) & 1) == 0) { sinkInt = sinkInt + 1; } else { sinkInt = sinkInt - 1; }
    p = p.next; if (p == null) return null;
    if ((predicate_from_data(p) & 1) == 0) { sinkInt = sinkInt + 1; } else { sinkInt = sinkInt - 1; }
    p = p.next; if (p == null) return null;
    if ((predicate_from_data(p) & 1) == 0) { sinkInt = sinkInt + 1; } else { sinkInt = sinkInt - 1; }
    p = p.next;
    return p;
  }

  static PtrChase.Node runIntrinsic(PtrChase.Node p, int iters) {
    PtrChase.Node x = p;
    for (int i = 0; i < iters; i++) {
      x = PtrChase.chase8(x);
    }
    return x;
  }

  static PtrChase.Node runGuarded(PtrChase.Node p, int iters) {
    PtrChase.Node x = p;
    for (int i = 0; i < iters; i++) {
      x = chase8_guarded(x);
    }
    return x;
  }

  static PtrChase.Node runContract(PtrChase.Node p, int iters) {
    PtrChase.Node x = p;
    for (int i = 0; i < iters; i++) {
      x = chase8_contract(x);
    }
    return x;
  }

  static PtrChase.Node runGuardedG1(PtrChase.Node p, int iters) {
    PtrChase.Node x = p;
    for (int i = 0; i < iters; i++) {
      x = chase8_guarded_g1(x);
    }
    return x;
  }

  static PtrChase.Node runGuardedG2(PtrChase.Node p, int iters) {
    PtrChase.Node x = p;
    for (int i = 0; i < iters; i++) {
      x = chase8_guarded_g2(x);
    }
    return x;
  }

  // Bench entrypoints for assembly printing.
  static PtrChase.Node benchIntrinsic(PtrChase.Node p, int iters) {
    return runIntrinsic(p, iters);
  }

  static PtrChase.Node benchGuarded(PtrChase.Node p, int iters) {
    return runGuarded(p, iters);
  }

  static PtrChase.Node benchContract(PtrChase.Node p, int iters) {
    return runContract(p, iters);
  }

  static PtrChase.Node benchGuardedG1(PtrChase.Node p, int iters) {
    return runGuardedG1(p, iters);
  }

  static PtrChase.Node benchGuardedG2(PtrChase.Node p, int iters) {
    return runGuardedG2(p, iters);
  }

  public static void main(String[] args) {
    int nodes = args.length > 0 ? Integer.parseInt(args[0]) : 1_000_000;
    int iters = args.length > 1 ? Integer.parseInt(args[1]) : 50_000_000;
    long seed = args.length > 2 ? Long.parseLong(args[2]) : 12345L;
    String mode = args.length > 3 ? args[3] : "all";

    PtrChase.Node[] pool = buildPermutation(nodes, seed);
    PtrChase.Node start = pool[0];

    if ("all".equals(mode)) {
      // Warmup
      for (int i = 0; i < 3; i++) {
        sink = runIntrinsic(start, iters / 10);
        sink = runGuarded(start, iters / 10);
        sink = runContract(start, iters / 10);
        sink = runGuardedG1(start, iters / 10);
        sink = runGuardedG2(start, iters / 10);
      }

      long t0 = System.nanoTime();
      sink = runIntrinsic(start, iters);
      long t1 = System.nanoTime();
      System.out.println("intrinsic ms=" + (t1 - t0) / 1e6);

      t0 = System.nanoTime();
      sink = runGuarded(start, iters);
      t1 = System.nanoTime();
      System.out.println("guarded   ms=" + (t1 - t0) / 1e6);

      t0 = System.nanoTime();
      sink = runContract(start, iters);
      t1 = System.nanoTime();
      System.out.println("contract  ms=" + (t1 - t0) / 1e6);

      t0 = System.nanoTime();
      sink = runGuardedG1(start, iters);
      t1 = System.nanoTime();
      System.out.println("guarded_g1 ms=" + (t1 - t0) / 1e6);

      t0 = System.nanoTime();
      sink = runGuardedG2(start, iters);
      t1 = System.nanoTime();
      System.out.println("guarded_g2 ms=" + (t1 - t0) / 1e6);
      return;
    }

    // Single-mode run for perf sweeps
    for (int i = 0; i < 3; i++) {
      switch (mode) {
        case "intrinsic" -> sink = runIntrinsic(start, iters / 10);
        case "guarded" -> sink = runGuarded(start, iters / 10);
        case "contract" -> sink = runContract(start, iters / 10);
        case "guarded_g1" -> sink = runGuardedG1(start, iters / 10);
        case "guarded_g2" -> sink = runGuardedG2(start, iters / 10);
        default -> {
          System.err.println("Unknown mode: " + mode + " (use intrinsic|guarded|contract|guarded_g1|guarded_g2|all)");
          System.exit(2);
        }
      }
    }

    long t0 = System.nanoTime();
    switch (mode) {
      case "intrinsic" -> sink = runIntrinsic(start, iters);
      case "guarded" -> sink = runGuarded(start, iters);
      case "contract" -> sink = runContract(start, iters);
      case "guarded_g1" -> sink = runGuardedG1(start, iters);
      case "guarded_g2" -> sink = runGuardedG2(start, iters);
      default -> throw new IllegalStateException("unreachable");
    }
    long t1 = System.nanoTime();
    System.out.println(mode + " ms=" + (t1 - t0) / 1e6);
  }
}
