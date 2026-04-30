from pwn import xor

# === DATA BLOK 1 ===
p_a1 = bytes.fromhex("46 49 4c 45 53 54 41 52 54 3a 49 4d 47 30 30 00")
c_a1 = bytes.fromhex("B2 0F 3C 91 24 68 05 E7 43 5D 9A F1 28 4E 7C 55")
c_b1 = bytes.fromhex("A5 1A 29 84 37 7D 10 F2 58 48 8F E4 3B 5B 69 42")

# === DATA BLOK 2 ===
p_a2 = bytes.fromhex("50 41 59 4C 4F 41 44 3A 53 45 43 52 45 54 30 00")
c_a2 = bytes.fromhex("7A C3 81 0B 9F 56 D4 22 E8 14 63 AE 5B 92 3F 0D")
c_b2 = bytes.fromhex("6D D4 96 1E 8C 43 C1 35 FF 09 74 BB 4E 87 2A 18")

# === BLOK 1 ===
ks1 = xor(c_a1, p_a1)
p_b1 = xor(c_b1, ks1)

# === BLOK 2 ===
p_b2 = xor(c_a2, c_b2, p_a2)

# === OUTPUT TERPISAH ===
print("=== HASIL BLOK 1 ===")
print("Hex :", p_b1.hex(' ').upper())
print("Str :", p_b1.decode('ascii', errors='ignore'))

print("\n=== HASIL BLOK 2 ===")
print("Hex :", p_b2.hex(' ').upper())
print("Str :", p_b2.decode('ascii', errors='ignore'))