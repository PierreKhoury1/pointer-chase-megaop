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

NOINLINE USED int plain_d1(int * p) {
  return *(p);
}

NOINLINE USED int const_d1(int * p) {
  return *(p + 2);
}

NOINLINE USED int dyn_d1(int * p, int o1) {
  return *(p + o1);
}

NOINLINE USED int checks_d1(int * p, int o1) {
  GUARD(p);
  return *(p + o1);
}

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

NOINLINE USED int plain_d4(int **** p) {
  return *(*(*(*(p))));
}

NOINLINE USED int const_d4(int **** p) {
  return *(*(*(*(p + 2) + 5) + 17) + 3);
}

NOINLINE USED int dyn_d4(int **** p, int o1, int o2, int o3, int o4) {
  return *(*(*(*(p + o1) + o2) + o3) + o4);
}

NOINLINE USED int checks_d4(int **** p, int o1, int o2, int o3, int o4) {
  GUARD(p);
  int ***p1 = *(p + o1);
  GUARD(p1);
  int **p2 = *(p1 + o2);
  GUARD(p2);
  int *p3 = *(p2 + o3);
  GUARD(p3);
  return *(p3 + o4);
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

NOINLINE USED int plain_d6(int ****** p) {
  return *(*(*(*(*(*(p))))));
}

NOINLINE USED int const_d6(int ****** p) {
  return *(*(*(*(*(*(p + 2) + 5) + 17) + 3) + 7) + 11);
}

NOINLINE USED int dyn_d6(int ****** p, int o1, int o2, int o3, int o4, int o5, int o6) {
  return *(*(*(*(*(*(p + o1) + o2) + o3) + o4) + o5) + o6);
}

NOINLINE USED int checks_d6(int ****** p, int o1, int o2, int o3, int o4, int o5, int o6) {
  GUARD(p);
  int *****p1 = *(p + o1);
  GUARD(p1);
  int ****p2 = *(p1 + o2);
  GUARD(p2);
  int ***p3 = *(p2 + o3);
  GUARD(p3);
  int **p4 = *(p3 + o4);
  GUARD(p4);
  int *p5 = *(p4 + o5);
  GUARD(p5);
  return *(p5 + o6);
}

NOINLINE USED int plain_d7(int ******* p) {
  return *(*(*(*(*(*(*(p)))))));
}

NOINLINE USED int const_d7(int ******* p) {
  return *(*(*(*(*(*(*(p + 2) + 5) + 17) + 3) + 7) + 11) + 13);
}

NOINLINE USED int dyn_d7(int ******* p, int o1, int o2, int o3, int o4, int o5, int o6, int o7) {
  return *(*(*(*(*(*(*(p + o1) + o2) + o3) + o4) + o5) + o6) + o7);
}

NOINLINE USED int checks_d7(int ******* p, int o1, int o2, int o3, int o4, int o5, int o6, int o7) {
  GUARD(p);
  int ******p1 = *(p + o1);
  GUARD(p1);
  int *****p2 = *(p1 + o2);
  GUARD(p2);
  int ****p3 = *(p2 + o3);
  GUARD(p3);
  int ***p4 = *(p3 + o4);
  GUARD(p4);
  int **p5 = *(p4 + o5);
  GUARD(p5);
  int *p6 = *(p5 + o6);
  GUARD(p6);
  return *(p6 + o7);
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

NOINLINE USED int plain_d9(int ********* p) {
  return *(*(*(*(*(*(*(*(*(p)))))))));
}

NOINLINE USED int const_d9(int ********* p) {
  return *(*(*(*(*(*(*(*(*(p + 2) + 5) + 17) + 3) + 7) + 11) + 13) + 19) + 2);
}

NOINLINE USED int dyn_d9(int ********* p, int o1, int o2, int o3, int o4, int o5, int o6, int o7, int o8, int o9) {
  return *(*(*(*(*(*(*(*(*(p + o1) + o2) + o3) + o4) + o5) + o6) + o7) + o8) + o9);
}

NOINLINE USED int checks_d9(int ********* p, int o1, int o2, int o3, int o4, int o5, int o6, int o7, int o8, int o9) {
  GUARD(p);
  int ********p1 = *(p + o1);
  GUARD(p1);
  int *******p2 = *(p1 + o2);
  GUARD(p2);
  int ******p3 = *(p2 + o3);
  GUARD(p3);
  int *****p4 = *(p3 + o4);
  GUARD(p4);
  int ****p5 = *(p4 + o5);
  GUARD(p5);
  int ***p6 = *(p5 + o6);
  GUARD(p6);
  int **p7 = *(p6 + o7);
  GUARD(p7);
  int *p8 = *(p7 + o8);
  GUARD(p8);
  return *(p8 + o9);
}

NOINLINE USED int plain_d10(int ********** p) {
  return *(*(*(*(*(*(*(*(*(*(p))))))))));
}

NOINLINE USED int const_d10(int ********** p) {
  return *(*(*(*(*(*(*(*(*(*(p + 2) + 5) + 17) + 3) + 7) + 11) + 13) + 19) + 2) + 5);
}

NOINLINE USED int dyn_d10(int ********** p, int o1, int o2, int o3, int o4, int o5, int o6, int o7, int o8, int o9, int o10) {
  return *(*(*(*(*(*(*(*(*(*(p + o1) + o2) + o3) + o4) + o5) + o6) + o7) + o8) + o9) + o10);
}

NOINLINE USED int checks_d10(int ********** p, int o1, int o2, int o3, int o4, int o5, int o6, int o7, int o8, int o9, int o10) {
  GUARD(p);
  int *********p1 = *(p + o1);
  GUARD(p1);
  int ********p2 = *(p1 + o2);
  GUARD(p2);
  int *******p3 = *(p2 + o3);
  GUARD(p3);
  int ******p4 = *(p3 + o4);
  GUARD(p4);
  int *****p5 = *(p4 + o5);
  GUARD(p5);
  int ****p6 = *(p5 + o6);
  GUARD(p6);
  int ***p7 = *(p6 + o7);
  GUARD(p7);
  int **p8 = *(p7 + o8);
  GUARD(p8);
  int *p9 = *(p8 + o9);
  GUARD(p9);
  return *(p9 + o10);
}

NOINLINE USED int plain_d11(int *********** p) {
  return *(*(*(*(*(*(*(*(*(*(*(p)))))))))));
}

NOINLINE USED int const_d11(int *********** p) {
  return *(*(*(*(*(*(*(*(*(*(*(p + 2) + 5) + 17) + 3) + 7) + 11) + 13) + 19) + 2) + 5) + 17);
}

NOINLINE USED int dyn_d11(int *********** p, int o1, int o2, int o3, int o4, int o5, int o6, int o7, int o8, int o9, int o10, int o11) {
  return *(*(*(*(*(*(*(*(*(*(*(p + o1) + o2) + o3) + o4) + o5) + o6) + o7) + o8) + o9) + o10) + o11);
}

NOINLINE USED int checks_d11(int *********** p, int o1, int o2, int o3, int o4, int o5, int o6, int o7, int o8, int o9, int o10, int o11) {
  GUARD(p);
  int **********p1 = *(p + o1);
  GUARD(p1);
  int *********p2 = *(p1 + o2);
  GUARD(p2);
  int ********p3 = *(p2 + o3);
  GUARD(p3);
  int *******p4 = *(p3 + o4);
  GUARD(p4);
  int ******p5 = *(p4 + o5);
  GUARD(p5);
  int *****p6 = *(p5 + o6);
  GUARD(p6);
  int ****p7 = *(p6 + o7);
  GUARD(p7);
  int ***p8 = *(p7 + o8);
  GUARD(p8);
  int **p9 = *(p8 + o9);
  GUARD(p9);
  int *p10 = *(p9 + o10);
  GUARD(p10);
  return *(p10 + o11);
}

NOINLINE USED int plain_d12(int ************ p) {
  return *(*(*(*(*(*(*(*(*(*(*(*(p))))))))))));
}

NOINLINE USED int const_d12(int ************ p) {
  return *(*(*(*(*(*(*(*(*(*(*(*(p + 2) + 5) + 17) + 3) + 7) + 11) + 13) + 19) + 2) + 5) + 17) + 3);
}

NOINLINE USED int dyn_d12(int ************ p, int o1, int o2, int o3, int o4, int o5, int o6, int o7, int o8, int o9, int o10, int o11, int o12) {
  return *(*(*(*(*(*(*(*(*(*(*(*(p + o1) + o2) + o3) + o4) + o5) + o6) + o7) + o8) + o9) + o10) + o11) + o12);
}

NOINLINE USED int checks_d12(int ************ p, int o1, int o2, int o3, int o4, int o5, int o6, int o7, int o8, int o9, int o10, int o11, int o12) {
  GUARD(p);
  int ***********p1 = *(p + o1);
  GUARD(p1);
  int **********p2 = *(p1 + o2);
  GUARD(p2);
  int *********p3 = *(p2 + o3);
  GUARD(p3);
  int ********p4 = *(p3 + o4);
  GUARD(p4);
  int *******p5 = *(p4 + o5);
  GUARD(p5);
  int ******p6 = *(p5 + o6);
  GUARD(p6);
  int *****p7 = *(p6 + o7);
  GUARD(p7);
  int ****p8 = *(p7 + o8);
  GUARD(p8);
  int ***p9 = *(p8 + o9);
  GUARD(p9);
  int **p10 = *(p9 + o10);
  GUARD(p10);
  int *p11 = *(p10 + o11);
  GUARD(p11);
  return *(p11 + o12);
}

NOINLINE USED int plain_d13(int ************* p) {
  return *(*(*(*(*(*(*(*(*(*(*(*(*(p)))))))))))));
}

NOINLINE USED int const_d13(int ************* p) {
  return *(*(*(*(*(*(*(*(*(*(*(*(*(p + 2) + 5) + 17) + 3) + 7) + 11) + 13) + 19) + 2) + 5) + 17) + 3) + 7);
}

NOINLINE USED int dyn_d13(int ************* p, int o1, int o2, int o3, int o4, int o5, int o6, int o7, int o8, int o9, int o10, int o11, int o12, int o13) {
  return *(*(*(*(*(*(*(*(*(*(*(*(*(p + o1) + o2) + o3) + o4) + o5) + o6) + o7) + o8) + o9) + o10) + o11) + o12) + o13);
}

NOINLINE USED int checks_d13(int ************* p, int o1, int o2, int o3, int o4, int o5, int o6, int o7, int o8, int o9, int o10, int o11, int o12, int o13) {
  GUARD(p);
  int ************p1 = *(p + o1);
  GUARD(p1);
  int ***********p2 = *(p1 + o2);
  GUARD(p2);
  int **********p3 = *(p2 + o3);
  GUARD(p3);
  int *********p4 = *(p3 + o4);
  GUARD(p4);
  int ********p5 = *(p4 + o5);
  GUARD(p5);
  int *******p6 = *(p5 + o6);
  GUARD(p6);
  int ******p7 = *(p6 + o7);
  GUARD(p7);
  int *****p8 = *(p7 + o8);
  GUARD(p8);
  int ****p9 = *(p8 + o9);
  GUARD(p9);
  int ***p10 = *(p9 + o10);
  GUARD(p10);
  int **p11 = *(p10 + o11);
  GUARD(p11);
  int *p12 = *(p11 + o12);
  GUARD(p12);
  return *(p12 + o13);
}

NOINLINE USED int plain_d14(int ************** p) {
  return *(*(*(*(*(*(*(*(*(*(*(*(*(*(p))))))))))))));
}

NOINLINE USED int const_d14(int ************** p) {
  return *(*(*(*(*(*(*(*(*(*(*(*(*(*(p + 2) + 5) + 17) + 3) + 7) + 11) + 13) + 19) + 2) + 5) + 17) + 3) + 7) + 11);
}

NOINLINE USED int dyn_d14(int ************** p, int o1, int o2, int o3, int o4, int o5, int o6, int o7, int o8, int o9, int o10, int o11, int o12, int o13, int o14) {
  return *(*(*(*(*(*(*(*(*(*(*(*(*(*(p + o1) + o2) + o3) + o4) + o5) + o6) + o7) + o8) + o9) + o10) + o11) + o12) + o13) + o14);
}

NOINLINE USED int checks_d14(int ************** p, int o1, int o2, int o3, int o4, int o5, int o6, int o7, int o8, int o9, int o10, int o11, int o12, int o13, int o14) {
  GUARD(p);
  int *************p1 = *(p + o1);
  GUARD(p1);
  int ************p2 = *(p1 + o2);
  GUARD(p2);
  int ***********p3 = *(p2 + o3);
  GUARD(p3);
  int **********p4 = *(p3 + o4);
  GUARD(p4);
  int *********p5 = *(p4 + o5);
  GUARD(p5);
  int ********p6 = *(p5 + o6);
  GUARD(p6);
  int *******p7 = *(p6 + o7);
  GUARD(p7);
  int ******p8 = *(p7 + o8);
  GUARD(p8);
  int *****p9 = *(p8 + o9);
  GUARD(p9);
  int ****p10 = *(p9 + o10);
  GUARD(p10);
  int ***p11 = *(p10 + o11);
  GUARD(p11);
  int **p12 = *(p11 + o12);
  GUARD(p12);
  int *p13 = *(p12 + o13);
  GUARD(p13);
  return *(p13 + o14);
}

NOINLINE USED int plain_d15(int *************** p) {
  return *(*(*(*(*(*(*(*(*(*(*(*(*(*(*(p)))))))))))))));
}

NOINLINE USED int const_d15(int *************** p) {
  return *(*(*(*(*(*(*(*(*(*(*(*(*(*(*(p + 2) + 5) + 17) + 3) + 7) + 11) + 13) + 19) + 2) + 5) + 17) + 3) + 7) + 11) + 13);
}

NOINLINE USED int dyn_d15(int *************** p, int o1, int o2, int o3, int o4, int o5, int o6, int o7, int o8, int o9, int o10, int o11, int o12, int o13, int o14, int o15) {
  return *(*(*(*(*(*(*(*(*(*(*(*(*(*(*(p + o1) + o2) + o3) + o4) + o5) + o6) + o7) + o8) + o9) + o10) + o11) + o12) + o13) + o14) + o15);
}

NOINLINE USED int checks_d15(int *************** p, int o1, int o2, int o3, int o4, int o5, int o6, int o7, int o8, int o9, int o10, int o11, int o12, int o13, int o14, int o15) {
  GUARD(p);
  int **************p1 = *(p + o1);
  GUARD(p1);
  int *************p2 = *(p1 + o2);
  GUARD(p2);
  int ************p3 = *(p2 + o3);
  GUARD(p3);
  int ***********p4 = *(p3 + o4);
  GUARD(p4);
  int **********p5 = *(p4 + o5);
  GUARD(p5);
  int *********p6 = *(p5 + o6);
  GUARD(p6);
  int ********p7 = *(p6 + o7);
  GUARD(p7);
  int *******p8 = *(p7 + o8);
  GUARD(p8);
  int ******p9 = *(p8 + o9);
  GUARD(p9);
  int *****p10 = *(p9 + o10);
  GUARD(p10);
  int ****p11 = *(p10 + o11);
  GUARD(p11);
  int ***p12 = *(p11 + o12);
  GUARD(p12);
  int **p13 = *(p12 + o13);
  GUARD(p13);
  int *p14 = *(p13 + o14);
  GUARD(p14);
  return *(p14 + o15);
}

NOINLINE USED int plain_d16(int **************** p) {
  return *(*(*(*(*(*(*(*(*(*(*(*(*(*(*(*(p))))))))))))))));
}

NOINLINE USED int const_d16(int **************** p) {
  return *(*(*(*(*(*(*(*(*(*(*(*(*(*(*(*(p + 2) + 5) + 17) + 3) + 7) + 11) + 13) + 19) + 2) + 5) + 17) + 3) + 7) + 11) + 13) + 19);
}

NOINLINE USED int dyn_d16(int **************** p, int o1, int o2, int o3, int o4, int o5, int o6, int o7, int o8, int o9, int o10, int o11, int o12, int o13, int o14, int o15, int o16) {
  return *(*(*(*(*(*(*(*(*(*(*(*(*(*(*(*(p + o1) + o2) + o3) + o4) + o5) + o6) + o7) + o8) + o9) + o10) + o11) + o12) + o13) + o14) + o15) + o16);
}

NOINLINE USED int checks_d16(int **************** p, int o1, int o2, int o3, int o4, int o5, int o6, int o7, int o8, int o9, int o10, int o11, int o12, int o13, int o14, int o15, int o16) {
  GUARD(p);
  int ***************p1 = *(p + o1);
  GUARD(p1);
  int **************p2 = *(p1 + o2);
  GUARD(p2);
  int *************p3 = *(p2 + o3);
  GUARD(p3);
  int ************p4 = *(p3 + o4);
  GUARD(p4);
  int ***********p5 = *(p4 + o5);
  GUARD(p5);
  int **********p6 = *(p5 + o6);
  GUARD(p6);
  int *********p7 = *(p6 + o7);
  GUARD(p7);
  int ********p8 = *(p7 + o8);
  GUARD(p8);
  int *******p9 = *(p8 + o9);
  GUARD(p9);
  int ******p10 = *(p9 + o10);
  GUARD(p10);
  int *****p11 = *(p10 + o11);
  GUARD(p11);
  int ****p12 = *(p11 + o12);
  GUARD(p12);
  int ***p13 = *(p12 + o13);
  GUARD(p13);
  int **p14 = *(p13 + o14);
  GUARD(p14);
  int *p15 = *(p14 + o15);
  GUARD(p15);
  return *(p15 + o16);
}
