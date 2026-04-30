1. Kenapa Kadang Ada Alignment, Kadang Enggak?

Alignment (perataan memori) itu seperti aturan parkir di memori. 
Ada dua jenis alignment yang sering bikin pusing:
Stack Alignment (CPU/OS): 
Di arsitektur 64-bit, CPU mengharuskan stack rata 16-byte saat memanggil fungsi tertentu (seperti system atau printf). 
Jika tidak pas, program akan crash (Segfault). Di 32-bit, aturan ini biasanya lebih longgar.
Compiler Alignment (Padding): 
Compiler (seperti GCC) sering menambah "jarak" (padding) antar variabel di stack agar data lebih cepat diakses oleh prosesor.
 Itulah kenapa meskipun buffer kamu cuma 64 byte, jarak ke Canary bisa jadi 72 atau 88 byte karena ada tambahan alignment dari compiler.
 
 2. Cara Tahu Offset Alamat Libc di Format String
 
 Kalau Canary gampang dicari karena ada null byte di belakangnya (misal: 0x...00), alamat libc di format string biasanya dikenali dari polanya:
 Cari Alamat yang Dimulai dengan 0xf7 (32-bit) atau 0x7f (64-bit): 
 Ini adalah rentang memori standar untuk shared libraries (libc).
 Gunakan GDB:
 Jalankan program di GDB sampai ke titik printf(buffer).
 Ketik stack 50 atau telescope.
 Cari alamat yang menunjuk ke dalam libc. 
 GDB biasanya akan memberi label seperti <__libc_start_main+231> atau <_IO_2_1_stdout_>.
 Hitung posisinya dari atas stack. 
 Jika dia ada di urutan ke-5, maka offsetnya adalah %5$p.
 
 Cara Bruteforce Manual: Kirim %p. sebanyak-banyaknya (misal 50 kali). 
 Lihat outputnya, ambil alamat yang punya awalan 0xf7 atau 0x7f, lalu cek di internet atau GDB apakah itu alamat valid milik fungsi libc.
 
 3. Cara Mencari Offset Fungsi (Misal 0x067360)
 Angka 0x067360 itu bukan angka gaib, tapi jarak tetap fungsi tersebut dari titik awal (base) file libc.so. 
 
 Cara nyarinya:
 Pakai Command Linux (readelf):
 Jika kamu punya file libc-nya (misal libc.so.6), ketik di terminal:readelf -s libc.so.6 | grep puts
 Outputnya akan muncul seperti ini:
 420: 00067360   456 FUNC    GLOBAL DEFAULT   13 puts@@GLIBC_2.2.5
 Nah, 00067360 itulah offsetnya!.
 Pakai Pwntools (Paling Gampang):
 
 Python
 from pwn import *
libc = ELF('./libc.so.6')
print(hex(libc.symbols['puts'])) # Ini akan munculin 0x67360

Rumus Keramatnya:
$$\text{Alamat Asli (Runtime)} = \text{Libc Base} + \text{Offset}$$

Jadi, kalau kamu dapet leak puts di alamat 0xf7e12360 dan tahu offsetnya 0x67360, kamu bisa nemuin Libc Base dengan:0xf7e12360 - 0x67360 = 0xf7db5000 (Libc Base).Setelah tahu Base, kamu tinggal tambah offset system atau "/bin/sh" ke Base tersebut untuk mendapatkan alamat aslinya di memori.


cat /proc/sys/kernel/randomize_va_space