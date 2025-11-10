import fcntl
import time
import os

filename = "demo_flock.txt"

with open(filename, "w+") as f:
    print(f"Process {os.getpid()} waiting for flock...")
    fcntl.flock(f, fcntl.LOCK_EX)  # Acquire exclusive lock
    print(f"Process {os.getpid()} got the flock lock!")
    f.write(f"Locked by {os.getpid()}\n")
    time.sleep(5)
    print("Releasing flock lock...")
    fcntl.flock(f, fcntl.LOCK_UN)
