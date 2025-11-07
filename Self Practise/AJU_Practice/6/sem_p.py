import sysv_ipc
import time

key = 1234  # must match the first program
semaphore = sysv_ipc.Semaphore(key)

print(f"[P] Trying to perform P (wait) operation...")

# Perform P (wait)
semaphore.acquire()  # decreases value by 1, blocks if 0
print(f"[P] Acquired semaphore successfully!")
print(f"[P] Current semaphore value: {semaphore.value}")

# Keep it for some time to simulate work
time.sleep(5)

print(f"[P] Done with critical section. (Semaphore held for 5 seconds)")
