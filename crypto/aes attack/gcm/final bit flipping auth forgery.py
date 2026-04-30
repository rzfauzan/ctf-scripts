import galois

# ================= CONFIG =================
OUTPUT_FLAG = False   # True kalau mau format flag
# =========================================

GCM_POLY = 0x100000000000000000000000000000087
GF128 = galois.GF(2**128, irreducible_poly=GCM_POLY)

# ================= HELPER =================
def clean(h):
    return bytes.fromhex(h.replace(" ", ""))

def to_gf(h):
    return GF128(int.from_bytes(clean(h).ljust(16, b'\x00'), 'big'))

def gf_hex(x):
    return hex(int(x))[2:].upper().zfill(32)
# =========================================


def main():
    print("--- GCM Bit-Flipping & Tag Forgery ---")

    try:
        # ========= INPUT =========
        H = to_gf(input("H: "))
        S = to_gf(input("S: "))

        c_old = clean(input("Ciphertext lama: "))
        p_old = input("Plaintext lama : ").encode()
        p_new = input("Plaintext baru : ").encode()

        if len(p_old) != len(p_new):
            print("[!] Warning: panjang beda")

        # ========= BIT FLIP =========
        c_new = bytearray(
            (c_old[i] ^ p_old[i] ^ p_new[i]) if i < len(c_old) and i < len(p_old) else 0
            for i in range(len(p_new))
        )

        # ========= TAG FORGERY =========
        Cg = to_gf(c_new.hex())
        Lg = to_gf((len(c_new) * 8).to_bytes(16, 'big').hex())

        tag = (Cg * (H**2)) + (Lg * H) + S

        # ========= OUTPUT =========
        print("\n" + "="*40)
        print("CIPHERTEXT :", c_new.hex().upper())
        print("TAG        :", gf_hex(tag))

        # ===== FLAG OPSIONAL =====
        if OUTPUT_FLAG:
            print("FLAG       : flag{" + gf_hex(tag) + "}")
        # =========================

        print("="*40)

    except Exception as e:
        print("[!] Error:", e)


if __name__ == "__main__":
    main()