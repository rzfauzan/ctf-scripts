from pwn import *

# Load file binary
elf = ELF('./vuln')

# Cek satu-per-satu proteksinya
print(f"PIE: {elf.pie}")
print(f"NX: {elf.nx}")
print(f"Canary: {elf.canary}")

# Atau liat ringkasan kayak di terminal
# (checksec=False di konfigurasi biar gak muncul dua kali)
context.binary = elf