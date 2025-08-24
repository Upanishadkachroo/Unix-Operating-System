from  threading import Thread, Semaphore
import time

obj=Semaphore(3)

def display(args):
    obj.acquire()

    for i in range(5):
        print('Hello')
        time.sleep(1)
        print(args)
        obj.release()

    #obj.release()


t1=Thread(target=display, args=('Threads-1',))
t2=Thread(target=display, args=('Threads-2',))
t3=Thread(target=display, args=('Threads-3',))
t4=Thread(target=display, args=('Threads-3',))
t5=Thread(target=display, args=('Threads-3',))
t6=Thread(target=display, args=('Threads-3',))



t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()

