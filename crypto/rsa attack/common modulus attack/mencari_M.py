def extended_gcd(a, b):
    """Mencari algoritma euklides yang diperluas"""
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    """Mencari invers modular. Digunakan jika pangkat negatif."""
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError(f"Invers modular tidak ada karena GCD({a}, {m}) != 1")
    return (x % m + m) % m

def pangkat_modular(basis, eksponen, modulo):
    """Fungsi aman untuk menghitung (basis^eksponen) mod modulo"""
    if eksponen >= 0:
        return pow(basis, eksponen, modulo)
    else:
        # Jika eksponen negatif, cari invers basisnya dulu
        invers_basis = mod_inverse(basis, modulo)
        return pow(invers_basis, abs(eksponen), modulo)

def main():
    print("--- Langkah 5: Hitung Pesan M ---")
    try:
        # Mengambil input variabel
        C1 = int(input("Masukkan nilai C1 : "))
        r  = int(input("Masukkan nilai r  : "))
        C2 = int(input("Masukkan nilai C2 : "))
        s  = int(input("Masukkan nilai s  : "))
        N  = int(input("Masukkan nilai N  : "))

        print("-" * 45)
        
        # 1. Hitung bagian pertama: C1^r mod N
        bagian1 = pangkat_modular(C1, r, N)
        print(f"C1^r mod N = {C1}^{r} mod {N} = {bagian1}")

        # 2. Hitung bagian kedua: C2^s mod N
        bagian2 = pangkat_modular(C2, s, N)
        print(f"C2^s mod N = {C2}^{s} mod {N} = {bagian2}")

        # 3. Hitung M keseluruhan: (bagian1 * bagian2) mod N
        M_sementara = bagian1 * bagian2
        M_akhir = M_sementara % N
        
        print("-" * 45)
        print(f"M = (C1^r * C2^s) mod N")
        print(f"M = ({bagian1} * {bagian2}) mod {N}")
        print(f"M = {M_sementara} mod {N}")
        print(f"\nHasil Akhir: M = {M_akhir}")
        print("-" * 45)

    except ValueError as e:
        print(f"Error: {e}. Pastikan semua input adalah angka bulat.")

if __name__ == "__main__":
    main()