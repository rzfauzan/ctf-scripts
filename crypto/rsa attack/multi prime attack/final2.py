import math
import random

def is_prime_mr(n):
    """Miller-Rabin primality test."""
    if n < 2: return False
    if n in (2, 3): return True
    if n % 2 == 0: return False
    r, d = 0, n - 1
    while d % 2 == 0: r += 1; d //= 2
    for a in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
        if a >= n: continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1: continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1: break
        else: return False
    return True

def pollard_rho(n):
    """Pollard's Rho — untuk prima yang terlalu besar untuk trial division."""
    if n % 2 == 0: return 2
    for _ in range(50):
        x = random.randint(2, n - 1)
        c = random.randint(1, n - 1)
        y, d = x, 1
        while d == 1:
            # Batch accumulation: GCD setiap 128 langkah (jauh lebih cepat)
            q, xs = 1, x
            for _ in range(128):
                x = (x * x + c) % n
                y = (y * y + c) % n
                y = (y * y + c) % n
                diff = abs(x - y)
                if diff == 0: break
                q = q * diff % n
            d = math.gcd(q, n)
            if d == n:  # fallback per-langkah jika batch gagal
                d, x = 1, xs
                while d == 1:
                    x = (x * x + c) % n
                    y = (y * y + c) % n
                    y = (y * y + c) % n
                    d = math.gcd(abs(x - y), n)
        if 1 < d < n:
            return d
    return None

def factorize(n):
    """
    Hybrid factorization:
    - Trial division untuk prima kecil (< 10^6) → cepat
    - Pollard's Rho untuk prima besar
    """
    if n <= 1: return {}
    if is_prime_mr(n): return {n: 1}

    factors = {}
    stack = [n]

    while stack:
        num = stack.pop()
        if num == 1: continue
        if is_prime_mr(num):
            factors[num] = factors.get(num, 0) + 1
            continue

        # Coba trial division dulu untuk faktor kecil (cepat)
        found = False
        for d in range(2, min(10**6, int(num**0.5) + 1)):
            if num % d == 0:
                stack += [d, num // d]
                found = True
                break
            if d > 2 and d % 2 == 0: continue

        if not found:
            # Prima besar → Pollard's Rho
            d = pollard_rho(num)
            if d:
                stack += [d, num // d]
            else:
                # Tidak berhasil difaktorkan
                factors[num] = factors.get(num, 0) + 1

    return factors

def compute_phi(factors):
    """Phi Euler yang benar: p^(k-1) * (p-1) per faktor unik."""
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
    print("\n[*] Factoring N...")
    factors = factorize(n)
    if not factors:
        return print("[-] Faktorisasi gagal.")
    print(f"[+] Faktor  : {dict(factors)}")

    # 2. Phi
    phi = compute_phi(factors)
    print(f"[+] Phi(N)  : {phi}")

    # 3. Private key
    try:
        d = pow(e, -1, phi)
    except ValueError:
        return print("[-] e tidak invertible terhadap phi(N)!")

    # 4. Dekripsi + verifikasi
    m = pow(c, d, n)
    if pow(m, e, n) != c:
        return print("[-] Verifikasi gagal!")

    # 5. Konversi ke flag
    flag = int_to_flag(m)
    print(f"\n[+] FLAG    : {flag}")

if __name__ == "__main__":
    solve()