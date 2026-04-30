### **Analisis Stack & Memory**

Jika di stack posisi ke-11 berisi `0x0804a000` dan di alamat itu ada teks **"RAHASIA"**:

*   **`%11$p`** → Hasil: `0x0804a000` (Cuma ngasih tau alamatnya)
*   **`%11$x`** → Hasil: `804a000` (Cuma ngasih tau angkanya)
*   **`%11$s`** → Hasil: `RAHASIA` (Ngintip isi di dalam alamat tersebut)

---

### **Poin Penting**

*   **Canary Linux:** Selalu diakhiri dengan `\x00` (null byte) untuk mencegah string leak, tapi kita bisa baca dengan `%p` yang tidak stop di null.
*   **Direct Parameter Access:** Dengan `%11$p`, kita langsung baca parameter ke-11 tanpa perlu print yang lain.