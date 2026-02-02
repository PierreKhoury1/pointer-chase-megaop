	.file	"generated_pointer_chase.c"
	.text
	.p2align 4
	.globl	plain_d2
	.type	plain_d2, @function
plain_d2:
	endbr64
	movq	(%rdi), %rax
	movl	(%rax), %eax
	ret
	.size	plain_d2, .-plain_d2
	.p2align 4
	.globl	const_d2
	.type	const_d2, @function
const_d2:
	endbr64
	movq	16(%rdi), %rax
	movl	20(%rax), %eax
	ret
	.size	const_d2, .-const_d2
	.p2align 4
	.globl	dyn_d2
	.type	dyn_d2, @function
dyn_d2:
	endbr64
	movslq	%esi, %rsi
	movslq	%edx, %rdx
	movq	(%rdi,%rsi,8), %rax
	movl	(%rax,%rdx,4), %eax
	ret
	.size	dyn_d2, .-dyn_d2
	.section	.text.unlikely,"ax",@progbits
.LCOLDB0:
	.text
.LHOTB0:
	.p2align 4
	.globl	checks_d2
	.type	checks_d2, @function
checks_d2:
	endbr64
	testq	%rdi, %rdi
	je	.L7
	movslq	%esi, %rsi
	movq	(%rdi,%rsi,8), %rax
	testq	%rax, %rax
	je	.L7
	movslq	%edx, %rdx
	movl	(%rax,%rdx,4), %eax
	ret
	.section	.text.unlikely
	.type	checks_d2.cold, @function
checks_d2.cold:
.L7:
	ud2
	.text
	.size	checks_d2, .-checks_d2
	.section	.text.unlikely
	.size	checks_d2.cold, .-checks_d2.cold
.LCOLDE0:
	.text
.LHOTE0:
	.p2align 4
	.globl	plain_d3
	.type	plain_d3, @function
plain_d3:
	endbr64
	movq	(%rdi), %rax
	movq	(%rax), %rax
	movl	(%rax), %eax
	ret
	.size	plain_d3, .-plain_d3
	.p2align 4
	.globl	const_d3
	.type	const_d3, @function
const_d3:
	endbr64
	movq	16(%rdi), %rax
	movq	40(%rax), %rax
	movl	68(%rax), %eax
	ret
	.size	const_d3, .-const_d3
	.p2align 4
	.globl	dyn_d3
	.type	dyn_d3, @function
dyn_d3:
	endbr64
	movslq	%esi, %rsi
	movslq	%edx, %rdx
	movslq	%ecx, %rcx
	movq	(%rdi,%rsi,8), %rax
	movq	(%rax,%rdx,8), %rax
	movl	(%rax,%rcx,4), %eax
	ret
	.size	dyn_d3, .-dyn_d3
	.section	.text.unlikely
.LCOLDB1:
	.text
.LHOTB1:
	.p2align 4
	.globl	checks_d3
	.type	checks_d3, @function
checks_d3:
	endbr64
	testq	%rdi, %rdi
	je	.L16
	movslq	%esi, %rsi
	movq	(%rdi,%rsi,8), %rax
	testq	%rax, %rax
	je	.L16
	movslq	%edx, %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L16
	movslq	%ecx, %rcx
	movl	(%rax,%rcx,4), %eax
	ret
	.section	.text.unlikely
	.type	checks_d3.cold, @function
checks_d3.cold:
.L16:
	ud2
	.text
	.size	checks_d3, .-checks_d3
	.section	.text.unlikely
	.size	checks_d3.cold, .-checks_d3.cold
.LCOLDE1:
	.text
.LHOTE1:
	.p2align 4
	.globl	plain_d5
	.type	plain_d5, @function
plain_d5:
	endbr64
	movq	(%rdi), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movl	(%rax), %eax
	ret
	.size	plain_d5, .-plain_d5
	.p2align 4
	.globl	const_d5
	.type	const_d5, @function
const_d5:
	endbr64
	movq	16(%rdi), %rax
	movq	40(%rax), %rax
	movq	136(%rax), %rax
	movq	24(%rax), %rax
	movl	28(%rax), %eax
	ret
	.size	const_d5, .-const_d5
	.p2align 4
	.globl	dyn_d5
	.type	dyn_d5, @function
dyn_d5:
	endbr64
	movslq	%esi, %rsi
	movslq	%edx, %rdx
	movslq	%ecx, %rcx
	movslq	%r8d, %r8
	movq	(%rdi,%rsi,8), %rax
	movslq	%r9d, %r9
	movq	(%rax,%rdx,8), %rax
	movq	(%rax,%rcx,8), %rax
	movq	(%rax,%r8,8), %rax
	movl	(%rax,%r9,4), %eax
	ret
	.size	dyn_d5, .-dyn_d5
	.section	.text.unlikely
.LCOLDB2:
	.text
.LHOTB2:
	.p2align 4
	.globl	checks_d5
	.type	checks_d5, @function
checks_d5:
	endbr64
	testq	%rdi, %rdi
	je	.L28
	movslq	%esi, %rsi
	movq	(%rdi,%rsi,8), %rax
	testq	%rax, %rax
	je	.L28
	movslq	%edx, %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L28
	movslq	%ecx, %rcx
	movq	(%rax,%rcx,8), %rax
	testq	%rax, %rax
	je	.L28
	movslq	%r8d, %r8
	movq	(%rax,%r8,8), %rax
	testq	%rax, %rax
	je	.L28
	movslq	%r9d, %r9
	movl	(%rax,%r9,4), %eax
	ret
	.section	.text.unlikely
	.type	checks_d5.cold, @function
checks_d5.cold:
.L28:
	ud2
	.text
	.size	checks_d5, .-checks_d5
	.section	.text.unlikely
	.size	checks_d5.cold, .-checks_d5.cold
.LCOLDE2:
	.text
.LHOTE2:
	.p2align 4
	.globl	plain_d8
	.type	plain_d8, @function
plain_d8:
	endbr64
	movq	(%rdi), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movl	(%rax), %eax
	ret
	.size	plain_d8, .-plain_d8
	.p2align 4
	.globl	const_d8
	.type	const_d8, @function
const_d8:
	endbr64
	movq	16(%rdi), %rax
	movq	40(%rax), %rax
	movq	136(%rax), %rax
	movq	24(%rax), %rax
	movq	56(%rax), %rax
	movq	88(%rax), %rax
	movq	104(%rax), %rax
	movl	76(%rax), %eax
	ret
	.size	const_d8, .-const_d8
	.p2align 4
	.globl	dyn_d8
	.type	dyn_d8, @function
dyn_d8:
	endbr64
	movslq	%esi, %rsi
	movslq	%edx, %rdx
	movslq	%ecx, %rcx
	movslq	%r8d, %r8
	movq	(%rdi,%rsi,8), %rax
	movslq	%r9d, %r9
	movq	(%rax,%rdx,8), %rax
	movslq	8(%rsp), %rdx
	movq	(%rax,%rcx,8), %rax
	movslq	16(%rsp), %rcx
	movq	(%rax,%r8,8), %rax
	movq	(%rax,%r9,8), %rax
	movq	(%rax,%rdx,8), %rax
	movslq	24(%rsp), %rdx
	movq	(%rax,%rcx,8), %rax
	movl	(%rax,%rdx,4), %eax
	ret
	.size	dyn_d8, .-dyn_d8
	.section	.text.unlikely
.LCOLDB3:
	.text
.LHOTB3:
	.p2align 4
	.globl	checks_d8
	.type	checks_d8, @function
checks_d8:
	endbr64
	testq	%rdi, %rdi
	je	.L46
	movslq	%esi, %rsi
	movq	(%rdi,%rsi,8), %rax
	testq	%rax, %rax
	je	.L46
	movslq	%edx, %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L46
	movslq	%ecx, %rcx
	movq	(%rax,%rcx,8), %rax
	testq	%rax, %rax
	je	.L46
	movslq	%r8d, %r8
	movq	(%rax,%r8,8), %rax
	testq	%rax, %rax
	je	.L46
	movslq	%r9d, %r9
	movq	(%rax,%r9,8), %rax
	testq	%rax, %rax
	je	.L46
	movslq	8(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L46
	movslq	16(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L46
	movslq	24(%rsp), %rdx
	movl	(%rax,%rdx,4), %eax
	ret
	.section	.text.unlikely
	.type	checks_d8.cold, @function
checks_d8.cold:
.L46:
	ud2
	.text
	.size	checks_d8, .-checks_d8
	.section	.text.unlikely
	.size	checks_d8.cold, .-checks_d8.cold
.LCOLDE3:
	.text
.LHOTE3:
	.section	.note.GNU-stack,"",@progbits
	.section	.note.gnu.property,"a"
	.align 8
	.long	1f - 0f
	.long	4f - 1f
	.long	5
0:
	.string	"GNU"
1:
	.align 8
	.long	0xc0000002
	.long	3f - 2f
2:
	.long	0x3
3:
	.align 8
4:
