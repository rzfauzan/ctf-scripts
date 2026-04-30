import math

a = 12211
b = 14321
c = 16307
def cek_pairwise_coprime(a, b, c):
    # Menghitung GCD untuk tiap pasangan
    gcd_ab = math.gcd(a, b)
    gcd_ac = math.gcd(a, c)
    gcd_bc = math.gcd(b, c)

    print(f"Hasil Pengecekan untuk angka: {a}, {b}, {c}")
    print("-" * 30)
    
    # Menampilkan hasil tiap pasangan
    print(f"GCD({a}, {b}) = {gcd_ab} {'(OK!)' if gcd_ab == 1 else '(Bukan 1)'}")
    print(f"GCD({a}, {c}) = {gcd_ac} {'(OK!)' if gcd_ac == 1 else '(Bukan 1)'}")
    print(f"GCD({b}, {c}) = {gcd_bc} {'(OK!)' if gcd_bc == 1 else '(Bukan 1)'}")
    print("-" * 30)

    # Kesimpulan akhir
    if gcd_ab == 1 and gcd_ac == 1 and gcd_bc == 1:
        print("Kesimpulan: Ketiga pasangan adalah COPRIME (Semua GCD = 1).")
    else:
        print("Kesimpulan: Tidak semua pasangan adalah coprime.")

# Masukkan angka di sini
try:
    val_a = int(input("Masukkan angka a: "))
    val_b = int(input("Masukkan angka b: "))
    val_c = int(input("Masukkan angka c: "))
    
    cek_pairwise_coprime(val_a, val_b, val_c)
except ValueError:
    print("Error: Tolong masukkan angka bulat yang valid.")
