import socket

BLOCK_SIZE = 16

# ================= CONFIG =================
USE_REMOTE = False      # True kalau pakai server
OUTPUT_FLAG = True      # True kalau decode ke string

HOST = "chall.ctf.com"
PORT = 1234
# =========================================


# ================= HELPER =================
def split_blocks(data):
    return [data[i:i+BLOCK_SIZE] for i in range(0, len(data), BLOCK_SIZE)]

def remove_padding(data):
    return data[:-data[-1]]
# =========================================


# ================= ORACLE =================
def oracle(payload):
    if USE_REMOTE:
        try:
            s = socket.socket()
            s.connect((HOST, PORT))
            s.recv(4096)
            s.sendall(payload + b"\n")
            resp = s.recv(4096).decode(errors="ignore")
            s.close()

            return "Invalid padding" not in resp
        except:
            return False
    else:
        raise Exception("Oracle belum diset")
# =========================================


def padding_oracle_attack(iv, ct):
    blocks = [iv] + split_blocks(ct)
    plaintext = b""

    for b in range(len(blocks) - 1, 0, -1):
        print(f"\n[*] Block {b}")

        prev, curr = blocks[b-1], blocks[b]
        inter = bytearray(BLOCK_SIZE)
        plain = bytearray(BLOCK_SIZE)

        for i in range(15, -1, -1):
            pad = BLOCK_SIZE - i

            for guess in range(256):
                c_prime = bytearray(BLOCK_SIZE)

                # set known bytes
                for j in range(15, i, -1):
                    c_prime[j] = inter[j] ^ pad

                c_prime[i] = guess

                if oracle(bytes(c_prime) + curr):
                    inter[i] = guess ^ pad
                    plain[i] = inter[i] ^ prev[i]

                    print(f"[+] {i}: {hex(plain[i])}")
                    break

        plaintext = bytes(plain) + plaintext

    return plaintext


def main():
    print("=== Padding Oracle Attack ===")

    try:
        iv = bytes.fromhex(input("IV : ").strip())
        ct = bytes.fromhex(input("CT : ").strip())

        pt = padding_oracle_attack(iv, ct)

        print("\n=== RESULT ===")
        print("Hex:", pt.hex())

        # ===== FLAG OPSIONAL =====
        if OUTPUT_FLAG:
            try:
                clean = remove_padding(pt)
                print("Decoded:", clean.decode())
            except:
                print("Raw:", pt)
        # =========================

    except Exception as e:
        print("[!] Error:", e)


if __name__ == "__main__":
    main()