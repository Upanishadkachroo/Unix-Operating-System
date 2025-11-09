import threading
import time

def print_even():
    for i in range(2, 21, 2):
        print(f"Even: {i}")
        time.sleep(0.5)

def print_odd():
    for i in range(1, 20, 2):
        print(f"Odd: {i}")
        time.sleep(0.5)

def print_prime():
    def is_prime(n):
        if n < 2:
            return False
        for j in range(2, int(n ** 0.5) + 1):
            if n % j == 0:
                return False
        return True

    for i in range(2, 21):
        if is_prime(i):
            print(f"Prime: {i}")
        time.sleep(0.5)

if __name__ == "__main__":
    t1 = threading.Thread(target=print_even)
    t2 = threading.Thread(target=print_odd)
    t3 = threading.Thread(target=print_prime)

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    print("\nAll threads finished execution.")
