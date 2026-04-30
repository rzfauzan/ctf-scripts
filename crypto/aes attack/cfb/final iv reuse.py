import base64
import socket

# ================= CONFIG =================
OUTPUT_MODE = "hex"     # hex / base64 / raw
OUTPUT_FLAG = False     # True kalau butuh format FLAG{}
USE_NC = False          # True kalau kirim ke server

HOST = "chall.ctf.com"
PORT = 1234
# =========================================


# ================= HELPER =================
def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def clean_hex(h):
    return bytes.fromhex(h.replace(" ", ""))

def encode(data):
    if OUTPUT_MODE == "hex":
        return data.hex().upper().encode()
    elif OUTPUT_MODE == "base64":
        return base64.b64encode(data)
    return data
# =========================================


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
    print("=== AES-CFB IV Reuse Attack ===")
    print("PB1 = CB1 ^ (CA1 ^ PA1)\n")

    try:
        # ========= INPUT =========
        ca1 = clean_hex(input("C1: "))
        pa1 = clean_hex(input("P1: "))
        cb1 = clean_hex(input("C2: "))

        if not (len(ca1) == len(pa1) == len(cb1)):
            print("[!] Warning: panjang tidak sama")

        # ========= CORE =========
        ks = xor_bytes(ca1, pa1)
        pb1 = xor_bytes(cb1, ks)

        # ========= OUTPUT =========
        encoded = encode(pb1)

        print("\n=== HASIL ===")
        print("HEX :", pb1.hex().upper())

        try:
            print("STR :", pb1.decode())
        except:
            print("STR : (non-printable)")

        # ===== FLAG OPSIONAL =====
        if OUTPUT_FLAG:
            print("FLAG :", f"FLAG{{{pb1.hex().upper()}}}")
        # =========================

        # ===== NC OPSIONAL =====
        if USE_NC:
            send_nc(encoded)
        # ======================

    except ValueError:
        print("[!] HEX tidak valid")


if __name__ == "__main__":
    main()