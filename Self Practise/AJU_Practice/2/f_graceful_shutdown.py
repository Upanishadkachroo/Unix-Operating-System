import signal
import time
import sys

running = True

def graceful_exit(signum, frame):
    global running
    print(f"\n🛑 Received signal {signum} (SIGTERM). Cleaning up before exit...")
    running = False

# Catch termination signals
signal.signal(signal.SIGTERM, graceful_exit)
signal.signal(signal.SIGINT, graceful_exit)  # handle Ctrl+C as well

print("🚀 Service running. Send SIGTERM or press Ctrl+C to stop gracefully.\n")

while running:
    print("🟢 Working...")
    time.sleep(2)

print("✅ Cleanup complete. Exiting gracefully.")
sys.exit(0)

# python3 f_graceful_shutdown.py &
# kill -SIGTERM <pid>
