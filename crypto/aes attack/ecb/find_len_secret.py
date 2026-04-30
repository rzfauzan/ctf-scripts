import string
import requests
import subprocess

# ================= CONFIG =================
MODE = "dummy"   # nc / web_get / web_post / local / dummy
HOST = "10.10.1.5"
PORT = 1337
URL  = "http://challenge.lks.id/encrypt"

USE_PERSISTENT = False
# =========================================


# ================= ORACLE =================
if MODE == "nc":
    from pwn import remote

    if USE_PERSISTENT:
        r = remote(HOST, PORT)

        def oracle(payload):
            r.sendlineafter(b"Masukkan plaintext: ", payload.encode())
            return r.recvline().decode().strip()
    else:
        def oracle(payload):
            r = remote(HOST, PORT)
            r.sendlineafter(b"Masukkan plaintext: ", payload.encode())
            res = r.recvline().decode().strip()
            r.close()
            return res


elif MODE == "web_get":
    def oracle(payload):
        return requests.get(URL, params={'input': payload}).text.strip()


elif MODE == "web_post":
    def oracle(payload):
        return requests.post(URL, json={'plaintext': payload}).text.strip()


elif MODE == "local":
    def oracle(payload):
        return subprocess.check_output(['python3', 'encrypt.py', payload]).decode().strip()


else:
    import hashlib
    secret = "LKS{123}"

    def oracle(payload):
        full = payload + secret
        pad = 16 - len(full) % 16
        full += chr(pad) * pad

        return "".join(
            hashlib.md5(full[i:i+16].encode()).hexdigest()
            for i in range(0, len(full), 16)
        )
# =========================================


# ================= HELPER =================
def is_hex(data):
    try:
        int(data, 16)
        return True
    except:
        return False


def get_block_len(data):
    return len(data) // 2 if is_hex(data) else len(data)
# =========================================


# ================= FIND LENGTH =================
def find_secret_length():
    print("[*] Mencari panjang secret...")

    base = oracle("")
    if not base:
        print("[!] Oracle tidak merespon")
        return None

    base_len = get_block_len(base)

    for i in range(1, 65):
        if get_block_len(oracle("A" * i)) > base_len:
            secret_len = base_len - (i - 1)

            print(f"[+] Trigger di padding ke-{i}")
            print(f"[+] Secret length: {secret_len} byte")
            return secret_len

    print("[!] Gagal deteksi panjang")
    return None
# =========================================


if __name__ == "__main__":
    find_secret_length()

    # if MODE == "nc" and USE_PERSISTENT:
    #     r.close()