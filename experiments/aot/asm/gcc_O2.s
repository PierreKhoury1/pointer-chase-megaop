	.file	"generated_pointer_chase.c"
	.text
	.p2align 4
	.globl	plain_d1
	.type	plain_d1, @function
plain_d1:
	endbr64
	movl	(%rdi), %eax
	ret
	.size	plain_d1, .-plain_d1
	.p2align 4
	.globl	const_d1
	.type	const_d1, @function
const_d1:
	endbr64
	movl	8(%rdi), %eax
	ret
	.size	const_d1, .-const_d1
	.p2align 4
	.globl	dyn_d1
	.type	dyn_d1, @function
dyn_d1:
	endbr64
	movslq	%esi, %rsi
	movl	(%rdi,%rsi,4), %eax
	ret
	.size	dyn_d1, .-dyn_d1
	.section	.text.unlikely,"ax",@progbits
.LCOLDB0:
	.text
.LHOTB0:
	.p2align 4
	.globl	checks_d1
	.type	checks_d1, @function
checks_d1:
	endbr64
	testq	%rdi, %rdi
	je	.L7
	movslq	%esi, %rsi
	movl	(%rdi,%rsi,4), %eax
	ret
	.section	.text.unlikely
	.type	checks_d1.cold, @function
checks_d1.cold:
.L7:
	ud2
	.text
	.size	checks_d1, .-checks_d1
	.section	.text.unlikely
	.size	checks_d1.cold, .-checks_d1.cold
.LCOLDE0:
	.text
.LHOTE0:
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
	.section	.text.unlikely
.LCOLDB1:
	.text
.LHOTB1:
	.p2align 4
	.globl	checks_d2
	.type	checks_d2, @function
checks_d2:
	endbr64
	testq	%rdi, %rdi
	je	.L13
	movslq	%esi, %rsi
	movq	(%rdi,%rsi,8), %rax
	testq	%rax, %rax
	je	.L13
	movslq	%edx, %rdx
	movl	(%rax,%rdx,4), %eax
	ret
	.section	.text.unlikely
	.type	checks_d2.cold, @function
checks_d2.cold:
.L13:
	ud2
	.text
	.size	checks_d2, .-checks_d2
	.section	.text.unlikely
	.size	checks_d2.cold, .-checks_d2.cold
.LCOLDE1:
	.text
.LHOTE1:
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
.LCOLDB2:
	.text
.LHOTB2:
	.p2align 4
	.globl	checks_d3
	.type	checks_d3, @function
checks_d3:
	endbr64
	testq	%rdi, %rdi
	je	.L22
	movslq	%esi, %rsi
	movq	(%rdi,%rsi,8), %rax
	testq	%rax, %rax
	je	.L22
	movslq	%edx, %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L22
	movslq	%ecx, %rcx
	movl	(%rax,%rcx,4), %eax
	ret
	.section	.text.unlikely
	.type	checks_d3.cold, @function
checks_d3.cold:
.L22:
	ud2
	.text
	.size	checks_d3, .-checks_d3
	.section	.text.unlikely
	.size	checks_d3.cold, .-checks_d3.cold
.LCOLDE2:
	.text
.LHOTE2:
	.p2align 4
	.globl	plain_d4
	.type	plain_d4, @function
plain_d4:
	endbr64
	movq	(%rdi), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movl	(%rax), %eax
	ret
	.size	plain_d4, .-plain_d4
	.p2align 4
	.globl	const_d4
	.type	const_d4, @function
const_d4:
	endbr64
	movq	16(%rdi), %rax
	movq	40(%rax), %rax
	movq	136(%rax), %rax
	movl	12(%rax), %eax
	ret
	.size	const_d4, .-const_d4
	.p2align 4
	.globl	dyn_d4
	.type	dyn_d4, @function
dyn_d4:
	endbr64
	movslq	%esi, %rsi
	movslq	%edx, %rdx
	movslq	%ecx, %rcx
	movslq	%r8d, %r8
	movq	(%rdi,%rsi,8), %rax
	movq	(%rax,%rdx,8), %rax
	movq	(%rax,%rcx,8), %rax
	movl	(%rax,%r8,4), %eax
	ret
	.size	dyn_d4, .-dyn_d4
	.section	.text.unlikely
.LCOLDB3:
	.text
.LHOTB3:
	.p2align 4
	.globl	checks_d4
	.type	checks_d4, @function
checks_d4:
	endbr64
	testq	%rdi, %rdi
	je	.L34
	movslq	%esi, %rsi
	movq	(%rdi,%rsi,8), %rax
	testq	%rax, %rax
	je	.L34
	movslq	%edx, %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L34
	movslq	%ecx, %rcx
	movq	(%rax,%rcx,8), %rax
	testq	%rax, %rax
	je	.L34
	movslq	%r8d, %r8
	movl	(%rax,%r8,4), %eax
	ret
	.section	.text.unlikely
	.type	checks_d4.cold, @function
checks_d4.cold:
.L34:
	ud2
	.text
	.size	checks_d4, .-checks_d4
	.section	.text.unlikely
	.size	checks_d4.cold, .-checks_d4.cold
.LCOLDE3:
	.text
.LHOTE3:
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
.LCOLDB4:
	.text
.LHOTB4:
	.p2align 4
	.globl	checks_d5
	.type	checks_d5, @function
checks_d5:
	endbr64
	testq	%rdi, %rdi
	je	.L49
	movslq	%esi, %rsi
	movq	(%rdi,%rsi,8), %rax
	testq	%rax, %rax
	je	.L49
	movslq	%edx, %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L49
	movslq	%ecx, %rcx
	movq	(%rax,%rcx,8), %rax
	testq	%rax, %rax
	je	.L49
	movslq	%r8d, %r8
	movq	(%rax,%r8,8), %rax
	testq	%rax, %rax
	je	.L49
	movslq	%r9d, %r9
	movl	(%rax,%r9,4), %eax
	ret
	.section	.text.unlikely
	.type	checks_d5.cold, @function
checks_d5.cold:
.L49:
	ud2
	.text
	.size	checks_d5, .-checks_d5
	.section	.text.unlikely
	.size	checks_d5.cold, .-checks_d5.cold
.LCOLDE4:
	.text
.LHOTE4:
	.p2align 4
	.globl	plain_d6
	.type	plain_d6, @function
plain_d6:
	endbr64
	movq	(%rdi), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movl	(%rax), %eax
	ret
	.size	plain_d6, .-plain_d6
	.p2align 4
	.globl	const_d6
	.type	const_d6, @function
const_d6:
	endbr64
	movq	16(%rdi), %rax
	movq	40(%rax), %rax
	movq	136(%rax), %rax
	movq	24(%rax), %rax
	movq	56(%rax), %rax
	movl	44(%rax), %eax
	ret
	.size	const_d6, .-const_d6
	.p2align 4
	.globl	dyn_d6
	.type	dyn_d6, @function
dyn_d6:
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
	movq	(%rax,%r8,8), %rax
	movq	(%rax,%r9,8), %rax
	movl	(%rax,%rdx,4), %eax
	ret
	.size	dyn_d6, .-dyn_d6
	.section	.text.unlikely
.LCOLDB5:
	.text
.LHOTB5:
	.p2align 4
	.globl	checks_d6
	.type	checks_d6, @function
checks_d6:
	endbr64
	testq	%rdi, %rdi
	je	.L67
	movslq	%esi, %rsi
	movq	(%rdi,%rsi,8), %rax
	testq	%rax, %rax
	je	.L67
	movslq	%edx, %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L67
	movslq	%ecx, %rcx
	movq	(%rax,%rcx,8), %rax
	testq	%rax, %rax
	je	.L67
	movslq	%r8d, %r8
	movq	(%rax,%r8,8), %rax
	testq	%rax, %rax
	je	.L67
	movslq	%r9d, %r9
	movq	(%rax,%r9,8), %rax
	testq	%rax, %rax
	je	.L67
	movslq	8(%rsp), %rdx
	movl	(%rax,%rdx,4), %eax
	ret
	.section	.text.unlikely
	.type	checks_d6.cold, @function
checks_d6.cold:
.L67:
	ud2
	.text
	.size	checks_d6, .-checks_d6
	.section	.text.unlikely
	.size	checks_d6.cold, .-checks_d6.cold
.LCOLDE5:
	.text
.LHOTE5:
	.p2align 4
	.globl	plain_d7
	.type	plain_d7, @function
plain_d7:
	endbr64
	movq	(%rdi), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movl	(%rax), %eax
	ret
	.size	plain_d7, .-plain_d7
	.p2align 4
	.globl	const_d7
	.type	const_d7, @function
const_d7:
	endbr64
	movq	16(%rdi), %rax
	movq	40(%rax), %rax
	movq	136(%rax), %rax
	movq	24(%rax), %rax
	movq	56(%rax), %rax
	movq	88(%rax), %rax
	movl	52(%rax), %eax
	ret
	.size	const_d7, .-const_d7
	.p2align 4
	.globl	dyn_d7
	.type	dyn_d7, @function
dyn_d7:
	endbr64
	movslq	%esi, %rsi
	movslq	%edx, %rdx
	movslq	%ecx, %rcx
	movslq	%r8d, %r8
	movq	(%rdi,%rsi,8), %rax
	movslq	%r9d, %r9
	movq	(%rax,%rdx,8), %rax
	movslq	16(%rsp), %rdx
	movq	(%rax,%rcx,8), %rax
	movslq	8(%rsp), %rcx
	movq	(%rax,%r8,8), %rax
	movq	(%rax,%r9,8), %rax
	movq	(%rax,%rcx,8), %rax
	movl	(%rax,%rdx,4), %eax
	ret
	.size	dyn_d7, .-dyn_d7
	.section	.text.unlikely
.LCOLDB6:
	.text
.LHOTB6:
	.p2align 4
	.globl	checks_d7
	.type	checks_d7, @function
checks_d7:
	endbr64
	testq	%rdi, %rdi
	je	.L88
	movslq	%esi, %rsi
	movq	(%rdi,%rsi,8), %rax
	testq	%rax, %rax
	je	.L88
	movslq	%edx, %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L88
	movslq	%ecx, %rcx
	movq	(%rax,%rcx,8), %rax
	testq	%rax, %rax
	je	.L88
	movslq	%r8d, %r8
	movq	(%rax,%r8,8), %rax
	testq	%rax, %rax
	je	.L88
	movslq	%r9d, %r9
	movq	(%rax,%r9,8), %rax
	testq	%rax, %rax
	je	.L88
	movslq	8(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L88
	movslq	16(%rsp), %rdx
	movl	(%rax,%rdx,4), %eax
	ret
	.section	.text.unlikely
	.type	checks_d7.cold, @function
checks_d7.cold:
.L88:
	ud2
	.text
	.size	checks_d7, .-checks_d7
	.section	.text.unlikely
	.size	checks_d7.cold, .-checks_d7.cold
.LCOLDE6:
	.text
.LHOTE6:
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
.LCOLDB7:
	.text
.LHOTB7:
	.p2align 4
	.globl	checks_d8
	.type	checks_d8, @function
checks_d8:
	endbr64
	testq	%rdi, %rdi
	je	.L112
	movslq	%esi, %rsi
	movq	(%rdi,%rsi,8), %rax
	testq	%rax, %rax
	je	.L112
	movslq	%edx, %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L112
	movslq	%ecx, %rcx
	movq	(%rax,%rcx,8), %rax
	testq	%rax, %rax
	je	.L112
	movslq	%r8d, %r8
	movq	(%rax,%r8,8), %rax
	testq	%rax, %rax
	je	.L112
	movslq	%r9d, %r9
	movq	(%rax,%r9,8), %rax
	testq	%rax, %rax
	je	.L112
	movslq	8(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L112
	movslq	16(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L112
	movslq	24(%rsp), %rdx
	movl	(%rax,%rdx,4), %eax
	ret
	.section	.text.unlikely
	.type	checks_d8.cold, @function
checks_d8.cold:
.L112:
	ud2
	.text
	.size	checks_d8, .-checks_d8
	.section	.text.unlikely
	.size	checks_d8.cold, .-checks_d8.cold
.LCOLDE7:
	.text
.LHOTE7:
	.p2align 4
	.globl	plain_d9
	.type	plain_d9, @function
plain_d9:
	endbr64
	movq	(%rdi), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movl	(%rax), %eax
	ret
	.size	plain_d9, .-plain_d9
	.p2align 4
	.globl	const_d9
	.type	const_d9, @function
const_d9:
	endbr64
	movq	16(%rdi), %rax
	movq	40(%rax), %rax
	movq	136(%rax), %rax
	movq	24(%rax), %rax
	movq	56(%rax), %rax
	movq	88(%rax), %rax
	movq	104(%rax), %rax
	movq	152(%rax), %rax
	movl	8(%rax), %eax
	ret
	.size	const_d9, .-const_d9
	.p2align 4
	.globl	dyn_d9
	.type	dyn_d9, @function
dyn_d9:
	endbr64
	movslq	%esi, %rsi
	movslq	%edx, %rdx
	movslq	%ecx, %rcx
	movslq	%r8d, %r8
	movq	(%rdi,%rsi,8), %rax
	movslq	%r9d, %r9
	movq	(%rax,%rdx,8), %rax
	movslq	16(%rsp), %rdx
	movq	(%rax,%rcx,8), %rax
	movslq	8(%rsp), %rcx
	movq	(%rax,%r8,8), %rax
	movq	(%rax,%r9,8), %rax
	movq	(%rax,%rcx,8), %rax
	movslq	24(%rsp), %rcx
	movq	(%rax,%rdx,8), %rax
	movslq	32(%rsp), %rdx
	movq	(%rax,%rcx,8), %rax
	movl	(%rax,%rdx,4), %eax
	ret
	.size	dyn_d9, .-dyn_d9
	.section	.text.unlikely
.LCOLDB8:
	.text
.LHOTB8:
	.p2align 4
	.globl	checks_d9
	.type	checks_d9, @function
checks_d9:
	endbr64
	testq	%rdi, %rdi
	je	.L139
	movslq	%esi, %rsi
	movq	(%rdi,%rsi,8), %rax
	testq	%rax, %rax
	je	.L139
	movslq	%edx, %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L139
	movslq	%ecx, %rcx
	movq	(%rax,%rcx,8), %rax
	testq	%rax, %rax
	je	.L139
	movslq	%r8d, %r8
	movq	(%rax,%r8,8), %rax
	testq	%rax, %rax
	je	.L139
	movslq	%r9d, %r9
	movq	(%rax,%r9,8), %rax
	testq	%rax, %rax
	je	.L139
	movslq	8(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L139
	movslq	16(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L139
	movslq	24(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L139
	movslq	32(%rsp), %rdx
	movl	(%rax,%rdx,4), %eax
	ret
	.section	.text.unlikely
	.type	checks_d9.cold, @function
checks_d9.cold:
.L139:
	ud2
	.text
	.size	checks_d9, .-checks_d9
	.section	.text.unlikely
	.size	checks_d9.cold, .-checks_d9.cold
.LCOLDE8:
	.text
.LHOTE8:
	.p2align 4
	.globl	plain_d10
	.type	plain_d10, @function
plain_d10:
	endbr64
	movq	(%rdi), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movl	(%rax), %eax
	ret
	.size	plain_d10, .-plain_d10
	.p2align 4
	.globl	const_d10
	.type	const_d10, @function
const_d10:
	endbr64
	movq	16(%rdi), %rax
	movq	40(%rax), %rax
	movq	136(%rax), %rax
	movq	24(%rax), %rax
	movq	56(%rax), %rax
	movq	88(%rax), %rax
	movq	104(%rax), %rax
	movq	152(%rax), %rax
	movq	16(%rax), %rax
	movl	20(%rax), %eax
	ret
	.size	const_d10, .-const_d10
	.p2align 4
	.globl	dyn_d10
	.type	dyn_d10, @function
dyn_d10:
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
	movslq	32(%rsp), %rcx
	movq	(%rax,%rdx,8), %rax
	movslq	40(%rsp), %rdx
	movq	(%rax,%rcx,8), %rax
	movl	(%rax,%rdx,4), %eax
	ret
	.size	dyn_d10, .-dyn_d10
	.section	.text.unlikely
.LCOLDB9:
	.text
.LHOTB9:
	.p2align 4
	.globl	checks_d10
	.type	checks_d10, @function
checks_d10:
	endbr64
	testq	%rdi, %rdi
	je	.L169
	movslq	%esi, %rsi
	movq	(%rdi,%rsi,8), %rax
	testq	%rax, %rax
	je	.L169
	movslq	%edx, %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L169
	movslq	%ecx, %rcx
	movq	(%rax,%rcx,8), %rax
	testq	%rax, %rax
	je	.L169
	movslq	%r8d, %r8
	movq	(%rax,%r8,8), %rax
	testq	%rax, %rax
	je	.L169
	movslq	%r9d, %r9
	movq	(%rax,%r9,8), %rax
	testq	%rax, %rax
	je	.L169
	movslq	8(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L169
	movslq	16(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L169
	movslq	24(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L169
	movslq	32(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L169
	movslq	40(%rsp), %rdx
	movl	(%rax,%rdx,4), %eax
	ret
	.section	.text.unlikely
	.type	checks_d10.cold, @function
checks_d10.cold:
.L169:
	ud2
	.text
	.size	checks_d10, .-checks_d10
	.section	.text.unlikely
	.size	checks_d10.cold, .-checks_d10.cold
.LCOLDE9:
	.text
.LHOTE9:
	.p2align 4
	.globl	plain_d11
	.type	plain_d11, @function
plain_d11:
	endbr64
	movq	(%rdi), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movl	(%rax), %eax
	ret
	.size	plain_d11, .-plain_d11
	.p2align 4
	.globl	const_d11
	.type	const_d11, @function
const_d11:
	endbr64
	movq	16(%rdi), %rax
	movq	40(%rax), %rax
	movq	136(%rax), %rax
	movq	24(%rax), %rax
	movq	56(%rax), %rax
	movq	88(%rax), %rax
	movq	104(%rax), %rax
	movq	152(%rax), %rax
	movq	16(%rax), %rax
	movq	40(%rax), %rax
	movl	68(%rax), %eax
	ret
	.size	const_d11, .-const_d11
	.p2align 4
	.globl	dyn_d11
	.type	dyn_d11, @function
dyn_d11:
	endbr64
	movslq	%esi, %rsi
	movslq	%edx, %rdx
	movslq	%ecx, %rcx
	movslq	%r8d, %r8
	movq	(%rdi,%rsi,8), %rax
	movslq	%r9d, %r9
	movq	(%rax,%rdx,8), %rax
	movslq	16(%rsp), %rdx
	movq	(%rax,%rcx,8), %rax
	movslq	8(%rsp), %rcx
	movq	(%rax,%r8,8), %rax
	movq	(%rax,%r9,8), %rax
	movq	(%rax,%rcx,8), %rax
	movslq	24(%rsp), %rcx
	movq	(%rax,%rdx,8), %rax
	movslq	32(%rsp), %rdx
	movq	(%rax,%rcx,8), %rax
	movslq	40(%rsp), %rcx
	movq	(%rax,%rdx,8), %rax
	movslq	48(%rsp), %rdx
	movq	(%rax,%rcx,8), %rax
	movl	(%rax,%rdx,4), %eax
	ret
	.size	dyn_d11, .-dyn_d11
	.section	.text.unlikely
.LCOLDB10:
	.text
.LHOTB10:
	.p2align 4
	.globl	checks_d11
	.type	checks_d11, @function
checks_d11:
	endbr64
	testq	%rdi, %rdi
	je	.L202
	movslq	%esi, %rsi
	movq	(%rdi,%rsi,8), %rax
	testq	%rax, %rax
	je	.L202
	movslq	%edx, %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L202
	movslq	%ecx, %rcx
	movq	(%rax,%rcx,8), %rax
	testq	%rax, %rax
	je	.L202
	movslq	%r8d, %r8
	movq	(%rax,%r8,8), %rax
	testq	%rax, %rax
	je	.L202
	movslq	%r9d, %r9
	movq	(%rax,%r9,8), %rax
	testq	%rax, %rax
	je	.L202
	movslq	8(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L202
	movslq	16(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L202
	movslq	24(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L202
	movslq	32(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L202
	movslq	40(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L202
	movslq	48(%rsp), %rdx
	movl	(%rax,%rdx,4), %eax
	ret
	.section	.text.unlikely
	.type	checks_d11.cold, @function
checks_d11.cold:
.L202:
	ud2
	.text
	.size	checks_d11, .-checks_d11
	.section	.text.unlikely
	.size	checks_d11.cold, .-checks_d11.cold
.LCOLDE10:
	.text
.LHOTE10:
	.p2align 4
	.globl	plain_d12
	.type	plain_d12, @function
plain_d12:
	endbr64
	movq	(%rdi), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movl	(%rax), %eax
	ret
	.size	plain_d12, .-plain_d12
	.p2align 4
	.globl	const_d12
	.type	const_d12, @function
const_d12:
	endbr64
	movq	16(%rdi), %rax
	movq	40(%rax), %rax
	movq	136(%rax), %rax
	movq	24(%rax), %rax
	movq	56(%rax), %rax
	movq	88(%rax), %rax
	movq	104(%rax), %rax
	movq	152(%rax), %rax
	movq	16(%rax), %rax
	movq	40(%rax), %rax
	movq	136(%rax), %rax
	movl	12(%rax), %eax
	ret
	.size	const_d12, .-const_d12
	.p2align 4
	.globl	dyn_d12
	.type	dyn_d12, @function
dyn_d12:
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
	movslq	32(%rsp), %rcx
	movq	(%rax,%rdx,8), %rax
	movslq	40(%rsp), %rdx
	movq	(%rax,%rcx,8), %rax
	movslq	48(%rsp), %rcx
	movq	(%rax,%rdx,8), %rax
	movslq	56(%rsp), %rdx
	movq	(%rax,%rcx,8), %rax
	movl	(%rax,%rdx,4), %eax
	ret
	.size	dyn_d12, .-dyn_d12
	.section	.text.unlikely
.LCOLDB11:
	.text
.LHOTB11:
	.p2align 4
	.globl	checks_d12
	.type	checks_d12, @function
checks_d12:
	endbr64
	testq	%rdi, %rdi
	je	.L238
	movslq	%esi, %rsi
	movq	(%rdi,%rsi,8), %rax
	testq	%rax, %rax
	je	.L238
	movslq	%edx, %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L238
	movslq	%ecx, %rcx
	movq	(%rax,%rcx,8), %rax
	testq	%rax, %rax
	je	.L238
	movslq	%r8d, %r8
	movq	(%rax,%r8,8), %rax
	testq	%rax, %rax
	je	.L238
	movslq	%r9d, %r9
	movq	(%rax,%r9,8), %rax
	testq	%rax, %rax
	je	.L238
	movslq	8(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L238
	movslq	16(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L238
	movslq	24(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L238
	movslq	32(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L238
	movslq	40(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L238
	movslq	48(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L238
	movslq	56(%rsp), %rdx
	movl	(%rax,%rdx,4), %eax
	ret
	.section	.text.unlikely
	.type	checks_d12.cold, @function
checks_d12.cold:
.L238:
	ud2
	.text
	.size	checks_d12, .-checks_d12
	.section	.text.unlikely
	.size	checks_d12.cold, .-checks_d12.cold
.LCOLDE11:
	.text
.LHOTE11:
	.p2align 4
	.globl	plain_d13
	.type	plain_d13, @function
plain_d13:
	endbr64
	movq	(%rdi), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movl	(%rax), %eax
	ret
	.size	plain_d13, .-plain_d13
	.p2align 4
	.globl	const_d13
	.type	const_d13, @function
const_d13:
	endbr64
	movq	16(%rdi), %rax
	movq	40(%rax), %rax
	movq	136(%rax), %rax
	movq	24(%rax), %rax
	movq	56(%rax), %rax
	movq	88(%rax), %rax
	movq	104(%rax), %rax
	movq	152(%rax), %rax
	movq	16(%rax), %rax
	movq	40(%rax), %rax
	movq	136(%rax), %rax
	movq	24(%rax), %rax
	movl	28(%rax), %eax
	ret
	.size	const_d13, .-const_d13
	.p2align 4
	.globl	dyn_d13
	.type	dyn_d13, @function
dyn_d13:
	endbr64
	movslq	%esi, %rsi
	movslq	%edx, %rdx
	movslq	%ecx, %rcx
	movslq	%r8d, %r8
	movq	(%rdi,%rsi,8), %rax
	movslq	%r9d, %r9
	movq	(%rax,%rdx,8), %rax
	movslq	16(%rsp), %rdx
	movq	(%rax,%rcx,8), %rax
	movslq	8(%rsp), %rcx
	movq	(%rax,%r8,8), %rax
	movq	(%rax,%r9,8), %rax
	movq	(%rax,%rcx,8), %rax
	movslq	24(%rsp), %rcx
	movq	(%rax,%rdx,8), %rax
	movslq	32(%rsp), %rdx
	movq	(%rax,%rcx,8), %rax
	movslq	40(%rsp), %rcx
	movq	(%rax,%rdx,8), %rax
	movslq	48(%rsp), %rdx
	movq	(%rax,%rcx,8), %rax
	movslq	56(%rsp), %rcx
	movq	(%rax,%rdx,8), %rax
	movslq	64(%rsp), %rdx
	movq	(%rax,%rcx,8), %rax
	movl	(%rax,%rdx,4), %eax
	ret
	.size	dyn_d13, .-dyn_d13
	.section	.text.unlikely
.LCOLDB12:
	.text
.LHOTB12:
	.p2align 4
	.globl	checks_d13
	.type	checks_d13, @function
checks_d13:
	endbr64
	testq	%rdi, %rdi
	je	.L277
	movslq	%esi, %rsi
	movq	(%rdi,%rsi,8), %rax
	testq	%rax, %rax
	je	.L277
	movslq	%edx, %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L277
	movslq	%ecx, %rcx
	movq	(%rax,%rcx,8), %rax
	testq	%rax, %rax
	je	.L277
	movslq	%r8d, %r8
	movq	(%rax,%r8,8), %rax
	testq	%rax, %rax
	je	.L277
	movslq	%r9d, %r9
	movq	(%rax,%r9,8), %rax
	testq	%rax, %rax
	je	.L277
	movslq	8(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L277
	movslq	16(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L277
	movslq	24(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L277
	movslq	32(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L277
	movslq	40(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L277
	movslq	48(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L277
	movslq	56(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L277
	movslq	64(%rsp), %rdx
	movl	(%rax,%rdx,4), %eax
	ret
	.section	.text.unlikely
	.type	checks_d13.cold, @function
checks_d13.cold:
.L277:
	ud2
	.text
	.size	checks_d13, .-checks_d13
	.section	.text.unlikely
	.size	checks_d13.cold, .-checks_d13.cold
.LCOLDE12:
	.text
.LHOTE12:
	.p2align 4
	.globl	plain_d14
	.type	plain_d14, @function
plain_d14:
	endbr64
	movq	(%rdi), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movl	(%rax), %eax
	ret
	.size	plain_d14, .-plain_d14
	.p2align 4
	.globl	const_d14
	.type	const_d14, @function
const_d14:
	endbr64
	movq	16(%rdi), %rax
	movq	40(%rax), %rax
	movq	136(%rax), %rax
	movq	24(%rax), %rax
	movq	56(%rax), %rax
	movq	88(%rax), %rax
	movq	104(%rax), %rax
	movq	152(%rax), %rax
	movq	16(%rax), %rax
	movq	40(%rax), %rax
	movq	136(%rax), %rax
	movq	24(%rax), %rax
	movq	56(%rax), %rax
	movl	44(%rax), %eax
	ret
	.size	const_d14, .-const_d14
	.p2align 4
	.globl	dyn_d14
	.type	dyn_d14, @function
dyn_d14:
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
	movslq	32(%rsp), %rcx
	movq	(%rax,%rdx,8), %rax
	movslq	40(%rsp), %rdx
	movq	(%rax,%rcx,8), %rax
	movslq	48(%rsp), %rcx
	movq	(%rax,%rdx,8), %rax
	movslq	56(%rsp), %rdx
	movq	(%rax,%rcx,8), %rax
	movslq	64(%rsp), %rcx
	movq	(%rax,%rdx,8), %rax
	movslq	72(%rsp), %rdx
	movq	(%rax,%rcx,8), %rax
	movl	(%rax,%rdx,4), %eax
	ret
	.size	dyn_d14, .-dyn_d14
	.section	.text.unlikely
.LCOLDB13:
	.text
.LHOTB13:
	.p2align 4
	.globl	checks_d14
	.type	checks_d14, @function
checks_d14:
	endbr64
	testq	%rdi, %rdi
	je	.L319
	movslq	%esi, %rsi
	movq	(%rdi,%rsi,8), %rax
	testq	%rax, %rax
	je	.L319
	movslq	%edx, %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L319
	movslq	%ecx, %rcx
	movq	(%rax,%rcx,8), %rax
	testq	%rax, %rax
	je	.L319
	movslq	%r8d, %r8
	movq	(%rax,%r8,8), %rax
	testq	%rax, %rax
	je	.L319
	movslq	%r9d, %r9
	movq	(%rax,%r9,8), %rax
	testq	%rax, %rax
	je	.L319
	movslq	8(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L319
	movslq	16(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L319
	movslq	24(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L319
	movslq	32(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L319
	movslq	40(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L319
	movslq	48(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L319
	movslq	56(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L319
	movslq	64(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L319
	movslq	72(%rsp), %rdx
	movl	(%rax,%rdx,4), %eax
	ret
	.section	.text.unlikely
	.type	checks_d14.cold, @function
checks_d14.cold:
.L319:
	ud2
	.text
	.size	checks_d14, .-checks_d14
	.section	.text.unlikely
	.size	checks_d14.cold, .-checks_d14.cold
.LCOLDE13:
	.text
.LHOTE13:
	.p2align 4
	.globl	plain_d15
	.type	plain_d15, @function
plain_d15:
	endbr64
	movq	(%rdi), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movl	(%rax), %eax
	ret
	.size	plain_d15, .-plain_d15
	.p2align 4
	.globl	const_d15
	.type	const_d15, @function
const_d15:
	endbr64
	movq	16(%rdi), %rax
	movq	40(%rax), %rax
	movq	136(%rax), %rax
	movq	24(%rax), %rax
	movq	56(%rax), %rax
	movq	88(%rax), %rax
	movq	104(%rax), %rax
	movq	152(%rax), %rax
	movq	16(%rax), %rax
	movq	40(%rax), %rax
	movq	136(%rax), %rax
	movq	24(%rax), %rax
	movq	56(%rax), %rax
	movq	88(%rax), %rax
	movl	52(%rax), %eax
	ret
	.size	const_d15, .-const_d15
	.p2align 4
	.globl	dyn_d15
	.type	dyn_d15, @function
dyn_d15:
	endbr64
	movslq	%esi, %rsi
	movslq	%edx, %rdx
	movslq	%ecx, %rcx
	movslq	%r8d, %r8
	movq	(%rdi,%rsi,8), %rax
	movslq	%r9d, %r9
	movq	(%rax,%rdx,8), %rax
	movslq	16(%rsp), %rdx
	movq	(%rax,%rcx,8), %rax
	movslq	8(%rsp), %rcx
	movq	(%rax,%r8,8), %rax
	movq	(%rax,%r9,8), %rax
	movq	(%rax,%rcx,8), %rax
	movslq	24(%rsp), %rcx
	movq	(%rax,%rdx,8), %rax
	movslq	32(%rsp), %rdx
	movq	(%rax,%rcx,8), %rax
	movslq	40(%rsp), %rcx
	movq	(%rax,%rdx,8), %rax
	movslq	48(%rsp), %rdx
	movq	(%rax,%rcx,8), %rax
	movslq	56(%rsp), %rcx
	movq	(%rax,%rdx,8), %rax
	movslq	64(%rsp), %rdx
	movq	(%rax,%rcx,8), %rax
	movslq	72(%rsp), %rcx
	movq	(%rax,%rdx,8), %rax
	movslq	80(%rsp), %rdx
	movq	(%rax,%rcx,8), %rax
	movl	(%rax,%rdx,4), %eax
	ret
	.size	dyn_d15, .-dyn_d15
	.section	.text.unlikely
.LCOLDB14:
	.text
.LHOTB14:
	.p2align 4
	.globl	checks_d15
	.type	checks_d15, @function
checks_d15:
	endbr64
	testq	%rdi, %rdi
	je	.L364
	movslq	%esi, %rsi
	movq	(%rdi,%rsi,8), %rax
	testq	%rax, %rax
	je	.L364
	movslq	%edx, %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L364
	movslq	%ecx, %rcx
	movq	(%rax,%rcx,8), %rax
	testq	%rax, %rax
	je	.L364
	movslq	%r8d, %r8
	movq	(%rax,%r8,8), %rax
	testq	%rax, %rax
	je	.L364
	movslq	%r9d, %r9
	movq	(%rax,%r9,8), %rax
	testq	%rax, %rax
	je	.L364
	movslq	8(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L364
	movslq	16(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L364
	movslq	24(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L364
	movslq	32(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L364
	movslq	40(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L364
	movslq	48(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L364
	movslq	56(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L364
	movslq	64(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L364
	movslq	72(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L364
	movslq	80(%rsp), %rdx
	movl	(%rax,%rdx,4), %eax
	ret
	.section	.text.unlikely
	.type	checks_d15.cold, @function
checks_d15.cold:
.L364:
	ud2
	.text
	.size	checks_d15, .-checks_d15
	.section	.text.unlikely
	.size	checks_d15.cold, .-checks_d15.cold
.LCOLDE14:
	.text
.LHOTE14:
	.p2align 4
	.globl	plain_d16
	.type	plain_d16, @function
plain_d16:
	endbr64
	movq	(%rdi), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movl	(%rax), %eax
	ret
	.size	plain_d16, .-plain_d16
	.p2align 4
	.globl	const_d16
	.type	const_d16, @function
const_d16:
	endbr64
	movq	16(%rdi), %rax
	movq	40(%rax), %rax
	movq	136(%rax), %rax
	movq	24(%rax), %rax
	movq	56(%rax), %rax
	movq	88(%rax), %rax
	movq	104(%rax), %rax
	movq	152(%rax), %rax
	movq	16(%rax), %rax
	movq	40(%rax), %rax
	movq	136(%rax), %rax
	movq	24(%rax), %rax
	movq	56(%rax), %rax
	movq	88(%rax), %rax
	movq	104(%rax), %rax
	movl	76(%rax), %eax
	ret
	.size	const_d16, .-const_d16
	.p2align 4
	.globl	dyn_d16
	.type	dyn_d16, @function
dyn_d16:
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
	movslq	32(%rsp), %rcx
	movq	(%rax,%rdx,8), %rax
	movslq	40(%rsp), %rdx
	movq	(%rax,%rcx,8), %rax
	movslq	48(%rsp), %rcx
	movq	(%rax,%rdx,8), %rax
	movslq	56(%rsp), %rdx
	movq	(%rax,%rcx,8), %rax
	movslq	64(%rsp), %rcx
	movq	(%rax,%rdx,8), %rax
	movslq	72(%rsp), %rdx
	movq	(%rax,%rcx,8), %rax
	movslq	80(%rsp), %rcx
	movq	(%rax,%rdx,8), %rax
	movslq	88(%rsp), %rdx
	movq	(%rax,%rcx,8), %rax
	movl	(%rax,%rdx,4), %eax
	ret
	.size	dyn_d16, .-dyn_d16
	.section	.text.unlikely
.LCOLDB15:
	.text
.LHOTB15:
	.p2align 4
	.globl	checks_d16
	.type	checks_d16, @function
checks_d16:
	endbr64
	testq	%rdi, %rdi
	je	.L412
	movslq	%esi, %rsi
	movq	(%rdi,%rsi,8), %rax
	testq	%rax, %rax
	je	.L412
	movslq	%edx, %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L412
	movslq	%ecx, %rcx
	movq	(%rax,%rcx,8), %rax
	testq	%rax, %rax
	je	.L412
	movslq	%r8d, %r8
	movq	(%rax,%r8,8), %rax
	testq	%rax, %rax
	je	.L412
	movslq	%r9d, %r9
	movq	(%rax,%r9,8), %rax
	testq	%rax, %rax
	je	.L412
	movslq	8(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L412
	movslq	16(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L412
	movslq	24(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L412
	movslq	32(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L412
	movslq	40(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L412
	movslq	48(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L412
	movslq	56(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L412
	movslq	64(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L412
	movslq	72(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L412
	movslq	80(%rsp), %rdx
	movq	(%rax,%rdx,8), %rax
	testq	%rax, %rax
	je	.L412
	movslq	88(%rsp), %rdx
	movl	(%rax,%rdx,4), %eax
	ret
	.section	.text.unlikely
	.type	checks_d16.cold, @function
checks_d16.cold:
.L412:
	ud2
	.text
	.size	checks_d16, .-checks_d16
	.section	.text.unlikely
	.size	checks_d16.cold, .-checks_d16.cold
.LCOLDE15:
	.text
.LHOTE15:
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
