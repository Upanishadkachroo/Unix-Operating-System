import threading

# Initialize semaphore with 0 so f1 waits initially
sem = threading.Semaphore(0)

def f1():
    sem.acquire()  # Wait until f2 releases
    print("Function f1 is executing AFTER f2.")

def f2():
    print("Function f2 is executing FIRST.")
    sem.release()  # Signal f1 to proceed

if __name__ == "__main__":
    t1 = threading.Thread(target=f1)
    t2 = threading.Thread(target=f2)

    # Start in reverse order to show synchronization works
    t1.start()
    t2.start()

    t1.join()
    t2.join()
