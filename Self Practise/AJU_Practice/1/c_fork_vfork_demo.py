import os
import time

def demo_fork():
    print("\n=== Demonstrating fork() ===")
    pid = os.fork()
    if pid == 0:
        # Child process
        print(f"👶 Child Process: PID={os.getpid()}, Parent PID={os.getppid()}")
        message = "Child says: Hello!"
        print(message)
        time.sleep(2)
        print("👶 Child exiting...\n")
        os._exit(0)
    else:
        # Parent process
        print(f"🧠 Parent Process: PID={os.getpid()}, Created child PID={pid}")
        time.sleep(4)
        print("🧠 Parent continues independently.\n")

def demo_vfork_simulated():
    print("\n=== Simulated vfork() behavior ===")
    print("Note: Python does not support real vfork, this simulates 'suspend parent until exec'.")
    
    pid = os.fork()
    if pid == 0:
        # Simulate vfork behavior: child runs immediately
        print(f"👶 [vfork-child] PID={os.getpid()}, Parent PID={os.getppid()}")
        print("Child executing a new program using exec...")
        os.execlp("echo", "echo", "Hello from vfork-like child (exec replaces process!)")
    else:
        print(f"🧠 [Parent] PID={os.getpid()} waiting for child PID={pid}")
        os.waitpid(pid, 0)
        print("Parent resumes after child completes exec().\n")

if __name__ == "__main__":
    demo_fork()
    demo_vfork_simulated()
