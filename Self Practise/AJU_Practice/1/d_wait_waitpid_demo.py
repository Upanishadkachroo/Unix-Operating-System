import os
import time
import random

def child_task(num):
    print(f"👶 Child {num}: PID={os.getpid()} started.")
    time.sleep(random.randint(1, 4))
    print(f"👶 Child {num}: exiting.")
    os._exit(num)  # Return exit status

def main():
    print(f"Parent PID: {os.getpid()}")
    children = []
    for i in range(3):
        pid = os.fork()
        if pid == 0:
            child_task(i + 1)
        else:
            children.append(pid)
            print(f"🧠 Parent created child PID={pid}")

    print("\n--- Using wait() ---")
    while True:
        try:
            pid, status = os.wait()
            print(f"✅ Collected child PID={pid} with exit code {os.WEXITSTATUS(status)}")
        except ChildProcessError:
            print("No more child processes.\n")
            break

    # Demonstrate waitpid (specific child)
    print("--- Using waitpid() ---")
    pid = os.fork()
    if pid == 0:
        print("👶 New Child (PID=", os.getpid(), ") sleeping 3s then exiting.")
        time.sleep(3)
        os._exit(7)
    else:
        print("🧠 Parent waiting specifically for PID=", pid)
        pid_done, status = os.waitpid(pid, 0)
        print(f"✅ Child PID={pid_done} exited with status={os.WEXITSTATUS(status)}")

if __name__ == "__main__":
    main()
