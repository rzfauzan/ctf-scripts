import string
import re

BLOCK_SIZE = 16
CANDIDATES = string.ascii_letters + string.digits + "{}_-"

# ================= CONFIG =================
USE_NC = False
USE_WEB = False
AUTO_FLAG = True
# =========================================


# ================= ORACLE =================
def oracle(payload: bytes) -> bytes:
    if USE_NC:
        from pwn import remote
        r = remote("chall.ctf.com", 1337)
        r.sendlineafter(b"Input: ", payload)
        res = r.recvline().strip()
        r.close()
        return res

    elif USE_WEB:
        import requests
        url = "http://chall.ctf.com/encrypt"
        return requests.get(url, params={"data": payload.decode()}).content

    else:
        # Dummy
        secret = b"LKS{ECB_FAST_MODE}"
        full = payload + secret
        pad = BLOCK_SIZE - len(full) % BLOCK_SIZE
        full += bytes([pad]) * pad

        from hashlib import md5
        return b"".join(md5(full[i:i+BLOCK_SIZE]).digest()
                        for i in range(0, len(full), BLOCK_SIZE))
# =========================================


def detect_ecb():
    data = oracle(b"A" * (BLOCK_SIZE * 4))
    blocks = [data[i:i+BLOCK_SIZE] for i in range(0, len(data), BLOCK_SIZE)]
    return len(blocks) != len(set(blocks))


def find_secret_length():
    base = len(oracle(b""))
    for i in range(1, 64):
        if len(oracle(b"A" * i)) > base:
            return base - i
    return 0


def solve():
    print("[*] Detecting ECB...")
    if not detect_ecb():
        print("[!] Not ECB mode")
        return

    print("[+] ECB detected")

    secret_len = find_secret_length()
    print(f"[+] Secret length: {secret_len}\n")

    recovered = b""

    for i in range(secret_len):
        pad_len = BLOCK_SIZE - (len(recovered) % BLOCK_SIZE) - 1
        prefix = b"A" * pad_len

        block_idx = len(recovered) // BLOCK_SIZE
        start = block_idx * BLOCK_SIZE
        end = start + BLOCK_SIZE

        target = oracle(prefix)[start:end]

        # 🔥 OPTIMIZED: dictionary sekali per iterasi
        lookup = {}
        base = prefix + recovered

        for c in CANDIDATES:
            out = oracle(base + c.encode())
            lookup[out[start:end]] = c

        if target in lookup:
            recovered += lookup[target].encode()
            print(f"[+] {i+1:02}: {recovered.decode(errors='ignore')}")
        else:
            print("[!] Stuck")
            break

    print("\n=== RESULT ===")
    result = recovered.decode(errors="ignore")

    # ================= OPTIONAL FLAG =================
    if AUTO_FLAG:
        m = re.search(r'[A-Za-z0-9_]*\{.*?\}', result)
        if m:
            print("[+] FLAG:", m.group())
        else:
            print("[*] RESULT:", result)
    else:
        print("[*] RESULT:", result)
    # ================================================


if __name__ == "__main__":
    # ===== optional persistent =====
    # if USE_NC:
    #     from pwn import remote
    #     r = remote("chall.ctf.com", 1337)

    solve()

    # if USE_NC:
    #     r.close()