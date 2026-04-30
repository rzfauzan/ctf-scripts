from pwn import xor

def crib_drag(c1_hex, c2_hex, crib):
    # 1. Hitung Z = C_A ^ C_B = P_A ^ P_B
    c1 = bytes.fromhex(c1_hex)
    c2 = bytes.fromhex(c2_hex)
    z = xor(c1, c2)
    
    print(f"{'Pos':<5} | {'Hasil XOR dengan Crib':<20} | {'Status'}")
    print("-" * 50)
    
    # 2. Geser crib di sepanjang Z
    for i in range(len(z) - len(crib) + 1):
        # XOR potongan Z dengan crib di posisi i
        res = xor(z[i:i+len(crib)], crib.encode())
        
        # Coba tampilkan hasilnya (decode as ascii)
        try:
            res_str = res.decode('ascii')
            # Jika hasilnya human-readable, tandai sebagai potensi
            status = "POTENSIAL" if all(32 <= ord(c) <= 126 for c in res_str) else ""
            print(f"{i:<5} | {res_str:<20} | {status}")
        except:
            print(f"{i:<5} | {'[Non-ASCII]':<20} |")

# --- CONTOH PENGGUNAAN ---
# Masukkan hex ciphertext blok 2 dari gambar sebelumnya
ca2 = "7AC3810B9F56D422E81463AE5B923F0D"
cb2 = "6DD4961E8C43C135FF0974BB4E872A18"

# Tebak kata umum (Crib)
tebakan = "the" 

crib_drag(ca2, cb2, tebakan)