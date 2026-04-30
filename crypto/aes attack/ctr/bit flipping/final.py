def ctr_bit_flip_attack(pt, old, new, ct_hex):
    pos = pt.find(old)
    if pos < 0:
        raise ValueError("Target tidak ditemukan di plaintext")

    ct = bytearray.fromhex(ct_hex)

    # XOR langsung tanpa loop verbose
    for i, (o, n) in enumerate(zip(old.encode(), new.encode())):
        ct[pos + i] ^= o ^ n

    return ct.hex().upper()


# === CONFIG ===
original_pt = "uid=1337&role=user&exp=9999"
find_word   = "user"
replace_with = "root"
original_ct_hex = "3A8F416D3133333726726F6C653DD4B1A36C2F85C1D2"

# === RUN ===
new_ct = ctr_bit_flip_attack(original_pt, find_word, replace_with, original_ct_hex)

print("New Ciphertext:", new_ct)
print("Modified Plaintext:", original_pt.replace(find_word, replace_with))