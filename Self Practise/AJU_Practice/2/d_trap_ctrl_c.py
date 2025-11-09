import signal
import time

def handler(signum, frame):
    print("\n⚠️  Ctrl+C (SIGINT) detected — but I will not quit! Press Ctrl+Z to stop me manually.")

# Override SIGINT behavior
signal.signal(signal.SIGINT, handler)

print("🔁 Running... Press Ctrl+C to test. (Press Ctrl+Z to stop forcefully)\n")

while True:
    print("🟢 Working...")
    time.sleep(3)
