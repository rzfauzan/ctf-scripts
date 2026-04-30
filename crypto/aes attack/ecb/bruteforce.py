import string
import re

# ================= CONFIG =================
BLOCK_SIZE = 16
SECRET_LEN = 32
USE_NC = False
USE_WEB = False
AUTO_FLAG = True
# =========================================

CANDIDATES = string.printable


# ================= ORACLE =================
def oracle(payload):
    if USE_NC:
        from pwn import remote
        r = remote("chall.ctf.com", 1337)
        r.sendlineafter(b"Input: ", payload.encode())
        res = r.recvline().decode().strip()
        r.close()
        return res

    elif USE_WEB:
        import requests
        return requests.get(
            "http://chall.ctf.com/encrypt",
            params={'data': payload}
        ).text.strip()

    else:
        # Dummy (FIX BUG: hapus typo BLOCK_SIZEs)
        secret = "LKS{ECB_IS_WEAK}"
        full = payload + secret
        pad = BLOCK_SIZE - len(full) % BLOCK_SIZE
        full += chr(pad) * pad

        import hashlib
        return "".join(
            hashlib.md5(full[i:i+BLOCK_SIZE].encode()).hexdigest()
            for i in range(0, len(full), BLOCK_SIZE)
        )
# =========================================


def solve():
    print("=== AES ECB Byte-at-a-Time ===")

    test = oracle("A")
    if not test:
        print("[!] Oracle belum aktif")
        return

    HEX_MODE = all(c in string.hexdigits for c in test)
    CHUNK = BLOCK_SIZE * 2 if HEX_MODE else BLOCK_SIZE

    recovered = ""

    print(f"[*] Mode: {'HEX' if HEX_MODE else 'RAW'}\n")

    for pos in range(SECRET_LEN):
        pad = "A" * (BLOCK_SIZE - 1 - (pos % BLOCK_SIZE))

        ref = oracle(pad)
        idx = (pos // BLOCK_SIZE) * CHUNK
        target = ref[idx:idx + CHUNK]

        for ch in CANDIDATES:
            res = oracle(pad + recovered + ch)
            if res[idx:idx + CHUNK] == target:
                recovered += ch
                print(f"[+] {pos+1:02}: {recovered}")
                break
        else:
            print(f"[!] Stop di posisi {pos+1}")
            break

    print("\n" + "="*40)

    # ===== FLAG HANDLING =====
    if AUTO_FLAG:
        m = re.search(r'[A-Za-z0-9_]*\{.*?\}', recovered)
        print("[+] FLAG:" if m else "[*] RESULT:", m.group() if m else recovered)
    else:
        print("[*] RESULT:", recovered)
    # =========================

    print("="*40)


if __name__ == "__main__":
    # ===== OPTIONAL PERSISTENT NC =====
    # if USE_NC:
    #     from pwn import remote
    #     r = remote("chall.ctf.com", 1337)

    solve()

    # if USE_NC:
    #     r.close()