# mmap_write_example.py
import mmap
import os
import time

print(f"PID: {os.getpid()}")

# Step 1: Map 1 page (usually 4 KB)
page_size = mmap.PAGESIZE
mm = mmap.mmap(-1, page_size, flags=mmap.MAP_PRIVATE | mmap.MAP_ANONYMOUS)

print(f"Mapped {page_size} bytes of anonymous, private memory.")
input("Press Enter to check memory BEFORE writing...")

# Step 2: Write to the page (forces physical allocation)
mm.seek(0)
mm.write(b'A')  # write 1 byte

print("Wrote 1 byte to the mapped page.")
input("Press Enter to check memory AFTER writing...")

# Keep alive so you can measure
time.sleep(60)

mm.close()

