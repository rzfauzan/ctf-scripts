import galois
import numpy as np

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
    print("--- AES-GCM ATTACK TOOL ---")

    try:
        # ========= TAHAP 1 =========
        print("\n[1] HITUNG H & S (Nonce Reuse)")

        t1 = input("T1: ")
        t2 = input("T2: ")
        c1 = input("C1: ")
        c2 = input("C2: ")

        T1, T2 = to_gf(t1), to_gf(t2)
        C1, C2 = to_gf(c1), to_gf(c2)

        # Recover H
        H = np.sqrt((T1 + T2) * np.reciprocal(C1 + C2))

        # Hitung S
        L = to_gf((8 * 8).to_bytes(16, 'big').hex())
        S = T1 + (C1 * (H**2)) + (L * H)

        print("[+] H =", gf_hex(H))
        print("[+] S =", gf_hex(S))

        # ========= TAHAP 2 =========
        print("\n[2] FORGE CIPHERTEXT + TAG")

        c_target_hex = input("Ciphertext target: ")
        p_old = input("Plaintext lama   : ").encode()
        p_new = input("Plaintext baru   : ").encode()

        c_target = clean(c_target_hex)

        # Bit-flip
        c_new = bytearray(
            c_target[i] ^ p_old[i] ^ p_new[i]
            for i in range(len(p_new))
        )

        # Hitung tag baru
        Cn = to_gf(c_new.hex())
        Ln = to_gf((len(c_new) * 8).to_bytes(16, 'big').hex())

        tag_new = (Cn * (H**2)) + (Ln * H) + S
        tag_hex = gf_hex(tag_new)

        print("\n" + "="*40)
        print("CIPHERTEXT :", c_new.hex().upper())
        print("TAG        :", tag_hex)

        # ===== FLAG OPSIONAL =====
        if OUTPUT_FLAG:
            print("FLAG       : flag{" + tag_hex + "}")
        # =========================

        print("="*40)

    except Exception as e:
        print("[!] Error:", e)


if __name__ == "__main__":
    main()