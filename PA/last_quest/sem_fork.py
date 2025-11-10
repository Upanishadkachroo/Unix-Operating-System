import os
import time
from multiprocessing import Semaphore

def child_process(sem):
    print(f"Child {os.getpid()} waiting for semaphore...")
    sem.acquire()
    print(f"Child {os.getpid()} acquired semaphore!")
    for i in range(3):
        print(f"Child process running step {i+1}")
        time.sleep(1)
    print("Child releasing semaphore.")
    sem.release()

if __name__ == "__main__":
    sem = Semaphore(1)  # Shared semaphore
    pid = os.fork()

    if pid == 0:
        # Child process
        child_process(sem)
    else:
        # Parent process
        sem.acquire()
        print(f"Parent {os.getpid()} acquired semaphore!")
        for i in range(3):
            print(f"Parent process running step {i+1}")
            time.sleep(1)
        print("Parent releasing semaphore.")
        sem.release()
        os.wait()
