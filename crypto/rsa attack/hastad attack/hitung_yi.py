def get_modular_inverse():
    print("--- Kalkulator Modular Multiplicative Inverse ---")
    print("Mencari y untuk persamaan: m^-1 mod n = y")
    
    results = []
    
    # Kita akan meminta input untuk 3 pasangan sesuai permintaanmu
    for i in range(1, 4):
        print(f"\nEntri data ke-{i}:")
        try:
            m = int(input(f"Masukkan nilai m{i}: "))
            n = int(input(f"Masukkan nilai n{i}: "))
            
            # Menghitung invers modular menggunakan pow(base, exp, mod)
            y = pow(m, -1, n)
            results.append(y)
            print(f">>> Hasil y{i} = {y}")
            
        except ValueError as e:
            # ValueError muncul jika m dan n tidak koprim atau input bukan angka
            if "not invertible" in str(e) or "base is not relatively prime" in str(e).lower():
                print(f"Error: Invers tidak ada karena FPB({m}, {n}) != 1")
            else:
                print("Error: Harap masukkan angka bulat yang valid.")
            results.append(None)
            
    return results

# Menjalankan fungsi
y_values = get_modular_inverse()

print("\n" + "="*30)
print("Ringkasan Hasil Akhir:", y_values)