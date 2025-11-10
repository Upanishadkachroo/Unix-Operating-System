import fcntl
import time
import os

filename = "demo_lockf.txt"

with open(filename, "w+") as f:
    print(f"Process {os.getpid()} trying to acquire lock...")
    fcntl.lockf(f, fcntl.LOCK_EX)  # Exclusive lock
    print(f"Process {os.getpid()} acquired lock!")
    f.write("Locked by process\n")
    time.sleep(5)
    print("Releasing lock...")
    fcntl.lockf(f, fcntl.LOCK_UN)
