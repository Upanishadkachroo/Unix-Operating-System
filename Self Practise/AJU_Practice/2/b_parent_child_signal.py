import os
import signal
import time

# Define handler for both parent and child
def handler(signum, frame):
    print(f"Process {os.getpid()} received signal {signum}")

# Register handler
signal.signal(signal.SIGUSR1, handler)
signal.signal(signal.SIGUSR2, handler)

pid = os.fork()

if pid == 0:
    # Child process
    time.sleep(2)
    print(f"Child (PID {os.getpid()}) sending SIGUSR1 to parent ({os.getppid()})")
    os.kill(os.getppid(), signal.SIGUSR1)
    time.sleep(1)
    print("Child done.")
else:
    # Parent process
    print(f"Parent PID: {os.getpid()}, Child PID: {pid}")
    time.sleep(5)
    print(f"Parent sending SIGUSR2 to child ({pid})")
    os.kill(pid, signal.SIGUSR2)
    os.wait()
    print("Parent done.")
