# Binary Exploitation Notes — Alignment, Libc Leak, and Function Offset

## 1. Kenapa Kadang Perlu Stack Alignment?

Alignment adalah proses merapikan susunan memori agar CPU bisa mengakses data dengan benar dan efisien.

Secara umum ada dua jenis alignment yang sering muncul saat exploit:

### • Stack Alignment (CPU / ABI Rule)
Pada arsitektur **64-bit**, stack biasanya harus berada pada kelipatan **16-byte** sebelum pemanggilan fungsi penting seperti `system()`, `printf()`, atau gadget tertentu.

Jika posisi stack tidak aligned:
- fungsi libc bisa crash,
- exploit gagal,
- sering muncul `SIGSEGV`.

Karena itu pada ROP 64-bit kadang perlu menambahkan gadget `ret` sebagai penyeimbang stack.

> Di 32-bit aturan ini jauh lebih longgar, jadi tidak selalu dibutuhkan.

---

### • Compiler Padding / Variable Alignment
Compiler seperti GCC sering menambahkan ruang kosong (*padding*) antar variabel stack.

Tujuannya:
- mempercepat akses CPU,
- menjaga alignment data.

Akibatnya:
- buffer `char buf[64]` belum tentu tepat diikuti Canary,
- offset ke Canary bisa menjadi `72`, `80`, bahkan `88` byte.

Jadi offset exploit **tidak boleh menebak dari ukuran variabel saja**, harus dicek dengan:
- GDB,
- cyclic pattern,
- atau telescope stack.

---

## 2. Cara Menemukan Leak Alamat Libc dari Format String

Pada bug format string, kita biasanya melakukan dump stack:

```bash
%p %p %p %p %p %p ...
```

Tujuannya mencari pointer yang menunjuk ke region libc.

### Ciri Umum Alamat Libc
- **32-bit:** biasanya diawali `0xf7xxxxxx`
- **64-bit:** biasanya diawali `0x7fxxxxxx`

Karena shared library (`libc.so`) dimapping di area tersebut.

---

### Cara Menemukan Posisi Leak

#### Metode GDB
Jalankan binary sampai tepat sebelum `printf(buffer)` lalu cek stack:

```bash
telescope $rsp
```

atau pada 32-bit:

```bash
x/50wx $esp
```

Cari pointer yang:
- menunjuk ke `__libc_start_main`
- `_IO_2_1_stdout_`
- `puts`
- `printf`
- atau simbol libc lainnya.

Jika pointer libc muncul pada urutan ke-5 stack argument, maka payload leak-nya:

```bash
%5$p
```

---

#### Metode Bruteforce Manual

Kirim banyak `%p`:

```bash
%p.%p.%p.%p.%p.%p.%p.%p.%p.%p
```

Lalu cari output yang memiliki awalan:
- `0xf7`
- `0x7f`

Setelah ketemu, validasi menggunakan:
- GDB
- atau file libc.

---

## 3. Cara Mencari Offset Fungsi di Libc

Nilai seperti `0x67360` adalah **offset tetap** suatu fungsi dari awal file `libc.so.6`.

Rumusnya:

Runtime Address = Libc Base + Function Offset

---

### Metode 1 — readelf

Jika punya file libc:

```bash
readelf -s libc.so.6 | grep puts
```

Contoh output:

```bash
420: 00067360   456 FUNC    GLOBAL DEFAULT   13 puts@@GLIBC_2.2.5
```

Maka:

```bash
puts offset = 0x67360
```

---

### Metode 2 — Pwntools

```python
from pwn import *

libc = ELF('./libc.so.6')
print(hex(libc.symbols['puts']))
```

Output:

```bash
0x67360
```

---

## 4. Menghitung Libc Base dari Leak

Jika hasil leak runtime:

```bash
puts@libc = 0xf7e12360
```

dan offset `puts`:

```bash
0x67360
```

Maka:

```bash
libc_base = leak_puts - puts_offset
libc_base = 0xf7e12360 - 0x67360
libc_base = 0xf7dbb000
```

Setelah `libc_base` diketahui, alamat lain tinggal dihitung:

```bash
system = libc_base + system_offset
/bin/sh = libc_base + binsh_offset
```

Ini adalah dasar dari teknik **ret2libc**.

---

## 5. Mengecek Status ASLR

Untuk melihat apakah ASLR aktif:

```bash
cat /proc/sys/kernel/randomize_va_space
```

Nilai:
- `0` = ASLR mati
- `1` = random stack/shared library
- `2` = full randomization (default Linux modern)

Jika ASLR aktif, alamat libc berubah setiap run, sehingga leak wajib dilakukan.

---

## Summary Singkat

- **Alignment** membuat offset stack kadang tidak sesuai ukuran variabel.
- **Libc leak** pada format string dicari dari pointer `0xf7` / `0x7f`.
- **Function offset** diambil dari `readelf` atau `pwntools`.
- **Libc base** dihitung dengan `leak - offset`.
- Setelah base ketemu, `system` dan `"/bin/sh"` bisa dihitung untuk ret2libc.
