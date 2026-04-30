from pwn import *

# === KONFIGURASI ===
# Ganti HOST dan PORT sesuai info dari soal CTF
HOST = 'target-ctf.com'
PORT = 1337
# Ganti LOCAL_BIN kalau lu mau ngetes ke file lokal
LOCAL_BIN = './vuln' 

def start():
    if args.REMOTE:
        # Jalankan: python3 exploit.py REMOTE
        return remote(HOST, PORT)
    else:
        # Jalankan: python3 exploit.py
        return process(LOCAL_BIN)

io = start()

# ==========================================================
# === TEMPAT TARUH PAYLOAD LU ===
# ==========================================================

# Contoh Format String manual kayak di gambar lu:
# payload = p32(0x0804a018) + b"%10c%4$n" 

# Kirim payload
# io.sendline(payload)

# ==========================================================

# Biar dapet shell interaktif
io.interactive()