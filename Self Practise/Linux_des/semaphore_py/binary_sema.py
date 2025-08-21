import threading
import time

#counting_semaphore=threading.Semaphore(3)
binary_semaphore=threading.Semaphore(1)

def task(args):
    print(f'{args} has enetered critical section')
    binary_semaphore.acquire()

    try:
        print(f'{args} has eneterd critical section')
        time.sleep(1)
        print(f'{args} has left critical section')
    finally:
        binary_semaphore.release()


#Multiple threads creation
threads=[]
for i in range(5):
    t=threading.Thread(target=task, args=(f'Threads-{i+1}',))
    threads.append(t)
    t.start()

for t in threads:
    t.join()               
