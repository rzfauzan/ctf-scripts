import galois

GCM_POLY = 0x100000000000000000000000000000087
GF128 = galois.GF(2**128, irreducible_poly=GCM_POLY)

def clean(h):
    return bytes.fromhex(h.replace(" ", ""))

def to_gf(h):
    return GF128(int.from_bytes(clean(h).ljust(16, b'\x00'), 'big'))

def gf_hex(x):
    return hex(int(x))[2:].upper().zfill(32)


print("=== AES-GCM S Calculator ===")

H = to_gf(input("H: "))
T = to_gf(input("T: "))
C = to_gf(input("C: "))

L = to_gf((len(clean(input("C: "))) * 8).to_bytes(16, 'big').hex())
ghash = (C * (H**2)) + (L * H)

S = T + ghash

print("\nS =", gf_hex(S))