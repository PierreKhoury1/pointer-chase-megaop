#include <stdint.h>
#include <stddef.h>

#if defined(__GNUC__)
#define NOINLINE __attribute__((noinline))
#define USED __attribute__((used))
#else
#define NOINLINE
#define USED
#endif

#define GUARD(ptr) do { if (!(ptr)) __builtin_trap(); } while (0)

NOINLINE USED int plain_d2(int ** p) {
  return *(*(p));
}

NOINLINE USED int const_d2(int ** p) {
  return *(*(p + 2) + 5);
}

NOINLINE USED int dyn_d2(int ** p, int o1, int o2) {
  return *(*(p + o1) + o2);
}

NOINLINE USED int checks_d2(int ** p, int o1, int o2) {
  GUARD(p);
  int *p1 = *(p + o1);
  GUARD(p1);
  return *(p1 + o2);
}

NOINLINE USED int plain_d3(int *** p) {
  return *(*(*(p)));
}

NOINLINE USED int const_d3(int *** p) {
  return *(*(*(p + 2) + 5) + 17);
}

NOINLINE USED int dyn_d3(int *** p, int o1, int o2, int o3) {
  return *(*(*(p + o1) + o2) + o3);
}

NOINLINE USED int checks_d3(int *** p, int o1, int o2, int o3) {
  GUARD(p);
  int **p1 = *(p + o1);
  GUARD(p1);
  int *p2 = *(p1 + o2);
  GUARD(p2);
  return *(p2 + o3);
}

NOINLINE USED int plain_d5(int ***** p) {
  return *(*(*(*(*(p)))));
}

NOINLINE USED int const_d5(int ***** p) {
  return *(*(*(*(*(p + 2) + 5) + 17) + 3) + 7);
}

NOINLINE USED int dyn_d5(int ***** p, int o1, int o2, int o3, int o4, int o5) {
  return *(*(*(*(*(p + o1) + o2) + o3) + o4) + o5);
}

NOINLINE USED int checks_d5(int ***** p, int o1, int o2, int o3, int o4, int o5) {
  GUARD(p);
  int ****p1 = *(p + o1);
  GUARD(p1);
  int ***p2 = *(p1 + o2);
  GUARD(p2);
  int **p3 = *(p2 + o3);
  GUARD(p3);
  int *p4 = *(p3 + o4);
  GUARD(p4);
  return *(p4 + o5);
}

NOINLINE USED int plain_d8(int ******** p) {
  return *(*(*(*(*(*(*(*(p))))))));
}

NOINLINE USED int const_d8(int ******** p) {
  return *(*(*(*(*(*(*(*(p + 2) + 5) + 17) + 3) + 7) + 11) + 13) + 19);
}

NOINLINE USED int dyn_d8(int ******** p, int o1, int o2, int o3, int o4, int o5, int o6, int o7, int o8) {
  return *(*(*(*(*(*(*(*(p + o1) + o2) + o3) + o4) + o5) + o6) + o7) + o8);
}

NOINLINE USED int checks_d8(int ******** p, int o1, int o2, int o3, int o4, int o5, int o6, int o7, int o8) {
  GUARD(p);
  int *******p1 = *(p + o1);
  GUARD(p1);
  int ******p2 = *(p1 + o2);
  GUARD(p2);
  int *****p3 = *(p2 + o3);
  GUARD(p3);
  int ****p4 = *(p3 + o4);
  GUARD(p4);
  int ***p5 = *(p4 + o5);
  GUARD(p5);
  int **p6 = *(p5 + o6);
  GUARD(p6);
  int *p7 = *(p6 + o7);
  GUARD(p7);
  return *(p7 + o8);
}
