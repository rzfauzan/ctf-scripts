import base64
import socket

# ================= CONFIG =================
OUTPUT_MODE = "hex"     # hex / base64 / raw
OUTPUT_FLAG = False     # True kalau butuh format flag
USE_NC = False          # True kalau kirim ke server

HOST = "chall.ctf.com"
PORT = 1234
# =========================================


# ================= HELPER =================
def clean_hex(h):
    return bytes.fromhex(h.replace(" ", ""))

def encode(data):
    if OUTPUT_MODE == "hex":
        return data.hex().upper().encode()
    elif OUTPUT_MODE == "base64":
        return base64.b64encode(data)
    return data
# =========================================


def flip_cfb(c, p_old, p_new):
    return bytearray(
        c[i] ^ p_old[i] ^ p_new[i]
        for i in range(len(p_old))
    )


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
    print("=== AES-CFB Bit Flipping ===")

    try:
        # ========= INPUT =========
        cipher = clean_hex(input("Ciphertext: "))
        p_old = input("Plaintext lama : ").encode()
        p_new = input("Plaintext baru : ").encode()

        if len(p_old) != len(p_new):
            print("[!] panjang harus sama")
            return

        if len(p_old) > len(cipher):
            print("[!] plaintext > ciphertext")
            return

        # ========= EXPLOIT =========
        modified = flip_cfb(cipher, p_old, p_new)
        encoded = encode(modified)

        print("\n=== HASIL ===")
        try:
            print(encoded.decode())
        except:
            print(encoded)

        # ===== FLAG OPSIONAL =====
        if OUTPUT_FLAG:
            print("FLAG : FLAG{" + modified.hex().upper() + "}")
        # =========================

        # ===== NC OPSIONAL =====
        if USE_NC:
            send_nc(encoded)
        # ======================

    except ValueError:
        print("[!] HEX tidak valid")


if __name__ == "__main__":
    main()