import time
import os
import sys
import mmap


if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <megabytes> [seconds]")
    sys.exit(1)

mb = int(sys.argv[1])

if len(sys.argv) > 2:
    seconds = int(sys.argv[2])
else:
    seconds = 0

size = mb * 1024 * 1024

print(f"Allocating memory")

# create anonymous memory
mm = mmap.mmap(-1, size, flags=mmap.MAP_PRIVATE | mmap.MAP_ANONYMOUS)

print(f"Memory allocated")

# touch to show memory in RSS
for i in range(0, size, mmap.PAGESIZE):
    mm[i] = 0

print(f"Memory holding")

if seconds > 0:
    time.sleep(seconds)
else:
    while True:
        time.sleep(1)

mm.close()

