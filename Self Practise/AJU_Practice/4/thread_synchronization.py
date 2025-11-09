import threading
import time
import random

# Shared resource
shared_counter = 0

# Semaphore to limit concurrent access
sem = threading.Semaphore(1)  # acts like a monitor lock

def increment(name):
    global shared_counter
    for _ in range(5):
        sem.acquire()  # enter critical section
        local_copy = shared_counter
        print(f"{name} entering critical section. Current value = {local_copy}")
        time.sleep(random.uniform(0.1, 0.5))
        local_copy += 1
        shared_counter = local_copy
        print(f"{name} updated counter to {shared_counter}")
        sem.release()  # exit critical section
        time.sleep(random.uniform(0.1, 0.5))

if __name__ == "__main__":
    t1 = threading.Thread(target=increment, args=("Thread-A",))
    t2 = threading.Thread(target=increment, args=("Thread-B",))
    t3 = threading.Thread(target=increment, args=("Thread-C",))

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    print("\nFinal counter value:", shared_counter)
