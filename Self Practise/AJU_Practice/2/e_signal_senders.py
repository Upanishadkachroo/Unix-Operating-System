import os
import signal
import time

# 1️⃣ Define a handler to receive signals
def handler(signum, frame):
    print(f"📨 Process {os.getpid()} received signal {signum}")

signal.signal(signal.SIGUSR1, handler)

print(f"🆔 Current PID: {os.getpid()}")
time.sleep(1)

# --- 1. os.kill(pid, signal) ---
print("\n1️⃣ Using os.kill(pid, signal):")
os.kill(os.getpid(), signal.SIGUSR1)
time.sleep(1)

# --- 2. os.killpg(pgid, signal) ---
print("\n2️⃣ Using os.killpg(pgid, signal):")
os.setpgid(0, 0)  # ensure current process has a group
os.killpg(os.getpgrp(), signal.SIGUSR1)
time.sleep(1)

# --- 3. signal.raise_signal(signal) ---
print("\n3️⃣ Using signal.raise_signal(signal):")
signal.raise_signal(signal.SIGUSR1)
time.sleep(1)

# --- 4. Using os.system('kill -SIGUSR1 pid') ---
print("\n4️⃣ Using os.system('kill -SIGUSR1 pid'):")
os.system(f"kill -SIGUSR1 {os.getpid()}")
time.sleep(1)

# --- 5. Using subprocess call to 'kill' ---
print("\n5️⃣ Using subprocess to send signal:")
import subprocess
subprocess.run(["kill", "-SIGUSR1", str(os.getpid())])
time.sleep(1)

print("\n✅ All five signal-sending methods executed.")
