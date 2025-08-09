import sys
import time
import mmap

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <megabytes> [seconds]")
    sys.exit(1)

mb = int(sys.argv[1])
seconds = int(sys.argv[2]) if len(sys.argv) > 2 else 0

size = mb * 1024 * 1024  # bytes

print(f"Allocating {mb} MB of memory...")

# Create an anonymous memory map (similar to malloc in C)
mm = mmap.mmap(-1, size, flags=mmap.MAP_PRIVATE | mmap.MAP_ANONYMOUS)

print("Memory allocated. Touching each page...")

# Touch each page to force physical allocation
for i in range(0, size, mmap.PAGESIZE):
    mm[i] = 0

print("Holding memory...")
if seconds > 0:
    time.sleep(seconds)
else:
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

mm.close()
print("Memory freed.")

