import os
import multiprocessing
import time

def child_task():
    print(f"[Clone-like process] PID={os.getpid()}, Parent={os.getppid()}")
    time.sleep(2)
    print("[Clone-like process] Done.")

if __name__ == "__main__":
    print(f"[Parent] PID={os.getpid()}")

    # --- fork() example ---
    pid = os.fork()

    if pid == 0:
        # child process
        print(f"[Forked Child] PID={os.getpid()}, Parent={os.getppid()}")
    else:
        # parent process
        print(f"[Parent] Created child PID={pid}")
        os.wait()

    print("\nNow simulating clone() with multiprocessing (shared memory concept):")

    process = multiprocessing.Process(target=child_task)
    process.start()
    process.join()

    print("[Parent] All done.")
