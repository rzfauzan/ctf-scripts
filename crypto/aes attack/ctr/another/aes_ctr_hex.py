import base64
import socket

# ================= CONFIG =================
OUTPUT_MODE = "raw"     # raw / hex / base64
OUTPUT_FLAG = False     # True kalau butuh FLAG{}
USE_NC = False          # True kalau mau kirim ke server

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
    print("=== AES-CTR Key Reuse ===")

    try:
        ct_flag = bytes.fromhex(input("Ciphertext FLAG (HEX): ").strip())
        ct_msg  = bytes.fromhex(input("Ciphertext Known (HEX): ").strip())
        pt_msg  = input("Plaintext Known: ").encode()

        if len(ct_msg) != len(pt_msg):
            print("[!] Warning: panjang beda")

        # CORE
        pt_flag = xor(ct_flag, xor(ct_msg, pt_msg))

        print("\n=== HASIL ===")
        try:
            print("STR :", pt_flag.decode())
        except:
            print("STR : (non-printable)")

        print("HEX :", pt_flag.hex().upper())

        # ===== FLAG OPSIONAL =====
        if OUTPUT_FLAG:
            print(f"\nFLAG{{{pt_flag.hex().upper()}}}")
        # =========================

        # ===== NC OPSIONAL =====
        if USE_NC:
            send_nc(encode(pt_flag))
        # =======================

    except ValueError:
        print("[!] HEX tidak valid")


if __name__ == "__main__":
    main()