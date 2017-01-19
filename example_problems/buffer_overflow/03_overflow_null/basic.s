	.file	"basic.c"
	.text
	.globl	my_gets
	.type	my_gets, @function
my_gets:
.LFB2:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$32, %rsp
	movq	%rdi, -24(%rbp)
	call	getchar
	movl	%eax, -4(%rbp)
	jmp	.L2
.L4:
	movq	-24(%rbp), %rax
	leaq	1(%rax), %rdx
	movq	%rdx, -24(%rbp)
	movl	-4(%rbp), %edx
	movb	%dl, (%rax)
	call	getchar
	movl	%eax, -4(%rbp)
.L2:
	cmpl	$10, -4(%rbp)
	je	.L1
	cmpl	$-1, -4(%rbp)
	jne	.L4
.L1:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE2:
	.size	my_gets, .-my_gets
	.section	.rodata
.LC0:
	.string	"P0stIt!"
.LC1:
	.string	"r"
.LC2:
	.string	"flag.txt"
.LC3:
	.string	"Enter password to get flag: "
.LC4:
	.string	"Password Accepted\nFlag = %s\n"
.LC5:
	.string	"%s is not the password\n"
	.text
	.globl	main
	.type	main, @function
main:
.LFB3:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	pushq	%rbx
	subq	$104, %rsp
	.cfi_offset 3, -24
	movl	%edi, -100(%rbp)
	movq	%rsi, -112(%rbp)
	movq	%fs:40, %rax
	movq	%rax, -24(%rbp)
	xorl	%eax, %eax
	movq	$.LC0, -96(%rbp)
	leaq	-80(%rbp), %rax
	movl	$8, %edx
	movl	$0, %esi
	movq	%rax, %rdi
	call	memset
	leaq	-64(%rbp), %rax
	movl	$32, %edx
	movl	$0, %esi
	movq	%rax, %rdi
	call	memset
	movl	$.LC1, %esi
	movl	$.LC2, %edi
	call	fopen
	movq	%rax, -88(%rbp)
	movq	-88(%rbp), %rdx
	leaq	-64(%rbp), %rax
	movl	$32, %esi
	movq	%rax, %rdi
	call	fgets
	movq	-88(%rbp), %rax
	movq	%rax, %rdi
	call	fclose
	movl	$.LC3, %edi
	movl	$0, %eax
	call	printf
	movq	stdout(%rip), %rax
	movq	%rax, %rdi
	call	fflush
	leaq	-80(%rbp), %rax
	movq	%rax, %rdi
	call	my_gets
	movq	-96(%rbp), %rcx
	leaq	-80(%rbp), %rax
	movl	$8, %edx
	movq	%rcx, %rsi
	movq	%rax, %rdi
	call	memcmp
	testl	%eax, %eax
	jne	.L6
	leaq	-64(%rbp), %rax
	movq	%rax, %rsi
	movl	$.LC4, %edi
	movl	$0, %eax
	call	printf
	jmp	.L7
.L6:
	leaq	-80(%rbp), %rax
	movq	%rax, %rsi
	movl	$.LC5, %edi
	movl	$0, %eax
	call	printf
.L7:
	movl	$0, %eax
	movq	-24(%rbp), %rbx
	xorq	%fs:40, %rbx
	je	.L9
	call	__stack_chk_fail
.L9:
	addq	$104, %rsp
	popq	%rbx
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE3:
	.size	main, .-main
	.ident	"GCC: (Ubuntu 4.8.4-2ubuntu1~14.04.3) 4.8.4"
	.section	.note.GNU-stack,"",@progbits
