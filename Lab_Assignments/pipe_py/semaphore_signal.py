import sysv_ipc

key=1234

sem=sysv_ipc.Semaphore(key)

print("perform V signal operation")
sem.release() #V operation
print("V (signal) operation successful, resources released")

