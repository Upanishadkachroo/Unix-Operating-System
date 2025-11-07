import sysv_ipc
import os
import time

# Unique key for semaphore
KEY = 1234

# Create semaphore with initial value 1 (resource available)
try:
    sem = sysv_ipc.Semaphore(KEY, sysv_ipc.IPC_CREX, initial_value=1)
    print(f"[INFO] Semaphore created with key {KEY}")
except sysv_ipc.ExistentialError:
    sem = sysv_ipc.Semaphore(KEY)
    print(f"[INFO] Existing semaphore connected with key {KEY}")

# Fork into parent and child
pid = os.fork()

def critical_section(process_name, iteration):
    """Simulated critical section."""
    print(f"{process_name}: Trying to acquire semaphore (iteration {iteration})...")
    sem.acquire()  # equivalent to sem_wait
    print(f"{process_name}: Acquired semaphore (ENTER critical section).")

    # Critical section: only one process can be here at a time
    time.sleep(3)
    print(f"{process_name}: Leaving critical section (iteration {iteration}).")

    sem.release()  # equivalent to sem_post
    print(f"{process_name}: Released semaphore (EXIT critical section).")
    time.sleep(2)  # Let the other process get chance

if pid == 0:
    # Child process
    for i in range(3):
        critical_section("Child Process", i + 1)
    print("Child Process finished.")
else:
    # Parent process
    for i in range(3):
        critical_section("Parent Process", i + 1)
    print("Parent Process finished.")
    os.wait()  # wait for child to finish

    # Optional cleanup
    sem.remove()
    print("[INFO] Semaphore removed successfully.")
