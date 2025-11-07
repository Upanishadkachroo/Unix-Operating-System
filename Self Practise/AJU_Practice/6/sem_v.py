import sysv_ipc

key = 1234
semaphore = sysv_ipc.Semaphore(key)

print(f"[V] Performing V (signal) operation...")

# Perform V (signal)
semaphore.release()  # increases value by 1
print(f"[V] Semaphore released successfully!")
print(f"[V] Current semaphore value: {semaphore.value}")
