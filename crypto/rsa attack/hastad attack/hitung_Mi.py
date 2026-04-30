def main():
    print("--- Script Pembagian N terhadap n1, n2, n3 ---")
    
    try:
        # 1. Input nilai N besar
        # Menggunakan int() agar mendukung angka yang sangat panjang
        N = int(input("Masukkan nilai N: "))
        
        # 2. Input nilai pembagi (n1, n2, n3)
        n1 = int(input("Masukkan nilai n1: "))
        n2 = int(input("Masukkan nilai n2: "))
        n3 = int(input("Masukkan nilai n3: "))
        
        print("\n--- Proses Pembagian ---")
        
        # 3. Melakukan pembagian dan mendefinisikan m1, m2, m3
        # Menggunakan // untuk integer division (hasil bulat tanpa .0)
        # Menggunakan % untuk melihat apakah ada sisa bagi (opsional)
        
        m1 = N // n1
        m2 = N // n2
        m3 = N // n3
        
        # 4. Menampilkan hasil
        # Kamu tidak perlu khawatir soal scientific notation di sini
        print(f"m1 (N / n1) = {m1}")
        print(f"m2 (N / n2) = {m2}")
        print(f"m3 (N / n3) = {m3}")
        
        print("\n--- Cek Sisa Bagi (Opsional) ---")
        print(f"Sisa N/n1: {N % n1}")
        print(f"Sisa N/n2: {N % n2}")
        print(f"Sisa N/n3: {N % n3}")

    except ZeroDivisionError:
        print("Error: Angka pembagi (n) tidak boleh nol!")
    except ValueError:
        print("Error: Masukkan angka bulat yang valid.")

if __name__ == "__main__":
    main()
