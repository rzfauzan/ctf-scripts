import base64
import socket
import re

# ================= CONFIG =================
OUTPUT_MODE = "raw"     # raw / hex / base64
OUTPUT_FLAG = False     # True kalau butuh FLAG{}
AUTO_DETECT_FLAG = True # auto detect flag
USE_NC = False          # True kalau kirim ke server

HOST = "chall.ctf.com"
PORT = 1234
# =========================================


def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


def encode(data):
    if OUTPUT_MODE == "hex":
        return data.hex().upper().encode()
    if OUTPUT_MODE == "base64":
        return base64.b64encode(data)
    return data


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
    print("=== AES-CTR Nonce Reuse ===")

    try:
        p_a = bytes.fromhex(input("Plaintext A (HEX): ").replace(" ", ""))
        c_a = bytes.fromhex(input("Ciphertext A (HEX): ").replace(" ", ""))
        c_b = bytes.fromhex(input("Ciphertext B (HEX): ").replace(" ", ""))

        if not (len(p_a) == len(c_a) == len(c_b)):
            print("[!] Warning: panjang beda")

        # CORE (langsung, tanpa variabel tambahan)
        p_b = xor(xor(c_a, c_b), p_a)

        print("\n=== HASIL ===")
        print("HEX :", p_b.hex().upper())

        try:
            decoded = p_b.decode(errors="ignore").replace('\x00', '')
            print("STR :", decoded)
        except:
            decoded = ""
            print("STR : (non-printable)")

        # ===== AUTO FLAG =====
        if AUTO_DETECT_FLAG and decoded:
            m = re.search(r'[A-Za-z0-9_]*\{.*?\}', decoded)
            if m:
                print("[+] FOUND:", m.group())
        # =====================

        # ===== FLAG OPSIONAL =====
        if OUTPUT_FLAG:
            print(f"\nFLAG{{{p_b.hex().upper()}}}")
        # =========================

        # ===== NC OPSIONAL =====
        if USE_NC:
            send_nc(encode(p_b))
        # =======================

    except Exception as e:
        print("[!] Error:", e)


if __name__ == "__main__":
    main()