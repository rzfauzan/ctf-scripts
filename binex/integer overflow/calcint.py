def hitung_wrap_signed():
    print("=== Kalkulator Signed Integer Wrap-Around ===")
    
    # 1. Pilih tipe data signed
    print("\nPilih tipe data (Signed):")
    print("1. int8_t  (-128 s/d 127)")
    print("2. int16_t (-32,768 s/d 32,767)")
    print("3. int32_t (-2,147,483,648 s/d 2,147,483,647)")
    
    pilihan = input("Pilihan (1/2/3): ")
    if pilihan == '1':
        bits = 8
        tipe = "int8_t"
    elif pilihan == '2':
        bits = 16
        tipe = "int16_t"
    elif pilihan == '3':
        bits = 32
        tipe = "int32_t"
    else:
        return

    # Hitung range
    MOD = 2**bits
    MIN_VAL = -(2**(bits-1))
    MAX_VAL = (2**(bits-1)) - 1

    try:
        awal = int(input(f"Masukkan nilai awal ({tipe}): "))
        target = int(input(f"Masukkan target hasil ({tipe}): "))

        if not (MIN_VAL <= target <= MAX_VAL):
            print(f"[!] Error: Target harus di antara {MIN_VAL} dan {MAX_VAL}")
            return

        print(f"\n[Hasil Analisis {tipe}]")
        print(f"Range: {MIN_VAL} s/d {MAX_VAL}")
        print("-" * 45)

        # Rumus Signed Wrap:
        # Hasil = (awal + x - MIN_VAL) % MOD + MIN_VAL
        # Maka: x = (target - awal) % MOD
        
        # Penjumlahan
        x_add = (target - awal) % MOD
        print(f"UNTUK OVERFLOW (Penjumlahan):")
        print(f"Input X = {x_add}")
        
        # Pengurangan
        x_sub = (awal - target) % MOD
        print(f"\nUNTUK UNDERFLOW (Pengurangan):")
        print(f"Input X = {x_sub}")
        
        print("-" * 45)
        print(f"Logika: {awal} + {x_add} akan melewati {MAX_VAL} dan kembali ke {target}")

    except ValueError:
        print("Input harus angka!")

if __name__ == "__main__":
    hitung_wrap_signed()
