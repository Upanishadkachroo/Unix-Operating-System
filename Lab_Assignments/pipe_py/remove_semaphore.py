import sysv_ipc

key=1234
sem=sysv_ipc.Semaphore(key)
sem.remove()
print("semaphore removed")
