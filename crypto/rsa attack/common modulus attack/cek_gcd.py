import math

def cek_relatif_prima():
    print("--- Pengecekan GCD(e1, e2) ---")
    
    try:
        # Mengambil input dari user
        e1 = int(input("Masukkan nilai e1: "))
        e2 = int(input("Masukkan nilai e2: "))

        # Menghitung GCD menggunakan fungsi bawaan math
        hasil_gcd = math.gcd(e1, e2)

        print("-" * 30)
        if hasil_gcd == 1:
            print(f"Hasil: GCD({e1}, {e2}) = 1")
            print("Status: BERHASIL. Kedua bilangan relatif prima.")
        else:
            print(f"Hasil: GCD({e1}, {e2}) = {hasil_gcd}")
            print("Status: GAGAL. Kedua bilangan tidak relatif prima.")
        print("-" * 30)

    except ValueError:
        print("Error: Harap masukkan angka bulat saja!")

if __name__ == "__main__":
    cek_relatif_prima()s