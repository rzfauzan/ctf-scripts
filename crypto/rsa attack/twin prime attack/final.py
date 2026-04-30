import math

def int_to_flag(m):
    raw = m.to_bytes((m.bit_length() + 7) // 8, 'big')
    for enc in ('utf-8', 'latin-1'):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return f"(hex) {raw.hex()}"

def fermat_factor(n, max_iter=10**7):
    # Edge case: n genap
    if n % 2 == 0:
        return 2, n // 2

    a = math.isqrt(n)
    if a * a < n:
        a += 1

    # Edge case: perfect square (p == q)
    if a * a == n:
        return a, a

    for i in range(max_iter):
        b2 = a * a - n
        b  = math.isqrt(b2)
        if b * b == b2:
            p, q = a + b, a - b
            assert p * q == n, "Hasil faktorisasi tidak valid!"
            return p, q
        a += 1
        if i % 100_000 == 0 and i > 0:
            print(f"\r[.] Iterasi: {i:,}", end='', flush=True)

    raise ValueError("Fermat gagal — p dan q kemungkinan tidak berdekatan.")

def solve():
    print("=== RSA Fermat Factorization Attack ===")

    try:
        n = int(input("N = "))
        e = int(input("e = "))
        c = int(input("C = "))
    except ValueError:
        return print("[-] Input harus angka bulat!")

    # 1. Faktorisasi
    print("\n[1] Factoring N...")
    try:
        p, q = fermat_factor(n)
    except ValueError as err:
        return print(f"\n[-] {err}")

    print(f"\n[+] p     = {p}")
    print(f"[+] q     = {q}")
    print(f"[+] |p-q| = {abs(p - q)}")

    # 2. Private key
    phi = (p - 1) * (q - 1)
    try:
        d = pow(e, -1, phi)
    except ValueError:
        return print("[-] e tidak invertible terhadap phi(N)!")

    # 3. Decrypt
    m = pow(c, d, n)
    print(f"\n[+] Raw Integer (M): {m}")

    # 4. Konversi ke flag
    flag = int_to_flag(m)
    print(f"\n[+] FLAG : {flag}")

if __name__ == "__main__":
    solve()