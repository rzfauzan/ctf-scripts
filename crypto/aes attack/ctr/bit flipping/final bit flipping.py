import base64
import socket

# ================= CONFIG =================
OUTPUT_MODE = "hex"     # hex / base64 / raw
OUTPUT_FLAG = False     # True kalau butuh FLAG{}
USE_NC = False          # True kalau mau kirim ke server

HOST = "chall.ctf.com"
PORT = 1234
# =========================================


def flip_ctr(cipher, old, new, offset):
    old_b, new_b = old.encode(), new.encode()

    if len(old_b) != len(new_b):
        print("[!] Warning: panjang beda")

    if offset + len(old_b) > len(cipher):
        raise ValueError("Offset keluar dari ciphertext")

    c = bytearray(cipher)
    for i in range(len(old_b)):
        c[offset+i] ^= old_b[i] ^ new_b[i]

    return bytes(c)


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
        s.recv(4096)  # banner optional
        s.sendall(payload + b"\n")
        print(s.recv(4096).decode(errors="ignore"))
    finally:
        s.close()
# ==============================================


def main():
    print("=== AES-CTR Bit-Flipping Tool ===")

    try:
        cipher = bytes.fromhex(input("Ciphertext (HEX): ").strip())
        old = input("Plaintext lama : ")
        new = input("Plaintext baru : ")
        offset = int(input("Offset        : "))

        modified = flip_ctr(cipher, old, new, offset)
        out = encode(modified)

        print("\n=== PAYLOAD ===")
        try:
            print(out.decode())
        except:
            print(out)

        # ===== FLAG OPSIONAL =====
        if OUTPUT_FLAG:
            print(f"\nFLAG{{{modified.hex().upper()}}}")
        # =========================

        # ===== NC OPSIONAL =====
        if USE_NC:
            send_nc(out)
        # ======================

        # ===== CLEAN OUTPUT OPSIONAL =====
        srv = input("\nOutput server (opsional): ").strip()
        if srv:
            try:
                print("Decoded:", bytes.fromhex(srv).decode(errors="ignore"))
            except:
                print("Raw:", srv)
        # ================================

    except Exception as e:
        print("[!] Error:", e)


if __name__ == "__main__":
    main()