import galois
import numpy as np

# ================= CONFIG =================
OUTPUT_FLAG = False   # True kalau mau format flag
# =========================================

GCM_POLY = 0x100000000000000000000000000000087
GF128 = galois.GF(2**128, irreducible_poly=GCM_POLY)

# ================= HELPER =================
def clean(h):
    return bytes.fromhex(h.replace(" ", "").replace("0x", ""))

def to_gf(h):
    return GF128(int.from_bytes(clean(h).ljust(16, b'\x00'), 'big'))

def gf_hex(x):
    return hex(int(x))[2:].upper().zfill(32)
# =========================================


def main():
    print("--- GCM Forbidden Attack ---")

    try:
        # ========= INPUT =========
        T1 = to_gf(input("T1: "))
        T2 = to_gf(input("T2: "))
        C1 = to_gf(input("C1: "))
        C2 = to_gf(input("C2: "))

        # ========= CORE =========
        delta_T = T1 + T2
        delta_C = C1 + C2

        H_sq = delta_T * np.reciprocal(delta_C)
        H = np.sqrt(H_sq)

        h_hex = gf_hex(H)

        # ========= OUTPUT =========
        print("\n" + "="*30)
        print("H =", h_hex)

        # ===== FLAG OPSIONAL =====
        if OUTPUT_FLAG:
            try:
                s = bytes.fromhex(h_hex).decode('ascii').strip('\x00')
                print("FLAG :", s)
            except:
                print("FLAG : flag{" + h_hex + "}")
        # =========================

        print("="*30)

    except Exception as e:
        print("[!] Error:", e)


if __name__ == "__main__":
    main()