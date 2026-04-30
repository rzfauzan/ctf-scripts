def extended_gcd(a, b):
    # Basis: jika a adalah 0, maka gcd adalah b
    # r = 0, s = 1 karena 0*(0) + 1*(b) = b
    if a == 0:
        return b, 0, 1
    
    # Rekursi untuk menjalankan algoritma euklides
    gcd, r1, s1 = extended_gcd(b % a, a)

    # Update r dan s menggunakan hasil dari rekursi
    r = s1 - (b // a) * r1
    s = r1

    return gcd, r, s

def main():
    print("--- Extended Euclidean Algorithm (Mencari r dan s) ---")
    try:
        e1 = int(input("Masukkan nilai e1: "))
        e2 = int(input("Masukkan nilai e2: "))

        gcd, r, s = extended_gcd(e1, e2)

        if gcd != 1:
            print(f"\nPerhatian: GCD({e1}, {e2}) = {gcd}. ")
            print("Nilai r dan s ditemukan, tapi hasilnya bukan 1 (tidak relatif prima).")
        
        print("-" * 45)
        print(f"Hasil Identitas Bézout:")
        print(f"r = {r}")
        print(f"s = {s}")
        print("-" * 45)
        
        # Verifikasi
        print(f"Verifikasi: ({r} * {e1}) + ({s} * {e2})")
        print(f"            {r * e1} + {s * e2} = {(r * e1) + (s * e2)}")

    except ValueError:
        print("Error: Input harus berupa angka bulat!")

if __name__ == "__main__":
    main()