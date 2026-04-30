def extended_gcd(a, b):
    """Fungsi pembantu untuk Extended Euclidean Algorithm"""
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    """Mencari invers modular dari a mod m"""
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError(f"Invers modular tidak ada karena GCD({a}, {m}) = {gcd} (Bukan 1)")
    # Pastikan hasil invers selalu positif
    return (x % m + m) % m

def hitung_eksponen_negatif():
    print("--- Kalkulator C^r mod N (Eksponen Negatif) ---")
    try:
        # Input sesuai contoh di gambar
        C1 = int(input("Masukkan nilai basis (C1)  : "))
        r = int(input("Masukkan eksponen (r)      : "))
        N = int(input("Masukkan nilai modulo (N)  : "))

        print("-" * 45)
        
        if r >= 0:
            # Jika r ternyata positif, gunakan pangkat modular biasa (pow bawaan Python)
            hasil = pow(C1, r, N)
            print(f"Eksponen positif, hasil: {C1}^{r} mod {N} = {hasil}")
        else:
            # Langkah 1: Cari invers modular dari C1 mod N
            invers_C1 = mod_inverse(C1, N)
            print(f"1. Invers dari {C1} mod {N} (C1^-1) = {invers_C1}")
            
            # Langkah 2: Pangkatkan invers dengan nilai positif dari r
            r_absolut = abs(r)
            # pow(basis, eksponen, modulo) sangat efisien di Python
            hasil_akhir = pow(invers_C1, r_absolut, N) 
            
            print(f"2. Hitung ({invers_C1})^{r_absolut} mod {N} = {hasil_akhir}")
            
            print("-" * 45)
            print(f"Kesimpulan: {C1}^({r}) mod {N} = {hasil_akhir}")

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    hitung_eksponen_negatif()