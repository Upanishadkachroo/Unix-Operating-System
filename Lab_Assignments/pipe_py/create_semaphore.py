import sysv_ipc

#create semaphore
key=1234

#binary semaphore
sem=sysv_ipc.Semaphore(key, sysv_ipc.IPC_CREX, initial_value=1)

print(f"semaphore created with id: {sem.id}, key:{key}")
