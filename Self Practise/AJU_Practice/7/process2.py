# process2.py
import time
import os

def process2(queue1, queue2):
    print(f"[Process 2 - PID {os.getpid()}] Ready to receive message...")

    # Step 1: Wait for Process 1 message
    msg = queue1.get()
    print(f"Process 2 received: {msg}")

    # Step 2: Reply
    reply = "Loud and Clear."
    print(f"Process 2: {reply}")
    queue2.put(reply)

    # Step 3: Receive acknowledgment
    final_msg = queue1.get()
    print(f"Process 2 received final message: {final_msg}")
