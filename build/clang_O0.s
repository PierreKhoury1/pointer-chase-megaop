	.text
	.file	"generated_pointer_chase.c"
	.globl	plain_d2                        # -- Begin function plain_d2
	.p2align	4, 0x90
	.type	plain_d2,@function
plain_d2:                               # @plain_d2
# %bb.0:
	pushq	%rbp
	movq	%rsp, %rbp
	movq	%rdi, -8(%rbp)
	movq	-8(%rbp), %rax
	movq	(%rax), %rax
	movl	(%rax), %eax
	popq	%rbp
	retq
.Lfunc_end0:
	.size	plain_d2, .Lfunc_end0-plain_d2
                                        # -- End function
	.globl	const_d2                        # -- Begin function const_d2
	.p2align	4, 0x90
	.type	const_d2,@function
const_d2:                               # @const_d2
# %bb.0:
	pushq	%rbp
	movq	%rsp, %rbp
	movq	%rdi, -8(%rbp)
	movq	-8(%rbp), %rax
	movq	16(%rax), %rax
	movl	20(%rax), %eax
	popq	%rbp
	retq
.Lfunc_end1:
	.size	const_d2, .Lfunc_end1-const_d2
                                        # -- End function
	.globl	dyn_d2                          # -- Begin function dyn_d2
	.p2align	4, 0x90
	.type	dyn_d2,@function
dyn_d2:                                 # @dyn_d2
# %bb.0:
	pushq	%rbp
	movq	%rsp, %rbp
	movq	%rdi, -8(%rbp)
	movl	%esi, -12(%rbp)
	movl	%edx, -16(%rbp)
	movq	-8(%rbp), %rax
	movslq	-12(%rbp), %rcx
	movq	(%rax,%rcx,8), %rax
	movslq	-16(%rbp), %rcx
	movl	(%rax,%rcx,4), %eax
	popq	%rbp
	retq
.Lfunc_end2:
	.size	dyn_d2, .Lfunc_end2-dyn_d2
                                        # -- End function
	.globl	checks_d2                       # -- Begin function checks_d2
	.p2align	4, 0x90
	.type	checks_d2,@function
checks_d2:                              # @checks_d2
# %bb.0:
	pushq	%rbp
	movq	%rsp, %rbp
	movq	%rdi, -8(%rbp)
	movl	%esi, -12(%rbp)
	movl	%edx, -16(%rbp)
# %bb.1:
	cmpq	$0, -8(%rbp)
	jne	.LBB3_3
# %bb.2:
	ud2
.LBB3_3:
	jmp	.LBB3_4
.LBB3_4:
	movq	-8(%rbp), %rax
	movslq	-12(%rbp), %rcx
	movq	(%rax,%rcx,8), %rax
	movq	%rax, -24(%rbp)
# %bb.5:
	cmpq	$0, -24(%rbp)
	jne	.LBB3_7
# %bb.6:
	ud2
.LBB3_7:
	jmp	.LBB3_8
.LBB3_8:
	movq	-24(%rbp), %rax
	movslq	-16(%rbp), %rcx
	movl	(%rax,%rcx,4), %eax
	popq	%rbp
	retq
.Lfunc_end3:
	.size	checks_d2, .Lfunc_end3-checks_d2
                                        # -- End function
	.globl	plain_d3                        # -- Begin function plain_d3
	.p2align	4, 0x90
	.type	plain_d3,@function
plain_d3:                               # @plain_d3
# %bb.0:
	pushq	%rbp
	movq	%rsp, %rbp
	movq	%rdi, -8(%rbp)
	movq	-8(%rbp), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movl	(%rax), %eax
	popq	%rbp
	retq
.Lfunc_end4:
	.size	plain_d3, .Lfunc_end4-plain_d3
                                        # -- End function
	.globl	const_d3                        # -- Begin function const_d3
	.p2align	4, 0x90
	.type	const_d3,@function
const_d3:                               # @const_d3
# %bb.0:
	pushq	%rbp
	movq	%rsp, %rbp
	movq	%rdi, -8(%rbp)
	movq	-8(%rbp), %rax
	movq	16(%rax), %rax
	movq	40(%rax), %rax
	movl	68(%rax), %eax
	popq	%rbp
	retq
.Lfunc_end5:
	.size	const_d3, .Lfunc_end5-const_d3
                                        # -- End function
	.globl	dyn_d3                          # -- Begin function dyn_d3
	.p2align	4, 0x90
	.type	dyn_d3,@function
dyn_d3:                                 # @dyn_d3
# %bb.0:
	pushq	%rbp
	movq	%rsp, %rbp
	movq	%rdi, -8(%rbp)
	movl	%esi, -12(%rbp)
	movl	%edx, -16(%rbp)
	movl	%ecx, -20(%rbp)
	movq	-8(%rbp), %rax
	movslq	-12(%rbp), %rcx
	movq	(%rax,%rcx,8), %rax
	movslq	-16(%rbp), %rcx
	movq	(%rax,%rcx,8), %rax
	movslq	-20(%rbp), %rcx
	movl	(%rax,%rcx,4), %eax
	popq	%rbp
	retq
.Lfunc_end6:
	.size	dyn_d3, .Lfunc_end6-dyn_d3
                                        # -- End function
	.globl	checks_d3                       # -- Begin function checks_d3
	.p2align	4, 0x90
	.type	checks_d3,@function
checks_d3:                              # @checks_d3
# %bb.0:
	pushq	%rbp
	movq	%rsp, %rbp
	movq	%rdi, -8(%rbp)
	movl	%esi, -12(%rbp)
	movl	%edx, -16(%rbp)
	movl	%ecx, -20(%rbp)
# %bb.1:
	cmpq	$0, -8(%rbp)
	jne	.LBB7_3
# %bb.2:
	ud2
.LBB7_3:
	jmp	.LBB7_4
.LBB7_4:
	movq	-8(%rbp), %rax
	movslq	-12(%rbp), %rcx
	movq	(%rax,%rcx,8), %rax
	movq	%rax, -32(%rbp)
# %bb.5:
	cmpq	$0, -32(%rbp)
	jne	.LBB7_7
# %bb.6:
	ud2
.LBB7_7:
	jmp	.LBB7_8
.LBB7_8:
	movq	-32(%rbp), %rax
	movslq	-16(%rbp), %rcx
	movq	(%rax,%rcx,8), %rax
	movq	%rax, -40(%rbp)
# %bb.9:
	cmpq	$0, -40(%rbp)
	jne	.LBB7_11
# %bb.10:
	ud2
.LBB7_11:
	jmp	.LBB7_12
.LBB7_12:
	movq	-40(%rbp), %rax
	movslq	-20(%rbp), %rcx
	movl	(%rax,%rcx,4), %eax
	popq	%rbp
	retq
.Lfunc_end7:
	.size	checks_d3, .Lfunc_end7-checks_d3
                                        # -- End function
	.globl	plain_d5                        # -- Begin function plain_d5
	.p2align	4, 0x90
	.type	plain_d5,@function
plain_d5:                               # @plain_d5
# %bb.0:
	pushq	%rbp
	movq	%rsp, %rbp
	movq	%rdi, -8(%rbp)
	movq	-8(%rbp), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movl	(%rax), %eax
	popq	%rbp
	retq
.Lfunc_end8:
	.size	plain_d5, .Lfunc_end8-plain_d5
                                        # -- End function
	.globl	const_d5                        # -- Begin function const_d5
	.p2align	4, 0x90
	.type	const_d5,@function
const_d5:                               # @const_d5
# %bb.0:
	pushq	%rbp
	movq	%rsp, %rbp
	movq	%rdi, -8(%rbp)
	movq	-8(%rbp), %rax
	movq	16(%rax), %rax
	movq	40(%rax), %rax
	movq	136(%rax), %rax
	movq	24(%rax), %rax
	movl	28(%rax), %eax
	popq	%rbp
	retq
.Lfunc_end9:
	.size	const_d5, .Lfunc_end9-const_d5
                                        # -- End function
	.globl	dyn_d5                          # -- Begin function dyn_d5
	.p2align	4, 0x90
	.type	dyn_d5,@function
dyn_d5:                                 # @dyn_d5
# %bb.0:
	pushq	%rbp
	movq	%rsp, %rbp
	movq	%rdi, -8(%rbp)
	movl	%esi, -12(%rbp)
	movl	%edx, -16(%rbp)
	movl	%ecx, -20(%rbp)
	movl	%r8d, -24(%rbp)
	movl	%r9d, -28(%rbp)
	movq	-8(%rbp), %rax
	movslq	-12(%rbp), %rcx
	movq	(%rax,%rcx,8), %rax
	movslq	-16(%rbp), %rcx
	movq	(%rax,%rcx,8), %rax
	movslq	-20(%rbp), %rcx
	movq	(%rax,%rcx,8), %rax
	movslq	-24(%rbp), %rcx
	movq	(%rax,%rcx,8), %rax
	movslq	-28(%rbp), %rcx
	movl	(%rax,%rcx,4), %eax
	popq	%rbp
	retq
.Lfunc_end10:
	.size	dyn_d5, .Lfunc_end10-dyn_d5
                                        # -- End function
	.globl	checks_d5                       # -- Begin function checks_d5
	.p2align	4, 0x90
	.type	checks_d5,@function
checks_d5:                              # @checks_d5
# %bb.0:
	pushq	%rbp
	movq	%rsp, %rbp
	movq	%rdi, -8(%rbp)
	movl	%esi, -12(%rbp)
	movl	%edx, -16(%rbp)
	movl	%ecx, -20(%rbp)
	movl	%r8d, -24(%rbp)
	movl	%r9d, -28(%rbp)
# %bb.1:
	cmpq	$0, -8(%rbp)
	jne	.LBB11_3
# %bb.2:
	ud2
.LBB11_3:
	jmp	.LBB11_4
.LBB11_4:
	movq	-8(%rbp), %rax
	movslq	-12(%rbp), %rcx
	movq	(%rax,%rcx,8), %rax
	movq	%rax, -40(%rbp)
# %bb.5:
	cmpq	$0, -40(%rbp)
	jne	.LBB11_7
# %bb.6:
	ud2
.LBB11_7:
	jmp	.LBB11_8
.LBB11_8:
	movq	-40(%rbp), %rax
	movslq	-16(%rbp), %rcx
	movq	(%rax,%rcx,8), %rax
	movq	%rax, -48(%rbp)
# %bb.9:
	cmpq	$0, -48(%rbp)
	jne	.LBB11_11
# %bb.10:
	ud2
.LBB11_11:
	jmp	.LBB11_12
.LBB11_12:
	movq	-48(%rbp), %rax
	movslq	-20(%rbp), %rcx
	movq	(%rax,%rcx,8), %rax
	movq	%rax, -56(%rbp)
# %bb.13:
	cmpq	$0, -56(%rbp)
	jne	.LBB11_15
# %bb.14:
	ud2
.LBB11_15:
	jmp	.LBB11_16
.LBB11_16:
	movq	-56(%rbp), %rax
	movslq	-24(%rbp), %rcx
	movq	(%rax,%rcx,8), %rax
	movq	%rax, -64(%rbp)
# %bb.17:
	cmpq	$0, -64(%rbp)
	jne	.LBB11_19
# %bb.18:
	ud2
.LBB11_19:
	jmp	.LBB11_20
.LBB11_20:
	movq	-64(%rbp), %rax
	movslq	-28(%rbp), %rcx
	movl	(%rax,%rcx,4), %eax
	popq	%rbp
	retq
.Lfunc_end11:
	.size	checks_d5, .Lfunc_end11-checks_d5
                                        # -- End function
	.globl	plain_d8                        # -- Begin function plain_d8
	.p2align	4, 0x90
	.type	plain_d8,@function
plain_d8:                               # @plain_d8
# %bb.0:
	pushq	%rbp
	movq	%rsp, %rbp
	movq	%rdi, -8(%rbp)
	movq	-8(%rbp), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movl	(%rax), %eax
	popq	%rbp
	retq
.Lfunc_end12:
	.size	plain_d8, .Lfunc_end12-plain_d8
                                        # -- End function
	.globl	const_d8                        # -- Begin function const_d8
	.p2align	4, 0x90
	.type	const_d8,@function
const_d8:                               # @const_d8
# %bb.0:
	pushq	%rbp
	movq	%rsp, %rbp
	movq	%rdi, -8(%rbp)
	movq	-8(%rbp), %rax
	movq	16(%rax), %rax
	movq	40(%rax), %rax
	movq	136(%rax), %rax
	movq	24(%rax), %rax
	movq	56(%rax), %rax
	movq	88(%rax), %rax
	movq	104(%rax), %rax
	movl	76(%rax), %eax
	popq	%rbp
	retq
.Lfunc_end13:
	.size	const_d8, .Lfunc_end13-const_d8
                                        # -- End function
	.globl	dyn_d8                          # -- Begin function dyn_d8
	.p2align	4, 0x90
	.type	dyn_d8,@function
dyn_d8:                                 # @dyn_d8
# %bb.0:
	pushq	%rbp
	movq	%rsp, %rbp
	movl	32(%rbp), %eax
	movl	24(%rbp), %eax
	movl	16(%rbp), %eax
	movq	%rdi, -8(%rbp)
	movl	%esi, -12(%rbp)
	movl	%edx, -16(%rbp)
	movl	%ecx, -20(%rbp)
	movl	%r8d, -24(%rbp)
	movl	%r9d, -28(%rbp)
	movq	-8(%rbp), %rax
	movslq	-12(%rbp), %rcx
	movq	(%rax,%rcx,8), %rax
	movslq	-16(%rbp), %rcx
	movq	(%rax,%rcx,8), %rax
	movslq	-20(%rbp), %rcx
	movq	(%rax,%rcx,8), %rax
	movslq	-24(%rbp), %rcx
	movq	(%rax,%rcx,8), %rax
	movslq	-28(%rbp), %rcx
	movq	(%rax,%rcx,8), %rax
	movslq	16(%rbp), %rcx
	movq	(%rax,%rcx,8), %rax
	movslq	24(%rbp), %rcx
	movq	(%rax,%rcx,8), %rax
	movslq	32(%rbp), %rcx
	movl	(%rax,%rcx,4), %eax
	popq	%rbp
	retq
.Lfunc_end14:
	.size	dyn_d8, .Lfunc_end14-dyn_d8
                                        # -- End function
	.globl	checks_d8                       # -- Begin function checks_d8
	.p2align	4, 0x90
	.type	checks_d8,@function
checks_d8:                              # @checks_d8
# %bb.0:
	pushq	%rbp
	movq	%rsp, %rbp
	movl	32(%rbp), %eax
	movl	24(%rbp), %eax
	movl	16(%rbp), %eax
	movq	%rdi, -8(%rbp)
	movl	%esi, -12(%rbp)
	movl	%edx, -16(%rbp)
	movl	%ecx, -20(%rbp)
	movl	%r8d, -24(%rbp)
	movl	%r9d, -28(%rbp)
# %bb.1:
	cmpq	$0, -8(%rbp)
	jne	.LBB15_3
# %bb.2:
	ud2
.LBB15_3:
	jmp	.LBB15_4
.LBB15_4:
	movq	-8(%rbp), %rax
	movslq	-12(%rbp), %rcx
	movq	(%rax,%rcx,8), %rax
	movq	%rax, -40(%rbp)
# %bb.5:
	cmpq	$0, -40(%rbp)
	jne	.LBB15_7
# %bb.6:
	ud2
.LBB15_7:
	jmp	.LBB15_8
.LBB15_8:
	movq	-40(%rbp), %rax
	movslq	-16(%rbp), %rcx
	movq	(%rax,%rcx,8), %rax
	movq	%rax, -48(%rbp)
# %bb.9:
	cmpq	$0, -48(%rbp)
	jne	.LBB15_11
# %bb.10:
	ud2
.LBB15_11:
	jmp	.LBB15_12
.LBB15_12:
	movq	-48(%rbp), %rax
	movslq	-20(%rbp), %rcx
	movq	(%rax,%rcx,8), %rax
	movq	%rax, -56(%rbp)
# %bb.13:
	cmpq	$0, -56(%rbp)
	jne	.LBB15_15
# %bb.14:
	ud2
.LBB15_15:
	jmp	.LBB15_16
.LBB15_16:
	movq	-56(%rbp), %rax
	movslq	-24(%rbp), %rcx
	movq	(%rax,%rcx,8), %rax
	movq	%rax, -64(%rbp)
# %bb.17:
	cmpq	$0, -64(%rbp)
	jne	.LBB15_19
# %bb.18:
	ud2
.LBB15_19:
	jmp	.LBB15_20
.LBB15_20:
	movq	-64(%rbp), %rax
	movslq	-28(%rbp), %rcx
	movq	(%rax,%rcx,8), %rax
	movq	%rax, -72(%rbp)
# %bb.21:
	cmpq	$0, -72(%rbp)
	jne	.LBB15_23
# %bb.22:
	ud2
.LBB15_23:
	jmp	.LBB15_24
.LBB15_24:
	movq	-72(%rbp), %rax
	movslq	16(%rbp), %rcx
	movq	(%rax,%rcx,8), %rax
	movq	%rax, -80(%rbp)
# %bb.25:
	cmpq	$0, -80(%rbp)
	jne	.LBB15_27
# %bb.26:
	ud2
.LBB15_27:
	jmp	.LBB15_28
.LBB15_28:
	movq	-80(%rbp), %rax
	movslq	24(%rbp), %rcx
	movq	(%rax,%rcx,8), %rax
	movq	%rax, -88(%rbp)
# %bb.29:
	cmpq	$0, -88(%rbp)
	jne	.LBB15_31
# %bb.30:
	ud2
.LBB15_31:
	jmp	.LBB15_32
.LBB15_32:
	movq	-88(%rbp), %rax
	movslq	32(%rbp), %rcx
	movl	(%rax,%rcx,4), %eax
	popq	%rbp
	retq
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
