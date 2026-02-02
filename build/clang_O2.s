	.text
	.file	"generated_pointer_chase.c"
	.globl	plain_d2                        # -- Begin function plain_d2
	.p2align	4, 0x90
	.type	plain_d2,@function
plain_d2:                               # @plain_d2
# %bb.0:
	movq	(%rdi), %rax
	movl	(%rax), %eax
	retq
.Lfunc_end0:
	.size	plain_d2, .Lfunc_end0-plain_d2
                                        # -- End function
	.globl	const_d2                        # -- Begin function const_d2
	.p2align	4, 0x90
	.type	const_d2,@function
const_d2:                               # @const_d2
# %bb.0:
	movq	16(%rdi), %rax
	movl	20(%rax), %eax
	retq
.Lfunc_end1:
	.size	const_d2, .Lfunc_end1-const_d2
                                        # -- End function
	.globl	dyn_d2                          # -- Begin function dyn_d2
	.p2align	4, 0x90
	.type	dyn_d2,@function
dyn_d2:                                 # @dyn_d2
# %bb.0:
	movslq	%esi, %rax
	movq	(%rdi,%rax,8), %rax
	movslq	%edx, %rcx
	movl	(%rax,%rcx,4), %eax
	retq
.Lfunc_end2:
	.size	dyn_d2, .Lfunc_end2-dyn_d2
                                        # -- End function
	.globl	checks_d2                       # -- Begin function checks_d2
	.p2align	4, 0x90
	.type	checks_d2,@function
checks_d2:                              # @checks_d2
# %bb.0:
	testq	%rdi, %rdi
	je	.LBB3_3
# %bb.1:
	movslq	%esi, %rax
	movq	(%rdi,%rax,8), %rax
	testq	%rax, %rax
	je	.LBB3_3
# %bb.2:
	movslq	%edx, %rcx
	movl	(%rax,%rcx,4), %eax
	retq
.LBB3_3:
	ud2
.Lfunc_end3:
	.size	checks_d2, .Lfunc_end3-checks_d2
                                        # -- End function
	.globl	plain_d3                        # -- Begin function plain_d3
	.p2align	4, 0x90
	.type	plain_d3,@function
plain_d3:                               # @plain_d3
# %bb.0:
	movq	(%rdi), %rax
	movq	(%rax), %rax
	movl	(%rax), %eax
	retq
.Lfunc_end4:
	.size	plain_d3, .Lfunc_end4-plain_d3
                                        # -- End function
	.globl	const_d3                        # -- Begin function const_d3
	.p2align	4, 0x90
	.type	const_d3,@function
const_d3:                               # @const_d3
# %bb.0:
	movq	16(%rdi), %rax
	movq	40(%rax), %rax
	movl	68(%rax), %eax
	retq
.Lfunc_end5:
	.size	const_d3, .Lfunc_end5-const_d3
                                        # -- End function
	.globl	dyn_d3                          # -- Begin function dyn_d3
	.p2align	4, 0x90
	.type	dyn_d3,@function
dyn_d3:                                 # @dyn_d3
# %bb.0:
	movslq	%esi, %rax
	movq	(%rdi,%rax,8), %rax
	movslq	%edx, %rdx
	movq	(%rax,%rdx,8), %rax
	movslq	%ecx, %rcx
	movl	(%rax,%rcx,4), %eax
	retq
.Lfunc_end6:
	.size	dyn_d3, .Lfunc_end6-dyn_d3
                                        # -- End function
	.globl	checks_d3                       # -- Begin function checks_d3
	.p2align	4, 0x90
	.type	checks_d3,@function
checks_d3:                              # @checks_d3
# %bb.0:
	testq	%rdi, %rdi
	je	.LBB7_4
# %bb.1:
	movslq	%esi, %rax
	movq	(%rdi,%rax,8), %rax
	testq	%rax, %rax
	je	.LBB7_4
# %bb.2:
	movslq	%edx, %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.LBB7_4
# %bb.3:
	movslq	%ecx, %rcx
	movl	(%rax,%rcx,4), %eax
	retq
.LBB7_4:
	ud2
.Lfunc_end7:
	.size	checks_d3, .Lfunc_end7-checks_d3
                                        # -- End function
	.globl	plain_d5                        # -- Begin function plain_d5
	.p2align	4, 0x90
	.type	plain_d5,@function
plain_d5:                               # @plain_d5
# %bb.0:
	movq	(%rdi), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movl	(%rax), %eax
	retq
.Lfunc_end8:
	.size	plain_d5, .Lfunc_end8-plain_d5
                                        # -- End function
	.globl	const_d5                        # -- Begin function const_d5
	.p2align	4, 0x90
	.type	const_d5,@function
const_d5:                               # @const_d5
# %bb.0:
	movq	16(%rdi), %rax
	movq	40(%rax), %rax
	movq	136(%rax), %rax
	movq	24(%rax), %rax
	movl	28(%rax), %eax
	retq
.Lfunc_end9:
	.size	const_d5, .Lfunc_end9-const_d5
                                        # -- End function
	.globl	dyn_d5                          # -- Begin function dyn_d5
	.p2align	4, 0x90
	.type	dyn_d5,@function
dyn_d5:                                 # @dyn_d5
# %bb.0:
	movslq	%esi, %rax
	movq	(%rdi,%rax,8), %rax
	movslq	%edx, %rdx
	movq	(%rax,%rdx,8), %rax
	movslq	%ecx, %rcx
	movq	(%rax,%rcx,8), %rax
	movslq	%r8d, %rcx
	movq	(%rax,%rcx,8), %rax
	movslq	%r9d, %rcx
	movl	(%rax,%rcx,4), %eax
	retq
.Lfunc_end10:
	.size	dyn_d5, .Lfunc_end10-dyn_d5
                                        # -- End function
	.globl	checks_d5                       # -- Begin function checks_d5
	.p2align	4, 0x90
	.type	checks_d5,@function
checks_d5:                              # @checks_d5
# %bb.0:
	testq	%rdi, %rdi
	je	.LBB11_6
# %bb.1:
	movslq	%esi, %rax
	movq	(%rdi,%rax,8), %rax
	testq	%rax, %rax
	je	.LBB11_6
# %bb.2:
	movslq	%edx, %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.LBB11_6
# %bb.3:
	movslq	%ecx, %rcx
	movq	(%rax,%rcx,8), %rax
	testq	%rax, %rax
	je	.LBB11_6
# %bb.4:
	movslq	%r8d, %rcx
	movq	(%rax,%rcx,8), %rax
	testq	%rax, %rax
	je	.LBB11_6
# %bb.5:
	movslq	%r9d, %rcx
	movl	(%rax,%rcx,4), %eax
	retq
.LBB11_6:
	ud2
.Lfunc_end11:
	.size	checks_d5, .Lfunc_end11-checks_d5
                                        # -- End function
	.globl	plain_d8                        # -- Begin function plain_d8
	.p2align	4, 0x90
	.type	plain_d8,@function
plain_d8:                               # @plain_d8
# %bb.0:
	movq	(%rdi), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movl	(%rax), %eax
	retq
.Lfunc_end12:
	.size	plain_d8, .Lfunc_end12-plain_d8
                                        # -- End function
	.globl	const_d8                        # -- Begin function const_d8
	.p2align	4, 0x90
	.type	const_d8,@function
const_d8:                               # @const_d8
# %bb.0:
	movq	16(%rdi), %rax
	movq	40(%rax), %rax
	movq	136(%rax), %rax
	movq	24(%rax), %rax
	movq	56(%rax), %rax
	movq	88(%rax), %rax
	movq	104(%rax), %rax
	movl	76(%rax), %eax
	retq
.Lfunc_end13:
	.size	const_d8, .Lfunc_end13-const_d8
                                        # -- End function
	.globl	dyn_d8                          # -- Begin function dyn_d8
	.p2align	4, 0x90
	.type	dyn_d8,@function
dyn_d8:                                 # @dyn_d8
# %bb.0:
	movslq	24(%rsp), %rax
	movslq	16(%rsp), %r10
	movslq	8(%rsp), %r11
	movslq	%esi, %rsi
	movq	(%rdi,%rsi,8), %rsi
	movslq	%edx, %rdx
	movq	(%rsi,%rdx,8), %rdx
	movslq	%ecx, %rcx
	movq	(%rdx,%rcx,8), %rcx
	movslq	%r8d, %rdx
	movq	(%rcx,%rdx,8), %rcx
	movslq	%r9d, %rdx
	movq	(%rcx,%rdx,8), %rcx
	movq	(%rcx,%r11,8), %rcx
	movq	(%rcx,%r10,8), %rcx
	movl	(%rcx,%rax,4), %eax
	retq
.Lfunc_end14:
	.size	dyn_d8, .Lfunc_end14-dyn_d8
                                        # -- End function
	.globl	checks_d8                       # -- Begin function checks_d8
	.p2align	4, 0x90
	.type	checks_d8,@function
checks_d8:                              # @checks_d8
# %bb.0:
	testq	%rdi, %rdi
	je	.LBB15_9
# %bb.1:
	movslq	%esi, %rax
	movq	(%rdi,%rax,8), %rax
	testq	%rax, %rax
	je	.LBB15_9
# %bb.2:
	movslq	%edx, %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.LBB15_9
# %bb.3:
	movslq	%ecx, %rcx
	movq	(%rax,%rcx,8), %rax
	testq	%rax, %rax
	je	.LBB15_9
# %bb.4:
	movslq	%r8d, %rcx
	movq	(%rax,%rcx,8), %rax
	testq	%rax, %rax
	je	.LBB15_9
# %bb.5:
	movslq	%r9d, %rcx
	movq	(%rax,%rcx,8), %rax
	testq	%rax, %rax
	je	.LBB15_9
# %bb.6:
	movslq	8(%rsp), %rcx
	movq	(%rax,%rcx,8), %rax
	testq	%rax, %rax
	je	.LBB15_9
# %bb.7:
	movslq	16(%rsp), %rcx
	movq	(%rax,%rcx,8), %rax
	testq	%rax, %rax
	je	.LBB15_9
# %bb.8:
	movslq	24(%rsp), %rcx
	movl	(%rax,%rcx,4), %eax
	retq
.LBB15_9:
	ud2
.Lfunc_end15:
	.size	checks_d8, .Lfunc_end15-checks_d8
                                        # -- End function
	.section	".note.GNU-stack","",@progbits
	.addrsig
	.addrsig_sym plain_d2
	.addrsig_sym const_d2
	.addrsig_sym dyn_d2
	.addrsig_sym checks_d2
	.addrsig_sym plain_d3
	.addrsig_sym const_d3
	.addrsig_sym dyn_d3
	.addrsig_sym checks_d3
	.addrsig_sym plain_d5
	.addrsig_sym const_d5
	.addrsig_sym dyn_d5
	.addrsig_sym checks_d5
	.addrsig_sym plain_d8
	.addrsig_sym const_d8
	.addrsig_sym dyn_d8
	.addrsig_sym checks_d8
