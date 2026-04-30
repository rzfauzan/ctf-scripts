def hitung_wrap():
    print("=== Kalkulator Integer Wrap-Around (Overflow/Underflow) ===")
    
    # 1. Pilih tipe data
    print("\nPilih tipe data (bit):")
    print("1. uint8_t  (8-bit: 0 - 255)")
    print("2. uint16_t (16-bit: 0 - 65,535)")
    print("3. uint32_t (32-bit: 0 - 4,294,967,295)")
    
    pilihan = input("Pilihan (1/2/3): ")
    if pilihan == '1': 
        mod = 2**8
        tipe = "uint8_t"
    elif pilihan == '2': 
        mod = 2**16
        tipe = "uint16_t"
    elif pilihan == '3': 
        mod = 2**32
        tipe = "uint32_t"
    else:
        print("Pilihan tidak valid.")
        return

    try:
        # 2. Input nilai
        awal = int(input(f"\nMasukkan nilai awal (A): "))
        target = int(input(f"Masukkan target hasil akhir (B): "))

        print(f"\n[Hasil Analisis untuk {tipe}]")
        print("-" * 45)

        # Hitung untuk Penjumlahan (Overflow)
        # (awal + x) % mod = target  =>  x = (target - awal) % mod
        x_add = (target - awal) % mod
        print(f"UNTUK OVERFLOW (Penjumlahan):")
        print(f"Agar {awal} + X = {target}")
        print(f">> Masukkan X = {x_add}")
        print(f"Cek: ({awal} + {x_add}) % {mod} = {(awal + x_add) % mod}")

        print("-" * 45)

        # Hitung untuk Pengurangan (Underflow)
        # (awal - x) % mod = target  =>  x = (awal - target) % mod
        x_sub = (awal - target) % mod
        print(f"UNTUK UNDERFLOW (Pengurangan):")
        print(f"Agar {awal} - X = {target}")
        print(f">> Masukkan X = {x_sub}")
        print(f"Cek: ({awal} - {x_sub}) % {mod} = {(awal - x_sub) % mod}")
        
    except ValueError:
        print("Input harus berupa angka!")

if __name__ == "__main__":
    hitung_wrap()
