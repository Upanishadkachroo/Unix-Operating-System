import threading
import time

class MonitorCounter:
    def __init__(self):
        self.counter = 0
        self.lock = threading.Lock()

    def increment(self, name):
        with self.lock:
            temp = self.counter
            print(f"{name} reads {temp}")
            time.sleep(0.1)
            self.counter = temp + 1
            print(f"{name} updates counter to {self.counter}")

monitor = MonitorCounter()

def task(name):
    for _ in range(5):
        monitor.increment(name)
        time.sleep(0.1)

t1 = threading.Thread(target=task, args=("Thread-X",))
t2 = threading.Thread(target=task, args=("Thread-Y",))

t1.start()
t2.start()
t1.join()
t2.join()

print("Final Counter:", monitor.counter)

