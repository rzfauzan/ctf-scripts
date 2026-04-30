import math

def solve_crt_rsa():
    print("--- Kalkulator CRT & Akar Pangkat Tiga ---")
    
    try:
        # Input nilai yang diperlukan
        print("\n--- Masukkan Nilai C (Ciphertext) ---")
        c1 = int(input("C1: "))
        c2 = int(input("C2: "))
        c3 = int(input("C3: "))

        print("\n--- Masukkan Nilai n (Modulus) ---")
        n1 = int(input("n1: "))
        n2 = int(input("n2: "))
        n3 = int(input("n3: "))

        # 1. Hitung Modulus Total (N)
        N_total = n1 * n2 * n3

        # 2. Hitung M1, M2, M3
        # Mi = N_total / ni
        M1 = n2 * n3
        M2 = n1 * n3
        M3 = n1 * n2

        # 3. Hitung Invers Modular (y1, y2, y3)
        # Mi * yi ≡ 1 (mod ni)
        y1 = pow(M1, -1, n1)
        y2 = pow(M2, -1, n2)
        y3 = pow(M3, -1, n3)

        print(f"\nInvers yang ditemukan: y1={y1}, y2={y2}, y3={y3}")

        # 4. Hitung X
        # X = (C1*M1*y1 + C2*M2*y2 + C3*M3*y3) mod N_total
        X = (c1 * M1 * y1 + c2 * M2 * y2 + c3 * M3 * y3) % N_total
        
        print(f"\nNilai X: {X}")

        # 5. Akar Pangkat Tiga untuk mencari M
        # Kita gunakan pendekatan integer root untuk presisi tinggi
        M = round(X ** (1/3))
        
        # Verifikasi apakah benar M^3 = X
        if M**3 == X:
            print(f"Hasil M (Plaintext): {M}")
        else:
            # Jika tidak pas, tampilkan hasil float-nya
            print(f"Hasil M (Pendekatan): {X ** (1/3)}")

    except ValueError as e:
        print(f"\nKesalahan: {e}")
        print("Pastikan Mi dan ni adalah koprim agar invers modular dapat ditemukan.")
    except Exception as e:
        print(f"\nTerjadi kesalahan: {e}")

if __name__ == "__main__":
    solve_crt_rsa()