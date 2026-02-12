; ModuleID = 'ptrchase_baseline.c'
source_filename = "ptrchase_baseline.c"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

; Function Attrs: nofree noinline norecurse nosync nounwind memory(read, inaccessiblemem: none) uwtable
define dso_local ptr @chase_normal(ptr noundef readonly %0, i32 noundef %1) local_unnamed_addr #0 {
  %3 = icmp sgt i32 %1, 0
  br i1 %3, label %4, label %19

4:                                                ; preds = %2
  %5 = and i32 %1, 7
  %6 = icmp ult i32 %1, 8
  br i1 %6, label %9, label %7

7:                                                ; preds = %4
  %8 = and i32 %1, 2147483640
  br label %21

9:                                                ; preds = %21, %4
  %10 = phi ptr [ undef, %4 ], [ %31, %21 ]
  %11 = phi ptr [ %0, %4 ], [ %31, %21 ]
  %12 = icmp eq i32 %5, 0
  br i1 %12, label %19, label %13

13:                                               ; preds = %9, %13
  %14 = phi ptr [ %16, %13 ], [ %11, %9 ]
  %15 = phi i32 [ %17, %13 ], [ 0, %9 ]
  %16 = load ptr, ptr %14, align 8, !tbaa !5
  %17 = add i32 %15, 1
  %18 = icmp eq i32 %17, %5
  br i1 %18, label %19, label %13, !llvm.loop !11

19:                                               ; preds = %9, %13, %2
  %20 = phi ptr [ %0, %2 ], [ %10, %9 ], [ %16, %13 ]
  ret ptr %20

21:                                               ; preds = %21, %7
  %22 = phi ptr [ %0, %7 ], [ %31, %21 ]
  %23 = phi i32 [ 0, %7 ], [ %32, %21 ]
  %24 = load ptr, ptr %22, align 8, !tbaa !5
  %25 = load ptr, ptr %24, align 8, !tbaa !5
  %26 = load ptr, ptr %25, align 8, !tbaa !5
  %27 = load ptr, ptr %26, align 8, !tbaa !5
  %28 = load ptr, ptr %27, align 8, !tbaa !5
  %29 = load ptr, ptr %28, align 8, !tbaa !5
  %30 = load ptr, ptr %29, align 8, !tbaa !5
  %31 = load ptr, ptr %30, align 8, !tbaa !5
  %32 = add i32 %23, 8
  %33 = icmp eq i32 %32, %8
  br i1 %33, label %9, label %21, !llvm.loop !13
}

attributes #0 = { nofree noinline norecurse nosync nounwind memory(read, inaccessiblemem: none) uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }

!llvm.module.flags = !{!0, !1, !2, !3}
!llvm.ident = !{!4}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{i32 8, !"PIC Level", i32 2}
!2 = !{i32 7, !"PIE Level", i32 2}
!3 = !{i32 7, !"uwtable", i32 2}
!4 = !{!"Ubuntu clang version 18.1.3 (1ubuntu1)"}
!5 = !{!6, !7, i64 0}
!6 = !{!"Node", !7, i64 0, !10, i64 8}
!7 = !{!"any pointer", !8, i64 0}
!8 = !{!"omnipotent char", !9, i64 0}
!9 = !{!"Simple C/C++ TBAA"}
!10 = !{!"int", !8, i64 0}
!11 = distinct !{!11, !12}
!12 = !{!"llvm.loop.unroll.disable"}
!13 = distinct !{!13, !14}
!14 = !{!"llvm.loop.mustprogress"}
