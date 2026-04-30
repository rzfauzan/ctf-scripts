import base64
import socket

# ================= CONFIG =================
OUTPUT_MODE = "base64"   # base64 / hex / raw
VERIFY = True            # True = verifikasi lokal
USE_NC = False           # True = kirim ke server
OUTPUT_FLAG = False      # True kalau mau format flag

HOST = "chall.ctf.com"
PORT = 1234
# =========================================


# ================= HELPER =================
def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def clean_hex(h):
    return bytes.fromhex(h.strip())

def encode_payload(p):
    if OUTPUT_MODE == "base64":
        return base64.b64encode(p)
    elif OUTPUT_MODE == "hex":
        return p.hex().encode()
    return p
# =========================================


def flip_cbc(c1, old, new, idxs):
    c = bytearray(c1)
    for i, idx in enumerate(idxs):
        c[idx] ^= ord(old[i]) ^ ord(new[i])
    return c


# ================= OPTIONAL NC =================
def send_nc(payload):
    s = socket.socket()
    s.connect((HOST, PORT))
    try:
        s.recv(4096)
        s.sendall(payload + b"\n")
        print(s.recv(4096).decode(errors="ignore"))
    finally:
        s.close()
# ==============================================


def main():
    print("=== CBC Bit-Flipping ===")

    try:
        # ========= INPUT =========
        iv = clean_hex(input("IV : "))
        c1 = clean_hex(input("C1 : "))
        c2 = clean_hex(input("C2 : "))

        idxs = list(map(int, input("Index : ").split(',')))
        old = input("Old : ")
        new = input("New : ")

        if len(old) != len(new):
            print("[!] panjang harus sama")
            return

        # ========= EXPLOIT =========
        c1_new = flip_cbc(c1, old, new, idxs)
        payload = iv + c1_new + c2
        encoded = encode_payload(payload)

        print("\n=== PAYLOAD ===")
        try:
            print(encoded.decode())
        except:
            print(encoded)

        # ===== FLAG OPSIONAL =====
        if OUTPUT_FLAG:
            try:
                print("FLAG :", encoded.decode())
            except:
                print("FLAG :", encoded)
        # =========================

        # ========= VERIFY =========
        if VERIFY:
            try:
                print("\n[*] Verifikasi...")
                p2 = b"role=user&xxx=0 "
                c1_orig = clean_hex(input("C1 original: "))

                dec = xor_bytes(p2, c1_orig)
                res = xor_bytes(dec, c1_new)

                print("Hasil:", res.decode(errors="replace"))

                if new in res.decode(errors="ignore"):
                    print("[+] SUCCESS")
                else:
                    print("[-] FAIL")
            except:
                print("Skip verify")

        # ========= NC =========
        if USE_NC:
            send_nc(encoded)

    except Exception as e:
        print("[!] Error:", e)


if __name__ == "__main__":
    main()