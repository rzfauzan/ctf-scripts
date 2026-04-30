# Binary Exploitation Notes

### 1. Format String (Stack & Memory Analysis)
Jika di stack posisi ke-11 berisi alamat `0x0804a000` dan di alamat itu ada teks **"RAHASIA"**:

*   **`%11$p`** → Hasil: `0x0804a000` (Cuma ngasih tau alamatnya)
*   **`%11$x`** → Hasil: `804a000` (Cuma ngasih tau angkanya)
*   **`%11$s`** → Hasil: `RAHASIA` (Ngintip isi di dalam alamat tersebut)

**Poin Penting:**
*   **Canary Linux:** Selalu diakhiri dengan `\x00` (null byte) untuk mencegah string leak. Gunakan `%p` untuk membacanya karena tidak berhenti di null.
*   **Direct Parameter Access:** Gunakan `%11$p` untuk langsung membaca parameter ke-11 tanpa mencetak parameter lainnya.

---

### 2. System Configuration & ASLR
Cek status pengacakan alamat memori (ASLR):
```bash
# Cek status
cat /proc/sys/kernel/randomize_va_space

# Konfigurasi ASLR (0: Off, 1: Conservative, 2: Full)
echo 0 | sudo tee /proc/sys/kernel/randomize_va_space