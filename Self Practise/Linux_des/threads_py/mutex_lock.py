import threading
import time

cnt=0
lock=threading.Lock()

def functionc():
    global cnt
    with lock: # accquires lock automatically
        cnt+=1
        print(f"counter value: {cnt}")

t1=threading.Thread(target=functionc)
t2=threading.Thread(target=functionc)

threads = []

for i in range(10):
    t = threading.Thread(target=functionc)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"Final counter value: {cnt}")


t1.start()
t2.start()

t1.join()
t2.join()

