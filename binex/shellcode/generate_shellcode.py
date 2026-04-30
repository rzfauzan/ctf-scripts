from pwn import *
context.arch = 'amd64' # atau 'i386'
print(enhex(asm(shellcraft.sh()))) # Otomatis generate shellcode