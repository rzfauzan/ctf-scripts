import string
import requests
from pwn import *

# ================= CONFIG =================
USE_NC = False
USE_WEB = False
AUTO_FLAG = True

HOST = "chall.ctf.com"
PORT = 1337
URL  = "http://chall.ctf.com/encrypt"

BLOCK_SIZE = 16
CANDIDATES = string.printable
# =========================================


# ================= ORACLE =================
def oracle(payload):
    if USE_NC:
        # ===== NON-PERSISTENT =====
        r = remote(HOST, PORT)
        r.sendline(payload.encode())
        resp = r.recvline().decode().strip()
        r.close()
        return resp

        # ===== PERSISTENT (AKTIFKAN JIKA PERLU) =====
        # global r
        # r.sendline(payload.encode())
        # return r.recvline().decode().strip()

    elif USE_WEB:
        return requests.get(URL, params={'data': payload}).json()['ciphertext']

    else:
        # Dummy
        import hashlib
        secret = "LKS{AES_ECB_IS_EASY}"
        full = payload + secret
        pad = BLOCK_SIZE - len(full) % BLOCK_SIZE
        full += chr(pad) * pad

        return "".join(
            hashlib.md5(full[i:i+BLOCK_SIZE].encode()).hexdigest()
            for i in range(0, len(full), BLOCK_SIZE)
        )
# =========================================


def detect_mode(sample):
    is_hex = all(c in string.hexdigits for c in sample)
    return is_hex, (BLOCK_SIZE * 2 if is_hex else BLOCK_SIZE)


def find_secret_length():
    base = oracle("")
    is_hex, _ = detect_mode(base)

    mul = 2 if is_hex else 1
    base_len = len(base) // mul

    for i in range(1, 64):
        if len(oracle("A" * i)) // mul > base_len:
            return base_len - (i - 1), is_hex

    return 0, True


def solve():
    print("=== AES ECB BYTE-BY-BYTE (Optimized) ===")

    secret_len, is_hex = find_secret_length()
    if secret_len == 0:
        print("[!] Gagal deteksi panjang")
        return

    chunk = BLOCK_SIZE * 2 if is_hex else BLOCK_SIZE
    recovered = ""

    print(f"[+] Panjang secret: {secret_len}\n")

    for i in range(secret_len):
        pad_len = BLOCK_SIZE - 1 - (i % BLOCK_SIZE)
        pad = "A" * pad_len

        ref = oracle(pad)
        block_idx = (i // BLOCK_SIZE) * chunk
        target = ref[block_idx:block_idx + chunk]

        # 🔥 OPTIMIZED LOOKUP
        lookup = {}
        base = pad + recovered

        for ch in CANDIDATES:
            out = oracle(base + ch)
            lookup[out[block_idx:block_idx + chunk]] = ch

        if target in lookup:
            recovered += lookup[target]
            print(f"[+] {i+1:02}: {repr(lookup[target])} → {recovered}")
        else:
            print(f"[!] Stuck di posisi {i+1}")
            break

    print("\n" + "="*40)

    # ================= FLAG HANDLING =================
    if AUTO_FLAG:
        import re
        m = re.search(r'[A-Za-z0-9_]*\{.*?\}', recovered)
        if m:
            print("[+] FLAG FOUND:", m.group())
        else:
            print("[*] RESULT:", recovered)
    else:
        print("[*] RESULT:", recovered)
    # ================================================

    print("="*40)


if __name__ == "__main__":
    # if USE_NC:
    #     r = remote(HOST, PORT)

    solve()

    # if USE_NC:
    #     r.close()