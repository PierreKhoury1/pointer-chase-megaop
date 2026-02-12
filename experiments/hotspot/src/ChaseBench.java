public class ChaseBench {
  static final int WIDTH = 32;
  static final int WARMUP_ITERS = 50000;
  static final int[] CONST_OFFSETS = {2, 5, 7, 3, 1, 6, 4, 9};

  static class Node {
    Node next;
    int value;
  }

  static volatile int sink;
  static Node chainHead;
  static Object root_d2;
  static Object root_d3;
  static Object root_d5;
  static Object root_d8;

  static Node buildNodeChain(int depth) {
    Node head = new Node();
    Node cur = head;
    for (int i = 1; i < depth; i++) {
      Node n = new Node();
      n.value = i;
      cur.next = n;
      cur = n;
    }
    return head;
  }

  static Object buildArrayChain(int depth) {
    if (depth <= 1) {
      int[] leaf = new int[WIDTH];
      for (int i = 0; i < leaf.length; i++) {
        leaf[i] = i + 1;
      }
      return leaf;
    }
    Object[] arr = new Object[WIDTH];
    Object child = buildArrayChain(depth - 1);
    for (int i = 0; i < arr.length; i++) {
      arr[i] = child;
    }
    return arr;
  }

  static void init() {
    chainHead = buildNodeChain(8);
    root_d2 = buildArrayChain(2);
    root_d3 = buildArrayChain(3);
    root_d5 = buildArrayChain(5);
    root_d8 = buildArrayChain(8);
  }

  // Plain object field chasing
  static int plain_d2(Node p) { return p.next.value; }
  static int plain_d3(Node p) { return p.next.next.value; }
  static int plain_d5(Node p) { return p.next.next.next.next.value; }
  static int plain_d8(Node p) { return p.next.next.next.next.next.next.next.value; }

  // Constant offsets (array-based)
  static int const_d2(Object root) {
    Object[] a0 = (Object[]) root;
    Object cur = a0[CONST_OFFSETS[0]];
    int[] leaf = (int[]) cur;
    return leaf[CONST_OFFSETS[1]];
  }

  static int const_d3(Object root) {
    Object[] a0 = (Object[]) root;
    Object cur = a0[CONST_OFFSETS[0]];
    Object[] a1 = (Object[]) cur;
    cur = a1[CONST_OFFSETS[1]];
    int[] leaf = (int[]) cur;
    return leaf[CONST_OFFSETS[2]];
  }

  static int const_d5(Object root) {
    Object[] a0 = (Object[]) root;
    Object cur = a0[CONST_OFFSETS[0]];
    Object[] a1 = (Object[]) cur;
    cur = a1[CONST_OFFSETS[1]];
    Object[] a2 = (Object[]) cur;
    cur = a2[CONST_OFFSETS[2]];
    Object[] a3 = (Object[]) cur;
    cur = a3[CONST_OFFSETS[3]];
    int[] leaf = (int[]) cur;
    return leaf[CONST_OFFSETS[4]];
  }

  static int const_d8(Object root) {
    Object[] a0 = (Object[]) root;
    Object cur = a0[CONST_OFFSETS[0]];
    Object[] a1 = (Object[]) cur;
    cur = a1[CONST_OFFSETS[1]];
    Object[] a2 = (Object[]) cur;
    cur = a2[CONST_OFFSETS[2]];
    Object[] a3 = (Object[]) cur;
    cur = a3[CONST_OFFSETS[3]];
    Object[] a4 = (Object[]) cur;
    cur = a4[CONST_OFFSETS[4]];
    Object[] a5 = (Object[]) cur;
    cur = a5[CONST_OFFSETS[5]];
    Object[] a6 = (Object[]) cur;
    cur = a6[CONST_OFFSETS[6]];
    int[] leaf = (int[]) cur;
    return leaf[CONST_OFFSETS[7]];
  }

  // Dynamic offsets (array-based)
  static int dyn_d2(Object root, int o1, int o2) {
    Object[] a0 = (Object[]) root;
    Object cur = a0[o1];
    int[] leaf = (int[]) cur;
    return leaf[o2];
  }

  static int dyn_d3(Object root, int o1, int o2, int o3) {
    Object[] a0 = (Object[]) root;
    Object cur = a0[o1];
    Object[] a1 = (Object[]) cur;
    cur = a1[o2];
    int[] leaf = (int[]) cur;
    return leaf[o3];
  }

  static int dyn_d5(Object root, int o1, int o2, int o3, int o4, int o5) {
    Object[] a0 = (Object[]) root;
    Object cur = a0[o1];
    Object[] a1 = (Object[]) cur;
    cur = a1[o2];
    Object[] a2 = (Object[]) cur;
    cur = a2[o3];
    Object[] a3 = (Object[]) cur;
    cur = a3[o4];
    int[] leaf = (int[]) cur;
    return leaf[o5];
  }

  static int dyn_d8(
      Object root, int o1, int o2, int o3, int o4, int o5, int o6, int o7, int o8) {
    Object[] a0 = (Object[]) root;
    Object cur = a0[o1];
    Object[] a1 = (Object[]) cur;
    cur = a1[o2];
    Object[] a2 = (Object[]) cur;
    cur = a2[o3];
    Object[] a3 = (Object[]) cur;
    cur = a3[o4];
    Object[] a4 = (Object[]) cur;
    cur = a4[o5];
    Object[] a5 = (Object[]) cur;
    cur = a5[o6];
    Object[] a6 = (Object[]) cur;
    cur = a6[o7];
    int[] leaf = (int[]) cur;
    return leaf[o8];
  }

  // Explicit per-level checks
  static int checks_d2(Object root, int o1, int o2) {
    if (root == null) throw new NullPointerException();
    if (!(root instanceof Object[])) throw new ClassCastException();
    Object[] a0 = (Object[]) root;
    if (o1 < 0 || o1 >= a0.length) throw new ArrayIndexOutOfBoundsException();
    Object cur = a0[o1];
    if (cur == null) throw new NullPointerException();
    if (!(cur instanceof int[])) throw new ClassCastException();
    int[] leaf = (int[]) cur;
    if (o2 < 0 || o2 >= leaf.length) throw new ArrayIndexOutOfBoundsException();
    return leaf[o2];
  }

  static int checks_d3(Object root, int o1, int o2, int o3) {
    if (root == null) throw new NullPointerException();
    if (!(root instanceof Object[])) throw new ClassCastException();
    Object[] a0 = (Object[]) root;
    if (o1 < 0 || o1 >= a0.length) throw new ArrayIndexOutOfBoundsException();
    Object cur = a0[o1];
    if (cur == null) throw new NullPointerException();
    if (!(cur instanceof Object[])) throw new ClassCastException();
    Object[] a1 = (Object[]) cur;
    if (o2 < 0 || o2 >= a1.length) throw new ArrayIndexOutOfBoundsException();
    cur = a1[o2];
    if (cur == null) throw new NullPointerException();
    if (!(cur instanceof int[])) throw new ClassCastException();
    int[] leaf = (int[]) cur;
    if (o3 < 0 || o3 >= leaf.length) throw new ArrayIndexOutOfBoundsException();
    return leaf[o3];
  }

  static int checks_d5(Object root, int o1, int o2, int o3, int o4, int o5) {
    if (root == null) throw new NullPointerException();
    if (!(root instanceof Object[])) throw new ClassCastException();
    Object[] a0 = (Object[]) root;
    if (o1 < 0 || o1 >= a0.length) throw new ArrayIndexOutOfBoundsException();
    Object cur = a0[o1];
    if (cur == null) throw new NullPointerException();
    if (!(cur instanceof Object[])) throw new ClassCastException();
    Object[] a1 = (Object[]) cur;
    if (o2 < 0 || o2 >= a1.length) throw new ArrayIndexOutOfBoundsException();
    cur = a1[o2];
    if (cur == null) throw new NullPointerException();
    if (!(cur instanceof Object[])) throw new ClassCastException();
    Object[] a2 = (Object[]) cur;
    if (o3 < 0 || o3 >= a2.length) throw new ArrayIndexOutOfBoundsException();
    cur = a2[o3];
    if (cur == null) throw new NullPointerException();
    if (!(cur instanceof Object[])) throw new ClassCastException();
    Object[] a3 = (Object[]) cur;
    if (o4 < 0 || o4 >= a3.length) throw new ArrayIndexOutOfBoundsException();
    cur = a3[o4];
    if (cur == null) throw new NullPointerException();
    if (!(cur instanceof int[])) throw new ClassCastException();
    int[] leaf = (int[]) cur;
    if (o5 < 0 || o5 >= leaf.length) throw new ArrayIndexOutOfBoundsException();
    return leaf[o5];
  }

  static int checks_d8(
      Object root, int o1, int o2, int o3, int o4, int o5, int o6, int o7, int o8) {
    if (root == null) throw new NullPointerException();
    if (!(root instanceof Object[])) throw new ClassCastException();
    Object[] a0 = (Object[]) root;
    if (o1 < 0 || o1 >= a0.length) throw new ArrayIndexOutOfBoundsException();
    Object cur = a0[o1];
    if (cur == null) throw new NullPointerException();
    if (!(cur instanceof Object[])) throw new ClassCastException();
    Object[] a1 = (Object[]) cur;
    if (o2 < 0 || o2 >= a1.length) throw new ArrayIndexOutOfBoundsException();
    cur = a1[o2];
    if (cur == null) throw new NullPointerException();
    if (!(cur instanceof Object[])) throw new ClassCastException();
    Object[] a2 = (Object[]) cur;
    if (o3 < 0 || o3 >= a2.length) throw new ArrayIndexOutOfBoundsException();
    cur = a2[o3];
    if (cur == null) throw new NullPointerException();
    if (!(cur instanceof Object[])) throw new ClassCastException();
    Object[] a3 = (Object[]) cur;
    if (o4 < 0 || o4 >= a3.length) throw new ArrayIndexOutOfBoundsException();
    cur = a3[o4];
    if (cur == null) throw new NullPointerException();
    if (!(cur instanceof Object[])) throw new ClassCastException();
    Object[] a4 = (Object[]) cur;
    if (o5 < 0 || o5 >= a4.length) throw new ArrayIndexOutOfBoundsException();
    cur = a4[o5];
    if (cur == null) throw new NullPointerException();
    if (!(cur instanceof Object[])) throw new ClassCastException();
    Object[] a5 = (Object[]) cur;
    if (o6 < 0 || o6 >= a5.length) throw new ArrayIndexOutOfBoundsException();
    cur = a5[o6];
    if (cur == null) throw new NullPointerException();
    if (!(cur instanceof Object[])) throw new ClassCastException();
    Object[] a6 = (Object[]) cur;
    if (o7 < 0 || o7 >= a6.length) throw new ArrayIndexOutOfBoundsException();
    cur = a6[o7];
    if (cur == null) throw new NullPointerException();
    if (!(cur instanceof int[])) throw new ClassCastException();
    int[] leaf = (int[]) cur;
    if (o8 < 0 || o8 >= leaf.length) throw new ArrayIndexOutOfBoundsException();
    return leaf[o8];
  }

  static int runPlain() {
    int acc = 0;
    for (int i = 0; i < WARMUP_ITERS; i++) {
      acc ^= plain_d2(chainHead);
      acc ^= plain_d3(chainHead);
      acc ^= plain_d5(chainHead);
      acc ^= plain_d8(chainHead);
    }
    return acc;
  }

  static int runConst() {
    int acc = 0;
    for (int i = 0; i < WARMUP_ITERS; i++) {
      acc ^= const_d2(root_d2);
      acc ^= const_d3(root_d3);
      acc ^= const_d5(root_d5);
      acc ^= const_d8(root_d8);
    }
    return acc;
  }

  static int runDyn() {
    int acc = 0;
    for (int i = 0; i < WARMUP_ITERS; i++) {
      int o1 = i & (WIDTH - 1);
      int o2 = (i + 3) & (WIDTH - 1);
      int o3 = (i + 7) & (WIDTH - 1);
      int o4 = (i + 11) & (WIDTH - 1);
      int o5 = (i + 13) & (WIDTH - 1);
      int o6 = (i + 17) & (WIDTH - 1);
      int o7 = (i + 19) & (WIDTH - 1);
      int o8 = (i + 23) & (WIDTH - 1);
      acc ^= dyn_d2(root_d2, o1, o2);
      acc ^= dyn_d3(root_d3, o1, o2, o3);
      acc ^= dyn_d5(root_d5, o1, o2, o3, o4, o5);
      acc ^= dyn_d8(root_d8, o1, o2, o3, o4, o5, o6, o7, o8);
    }
    return acc;
  }

  static int runChecks() {
    int acc = 0;
    for (int i = 0; i < WARMUP_ITERS; i++) {
      int o1 = i & (WIDTH - 1);
      int o2 = (i + 3) & (WIDTH - 1);
      int o3 = (i + 7) & (WIDTH - 1);
      int o4 = (i + 11) & (WIDTH - 1);
      int o5 = (i + 13) & (WIDTH - 1);
      int o6 = (i + 17) & (WIDTH - 1);
      int o7 = (i + 19) & (WIDTH - 1);
      int o8 = (i + 23) & (WIDTH - 1);
      acc ^= checks_d2(root_d2, o1, o2);
      acc ^= checks_d3(root_d3, o1, o2, o3);
      acc ^= checks_d5(root_d5, o1, o2, o3, o4, o5);
      acc ^= checks_d8(root_d8, o1, o2, o3, o4, o5, o6, o7, o8);
    }
    return acc;
  }

  public static void main(String[] args) {
    init();
    int acc = 0;
    acc ^= runPlain();
    acc ^= runConst();
    acc ^= runDyn();
    acc ^= runChecks();
    sink = acc;
    if (sink == 42) {
      System.out.println("unreachable");
    }
  }
}
