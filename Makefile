all:
	python3 hasm.py Test/exit_code.hasm
	nasm -f elf32 Test/exit_code.asm -o Test/exit_code.o
	ld -m elf_i386 Test/exit_code.o -o Test/exit_code