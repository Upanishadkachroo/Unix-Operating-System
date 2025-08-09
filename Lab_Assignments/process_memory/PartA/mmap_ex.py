# mmap_example.py
import mmap
import os
import time

print(f"PID: {os.getpid()}")

# Map 1 page (usually 4096 bytes) of anonymous, private memory
page_size = mmap.PAGESIZE
mm = mmap.mmap(-1, page_size, flags=mmap.MAP_PRIVATE | mmap.MAP_ANONYMOUS)

print(f"Mapped {page_size} bytes of anonymous, private memory.")
print("Sleeping for 5 minutes... Check VSZ and RSS now.")

time.sleep(300)  # keep process alive so you can inspect

mm.close()

