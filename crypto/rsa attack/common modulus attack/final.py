import math

def solve_common_modulus():
    print("=== RSA Common Modulus Attack ===")

    n  = int(input("[+] N  : "))
    e1 = int(input("[+] e1 : "))
    e2 = int(input("[+] e2 : "))
    c1 = int(input("[+] C1 : "))
    c2 = int(input("[+] C2 : "))

    # 1. Validasi GCD(e1, e2) == 1
    if math.gcd(e1, e2) != 1:
        return print("[-] GCD(e1, e2) != 1. Serangan tidak bisa dilanjutkan.")

    # 2. Koefisien Bezout: r*e1 + s*e2 = 1
    def extended_gcd(a, b):
        old_r, r = a, b
        old_s, s = 1, 0
        while r:
            q = old_r // r
            old_r, r = r, old_r - q * r
            old_s, s = s, old_s - q * s
        return old_r, old_s, (old_r - old_s * a) // b

    _, r, s = extended_gcd(e1, e2)
    print(f"[*] r={r}, s={s}")

    # 3. M = C1^r * C2^s mod N
    try:
        m = (pow(c1, r, n) * pow(c2, s, n)) % n

    except ValueError:
        # gcd(C2, N) != 1 → C2 berbagi faktor dengan N, bocorkan p dan q!
        factor = math.gcd(c2, n)
        if factor > 1:
            p, q = factor, n // factor
            print(f"[!] N berhasil difaktorkan!")
            print(f"[!] p = {p}")
            print(f"[!] q = {q}")
            phi = (p - 1) * (q - 1)
            d = pow(e1, -1, phi)
            m = pow(c1, d, n)
            print(f"[*] Decrypt via faktorisasi, M = {m}")
        else:
            return print("[-] pow() gagal dan faktor tidak ditemukan.")

    print(f"[*] M = {m}")

    # 4. Konversi ke flag
    try:
        flag = m.to_bytes((m.bit_length() + 7) // 8, 'big').decode('utf-8')
        print(f"\n[+] FLAG : {flag}")
    except (UnicodeDecodeError, OverflowError):
        print(f"[-] Gagal decode. Hex: {hex(m)}")

if __name__ == "__main__":
    solve_common_modulus()