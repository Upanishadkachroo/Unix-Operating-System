import signal
import sys
import time

def handler(signum, frame):
    print("\n⏰ Time is up! You didn’t respond in 10 seconds.")
    sys.exit(1)

# Register signal handler for SIGALRM
signal.signal(signal.SIGALRM, handler)

# Set alarm for 10 seconds
signal.alarm(10)

try:
    user_input = input("Enter your name within 10 seconds: ")
    # Cancel alarm if input received
    signal.alarm(0)
    print(f"✅ Hello, {user_input}!")
except Exception as e:
    print("Error:", e)
