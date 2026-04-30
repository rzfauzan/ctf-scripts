from solver import solve
import solver

# ================= CONFIG =================
MODE = "dummy"   # nc / web / local / dummy
HOST = "127.0.0.1"
PORT = 1337
URL  = "http://127.0.0.1:5000/encrypt"
# =========================================


# ================= ORACLE =================
if MODE == "nc":
    from pwn import remote

    # ===== NON-PERSISTENT =====
    def oracle(payload: bytes) -> bytes:
        r = remote(HOST, PORT)
        r.sendlineafter(b"Input: ", payload)
        res = bytes.fromhex(r.recvline().strip().decode())
        r.close()
        return res

    # ===== PERSISTENT (AKTIFKAN JIKA PERLU) =====
    # r = remote(HOST, PORT)
    # def oracle(payload: bytes) -> bytes:
    #     r.sendlineafter(b"Input: ", payload)
    #     return bytes.fromhex(r.recvline().strip().decode())


elif MODE == "web":
    import requests

    def oracle(payload: bytes) -> bytes:
        return bytes.fromhex(
            requests.get(URL, params={"data": payload.decode()}).text.strip()
        )


elif MODE == "local":
    from pwn import process

    def oracle(payload: bytes) -> bytes:
        p = process("./chall")
        p.sendlineafter(b"Input: ", payload)
        out = bytes.fromhex(p.recvline().strip().decode())
        p.close()
        return out


else:
    from Crypto.Cipher import AES

    KEY = b"YELLOW SUBMARINE"
    SECRET = b"LKS{ECB_BYTE_BY_BYTE_MASTER}"

    def pad(d):
        return d + bytes([16 - len(d) % 16]) * (16 - len(d) % 16)

    def oracle(payload: bytes) -> bytes:
        return AES.new(KEY, AES.MODE_ECB).encrypt(pad(payload + SECRET))


# Inject ke solver
solver.oracle = oracle


# ================= RUN =================
if __name__ == "__main__":
    solve()

    # ===== kalau pakai persistent =====
    # if MODE == "nc":
    #     r.close()