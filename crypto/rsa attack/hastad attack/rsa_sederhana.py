def modular_exponentiation():
    print("--- Kalkulator Modular Exponentiation (M^e mod N) ---")
    
    try:
        # Input dari user
        M = int(input("Masukkan nilai M (Pesan/Base): "))
        e = int(input("Masukkan nilai e (Eksponen): "))
        N = int(input("Masukkan nilai N (Modulus): "))

        # Menghitung M^e mod N
        # Fungsi pow(M, e, N) jauh lebih efisien daripada (M**e) % N
        hasil = pow(M, e, N)

        print("-" * 30)
        print(f"Hasil dari {M}^{e} mod {N} adalah:")
        print(f"Result: {hasil}")
        
    except ValueError:
        print("Error: Harap masukkan angka bulat (integer) yang valid.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    modular_exponentiation()