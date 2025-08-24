import os
import sysv_ipc

key=1234 # same as of create_semaphore.py

sem=sysv_ipc.Semaphore(key)

print("try perform P (wait) operation")
sem.acquire() # P operation
print("P (wait) operation successfull, resources acquired")
