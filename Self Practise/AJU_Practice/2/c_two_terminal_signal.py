import os
import signal
import time

def handler(signum, frame):
    print(f"\n📩 Signal {signum} received from another process!")

# Register a handler for SIGUSR1
signal.signal(signal.SIGUSR1, handler)

print(f"🔢 Current PID: {os.getpid()}")
print("📖 To send a signal from another terminal, run:")
print(f"    kill -SIGUSR1 {os.getpid()}")
print("Now waiting for signal... (Press Ctrl+C to exit)\n")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n👋 Exiting program.")
