import gmpy2
import binascii

def solve_low_exponent():
    print("=== RSA Low Exponent Root Solver ===")
    
    # Input Ciphertext (C)
    c_raw = input("Masukkan Ciphertext (C) [Desimal atau Hex 0x...]: ").strip()
    if c_raw.startswith('0x'):
        c = int(c_raw, 16)
    else:
        c = int(c_raw)

    # Input Exponent (e)
    e_raw = input("Masukkan Exponent (e) [Default 3]: ").strip()
    e = int(e_raw) if e_raw else 3

    print(f"\n[*] Menghitung akar pangkat {e}...")

    # Menghitung akar menggunakan gmpy2 untuk presisi integer besar
    m, exact = gmpy2.iroot(c, e)
    
    if exact:
        print("[+] Akar sempurna ditemukan!")
    else:
        print("[!] Peringatan: Hasil bukan akar sempurna (mungkin M^e > n atau ada padding).")

    # Konversi hasil ke String/Flag
    try:
        # Mengonversi integer m ke hex, lalu ke bytes
        m_hex = hex(m)[2:]
        if len(m_hex) % 2 != 0:
            m_hex = '0' + m_hex
        
        flag = binascii.unhexlify(m_hex).decode('utf-8', errors='ignore')
        
        print("-" * 30)
        print(f"Hasil Integer: {m}")
        print(f"Hasil String : {flag}")
        print("-" * 30)
    except Exception as err:
        print(f"[!] Gagal konversi ke string: {err}")
        print(f"Hasil Integer: {m}")

if __name__ == "__main__":
    try:
        solve_low_exponent()
    except KeyboardInterrupt:
        print("\n[!] Program dihentikan.")
    except ValueError:
        print("\n[!] Error: Pastikan input yang kamu masukkan adalah angka.")