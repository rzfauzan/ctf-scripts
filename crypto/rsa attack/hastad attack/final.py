import math

def iroot(n, k):
    if n == 0: return 0
    x = 1 << ((n.bit_length() + k - 1) // k)  
    while True:
        x1 = ((k - 1) * x + n // pow(x, k - 1)) // k
        if x1 >= x: break
        x = x1
    while pow(x + 1, k) <= n: x += 1  
    while pow(x, k) > n: x -= 1
    return x

def int_to_flag(m):
    try:
        length = (m.bit_length() + 7) // 8
        return m.to_bytes(length, 'big').decode('utf-8')
    except (UnicodeDecodeError, OverflowError):
        return f"(gagal decode) hex: {hex(m)}"

def main():
    print("=== RSA Hastad Broadcast Attack + CRT ===")

    e  = int(input("Masukkan nilai e: "))
    ns = [int(input(f"Masukkan nilai n{i}: ")) for i in range(1, e + 1)]
    cs = [int(input(f"Masukkan nilai C{i}: ")) for i in range(1, e + 1)]

    pairs = [(ns[i], ns[j]) for i in range(e) for j in range(i+1, e)]
    if any(math.gcd(a, b) != 1 for a, b in pairs):
        return print("GAGAL: n tidak semuanya coprime.")

    N = math.prod(ns)
    print(f"N Total: {N}")

    Ms = [N // n for n in ns]
    try:
        ys = [pow(M, -1, n) for M, n in zip(Ms, ns)]
    except ValueError:
        return print("GAGAL: Invers modular tidak ditemukan.")

    X = sum(c * M * y for c, M, y in zip(cs, Ms, ys)) % N
    m = iroot(X, e)

    if pow(m, e) != X:
        return print(f"GAGAL: Akar ke-{e} tidak sempurna. X={X}")

    print(f"\nPlaintext (integer) : {m}")

    if pow(m, e, ns[0]) == cs[0]:
        print("Verifikasi RSA     : BERHASIL")
    else:
        print("Verifikasi RSA     : GAGAL")

    flag = int_to_flag(m)
    print(f"Flag               : {flag}")

if __name__ == "__main__":
    main()