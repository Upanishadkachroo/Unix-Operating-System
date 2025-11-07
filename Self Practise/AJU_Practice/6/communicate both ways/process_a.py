import sysv_ipc
import time

# Common keys for shared memory and semaphores
SHM_KEY = 1234
SEM_KEY = 5678

# Create shared memory (or get existing)
try:
    shm = sysv_ipc.SharedMemory(SHM_KEY, sysv_ipc.IPC_CREX, size=1024)
    print("Process A: Created shared memory.")
except sysv_ipc.ExistentialError:
    shm = sysv_ipc.SharedMemory(SHM_KEY)
    print("Process A: Connected to existing shared memory.")

# Create semaphore set of size 2 (write/read)
try:
    sem = sysv_ipc.Semaphore(SEM_KEY, sysv_ipc.IPC_CREX, initial_value=0)
    sem2 = sysv_ipc.Semaphore(SEM_KEY + 1, sysv_ipc.IPC_CREX, initial_value=1)
    print("Process A: Created semaphores.")
except sysv_ipc.ExistentialError:
    sem = sysv_ipc.Semaphore(SEM_KEY)
    sem2 = sysv_ipc.Semaphore(SEM_KEY + 1)
    print("Process A: Connected to semaphores.")

print("Process A ready for chat.")

while True:
    # Wait for write permission (sem2)
    sem2.acquire()

    msg = input("You (A): ")
    shm.write(msg.encode() + b'\0')
    sem.release()  # Notify Process B to read

    if msg.lower() == "exit":
        break

    # Wait for reply from Process B
    sem2.acquire()
    data = shm.read(1024).split(b'\0')[0].decode()
    print(f"B: {data}")
    if data.lower() == "exit":
        break
    sem.release()

# Cleanup (only by creator)
try:
    shm.remove()
    sem.remove()
    sem2.remove()
except:
    pass

print("Chat ended.")
