# process1.py
from multiprocessing import Queue
import time
import os

def process1(queue1, queue2):
    print(f"[Process 1 - PID {os.getpid()}] Starting conversation...")

    # Step 1: Send message to process 2
    msg1 = "Are you hearing me?"
    print(f"Process 1: {msg1}")
    queue1.put(msg1)

    # Step 2: Wait for reply from process 2
    reply = queue2.get()
    print(f"Process 2 replied: {reply}")

    # Step 3: Send final acknowledgment
    final_msg = "I can hear you too."
    print(f"Process 1: {final_msg}")
    queue1.put(final_msg)


if __name__ == "__main__":
    q1 = Queue()  # For messages from P1 → P2
    q2 = Queue()  # For messages from P2 → P1

    from multiprocessing import Process
    p1 = Process(target=process1, args=(q1, q2))
    from process2 import process2

    p2 = Process(target=process2, args=(q1, q2))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
