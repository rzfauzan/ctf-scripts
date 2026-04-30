libc = ELF('./libc.so.6')
offset_puts = libc.symbols['puts']