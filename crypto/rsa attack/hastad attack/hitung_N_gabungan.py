import math

def main():
    print("--- Script Pengecekan Variabel e, N, dan m ---")
    
    try:
        # 1. Masukkan nilai variable e
        e = int(input("Masukkan nilai e: "))
        
        # 2. Masukkan 3 nilai n untuk dikalikan menjadi N
        n1 = int(input("Masukkan n1: "))
        n2 = int(input("Masukkan n2: "))
        n3 = int(input("Masukkan n3: "))
        
        # Menghitung N (n1 * n2 * n3)
        N_total = n1 * n2 * n3
        
        # 3. Cari n paling kecil diantara ketiganya
        n_terkecil = min(n1, n2, n3)
        
        # 4. Hasil pengurangan -1 dijadikan variabel baru (m)
        m = n_terkecil - 1
        
        print("\n--- Hasil Perhitungan ---")
        print(f"Nilai N (n1*n2*n3): {N_total}")
        print(f"n terkecil         : {n_terkecil}")
        print(f"Nilai m (n_min - 1): {m}")
        
        # 5. Cek apakah m^e < n_terkecil^e
        # Menggunakan fungsi pow(base, exp) agar lebih efisien untuk angka besar
        m_pangkat_e = pow(m, e)
        n_pangkat_e = pow(n_terkecil, e)
        
        print(f"\n--- Pengecekan m^e < n_min^e ---")
        if m_pangkat_e < n_pangkat_e:
            print(f"Hasil: BENAR (m^e lebih kecil dari n_min^e)")
        else:
            print(f"Hasil: SALAH (m^e tidak lebih kecil dari n_min^e)")
            
        # Opsional: Melihat selisihnya jika angka tidak terlalu raksasa
        # print(f"Selisih: {n_pangkat_e - m_pangkat_e}")

    except ValueError:
        print("Error: Harap masukkan angka bulat yang valid.")

if __name__ == "__main__":
    main()
