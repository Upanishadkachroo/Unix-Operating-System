# long_running.py
import time
import os

print(f"Process ID (PID): {os.getpid()}")
print("Running... You can check memory usage in another terminal.")
print("Sleeping for 300 seconds (5 minutes)...")

time.sleep(300)

print("Done.")

