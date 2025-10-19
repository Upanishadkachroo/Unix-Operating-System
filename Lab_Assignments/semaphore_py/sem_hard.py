import threading

# Create a semaphore initialized to 0
sem = threading.Semaphore(0)

def f1():
    # Wait until f2() releases the semaphore
    sem.acquire()
    print("Function f1 is executing after f2")

def f2():
    print("Function f2 is executing first")
    # Signal that f2 has finished
    sem.release()

# Create threads
t1 = threading.Thread(target=f1)
t2 = threading.Thread(target=f2)

# Start threads (in any order)
t1.start()
t2.start()

# Wait for both threads to finish
t1.join()
t2.join()

