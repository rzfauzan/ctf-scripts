### **Check ASLR Status**

`cat /proc/sys/kernel/randomize_va_space`

**Nilai & Penjelasan:**
*   **0**: Disabled (ASLR mati, alamat memori statis).
*   **1**: Conservative Randomization (Shared libraries, stack, mmap, dan VDSO diacak).
*   **2**: Full Randomization (Sama seperti 1, ditambah acak untuk segment data/heap).