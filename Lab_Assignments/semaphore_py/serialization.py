import threading
import time

counter = 0
lock = threading.Lock()

def increment(name):
    global counter
    for _ in range(5):
        with lock:  # automatically acquire and release
            temp = counter
            print(f"{name} reads {temp}")
            time.sleep(0.1)
            counter = temp + 1
            print(f"{name} updates counter to {counter}")
        time.sleep(0.1)

t1 = threading.Thread(target=increment, args=("Thread-A",))
t2 = threading.Thread(target=increment, args=("Thread-B",))

t1.start()
t2.start()
t1.join()
t2.join()

print("Final Counter:", counter)

