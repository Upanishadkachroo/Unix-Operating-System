import sysv_ipc
import time

# Same keys as process A
SHM_KEY = 1234
SEM_KEY = 5678

# Connect to existing shared memory and semaphores
shm = sysv_ipc.SharedMemory(SHM_KEY)
sem = sysv_ipc.Semaphore(SEM_KEY)
sem2 = sysv_ipc.Semaphore(SEM_KEY + 1)

print("Process B connected. Ready for chat.")

while True:
    # Wait for message from Process A
    sem.acquire()
    data = shm.read(1024).split(b'\0')[0].decode()
    print(f"A: {data}")
    if data.lower() == "exit":
        break

    # Write reply
    msg = input("You (B): ")
    shm.write(msg.encode() + b'\0')
    sem2.release()  # Notify A to read

    if msg.lower() == "exit":
        break

print("Chat ended.")
