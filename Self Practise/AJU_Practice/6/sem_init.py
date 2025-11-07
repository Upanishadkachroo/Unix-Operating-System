import sysv_ipc

# Create (or get existing) semaphore with unique key
key = 1234  # same key must be used in all programs

# IPC_CREAT ensures it’s created if not already present
semaphore = sysv_ipc.Semaphore(key, sysv_ipc.IPC_CREAT, initial_value=1)

print(f"[INIT] Semaphore created successfully!")
print(f"[INIT] Semaphore ID: {semaphore.id}")
print(f"[INIT] Initial value: {semaphore.value}")
