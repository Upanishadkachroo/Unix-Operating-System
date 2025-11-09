import threading
import time
import random

shared_value = 0
lock = threading.Lock()  # acts like monitor/serialize

def task(name):
    global shared_value
    for _ in range(3):
        with lock:  # monitor enter (synchronized block)
            old_value = shared_value
            print(f"{name} inside critical section. Value = {old_value}")
            time.sleep(random.uniform(0.1, 0.4))
            shared_value = old_value + 1
            print(f"{name} updated value to {shared_value}")
        time.sleep(random.uniform(0.2, 0.5))

if __name__ == "__main__":
    threads = [threading.Thread(target=task, args=(f"Thread-{i}",)) for i in range(3)]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("\nFinal shared value:", shared_value)
