import threading

count = 0
COUNT_DONE = 10
COUNT_HALT1 = 3
COUNT_HALT2 = 6

lock = threading.Lock()
condition = threading.Condition(lock)

def functionCount1():
    global count
    while True:
        with condition:  
            condition.wait()  # like pthread_cond_wait
            count += 1
            print(f"functionCount1 count: {count}")
            if count >= COUNT_DONE:
                return

def functionCount2():
    global count
    while True:
        with condition:
            if count < COUNT_HALT1 or count > COUNT_HALT2:
                condition.notify()  # like pthread_cond_signal
            else:
                count += 1
                print(f"functionCount2 count: {count}")
            if count >= COUNT_DONE:
                return

t1 = threading.Thread(target=functionCount1)
t2 = threading.Thread(target=functionCount2)

t1.start()
t2.start()
t1.join()
t2.join()

print(f"Final count: {count}")

