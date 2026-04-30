def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


def clean_hex(s):
    return s.replace(" ", "").strip()


def main():
    print("=== OFB Nonce Reuse Recovery Tool ===")

    try:
        # INPUT
        c1 = bytes.fromhex(clean_hex(input("C1 (hex): ")))
        c2 = bytes.fromhex(clean_hex(input("C2 (hex): ")))
        p1 = bytes.fromhex(clean_hex(input("P1 (hex): ")))

        # CORE ATTACK (langsung)
        p2 = xor_bytes(xor_bytes(c1, c2), p1)

        # OUTPUT
        print("\n--- RESULT ---")
        print("HEX :", p2.hex().upper())

        try:
            print("STR :", p2.decode())
        except:
            print("STR : (non-printable)")

    except ValueError:
        print("[!] HEX tidak valid")
    except Exception as e:
        print("[!] Error:", e)


if __name__ == "__main__":
    main()