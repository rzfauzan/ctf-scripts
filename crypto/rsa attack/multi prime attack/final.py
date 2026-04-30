import math

def factorize(n):
    """Trial division dengan optimasi — cukup untuk N CTF ukuran wajar."""
    factors = {}
    # Cek faktor 2
    while n % 2 == 0:
        factors[2] = factors.get(2, 0) + 1
        n //= 2
    # Cek faktor ganjil
    d = 3
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 2
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors  # {prima: eksponen}

def compute_phi(factors):
    """Phi Euler yang benar untuk faktor berulang: p^(k-1) * (p-1)."""
    phi = 1
    for p, k in factors.items():
        phi *= (p ** (k - 1)) * (p - 1)
    return phi

def int_to_flag(m):
    raw = m.to_bytes((m.bit_length() + 7) // 8, 'big')
    for enc in ('utf-8', 'latin-1'):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return f"(hex) {raw.hex()}"

def solve():
    print("=== RSA Multi-Prime Attack ===")

    try:
        n = int(input("N = "))
        e = int(input("e = "))
        c = int(input("C = "))
    except ValueError:
        return print("[-] Input harus angka bulat!")

    # 1. Faktorisasi
    factors = factorize(n)
    print(f"\n[+] Faktor  : {dict(factors)}")

    # 2. Hitung phi
    phi = compute_phi(factors)
    print(f"[+] Phi(N)  : {phi}")

    # 3. Private key
    try:
        d = pow(e, -1, phi)
    except ValueError:
        return print("[-] e tidak invertible terhadap phi(N)!")
    print(f"[+] d       : {d}")

    # 4. Dekripsi
    m = pow(c, d, n)

    # 5. Verifikasi
    if pow(m, e, n) != c:
        return print("[-] Verifikasi gagal — hasil dekripsi tidak cocok.")

    # 6. Konversi ke flag
    flag = int_to_flag(m)
    print(f"\n[+] FLAG    : {flag}")

if __name__ == "__main__":
    solve()