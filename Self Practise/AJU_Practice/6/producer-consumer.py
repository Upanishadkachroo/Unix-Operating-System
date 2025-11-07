import threading
import time
import random
from queue import Queue

# Buffer size
BUFFER_SIZE = 5

# Shared buffer
buffer = Queue(BUFFER_SIZE)

# Semaphores
empty = threading.Semaphore(BUFFER_SIZE)   # Counts empty slots
full = threading.Semaphore(0)              # Counts filled slots
mutex = threading.Semaphore(1)             # Mutual exclusion lock

# Producer function
def producer():
    item_id = 1
    while item_id <= 10:  # produce 10 items
        time.sleep(random.uniform(0.5, 2))  # simulate time to produce
        item = f"Item-{item_id}"

        empty.acquire()      # wait if buffer full
        mutex.acquire()      # enter critical section

        buffer.put(item)
        print(f"[Producer] Produced {item} | Buffer size: {buffer.qsize()}")

        mutex.release()      # leave critical section
        full.release()       # signal that buffer has one more filled slot

        item_id += 1

    print("[Producer] Finished producing.")

# Consumer function
def consumer():
    for _ in range(10):  # consume 10 items
        full.acquire()       # wait if buffer empty
        mutex.acquire()      # enter critical section

        item = buffer.get()
        print(f"[Consumer] Consumed {item} | Buffer size: {buffer.qsize()}")

        mutex.release()      # leave critical section
        empty.release()      # signal that buffer has one more empty slot

        time.sleep(random.uniform(1, 2))  # simulate time to consume

    print("[Consumer] Finished consuming.")

# Create threads
producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)

# Start threads
producer_thread.start()
consumer_thread.start()

# Wait for both threads to finish
producer_thread.join()
consumer_thread.join()

print("\n[Main] Producer-Consumer simulation complete.")
