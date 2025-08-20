import threading
import time

def worker():
    print("Hello from thread")

def print_messg(messg):
    print(messg)
    time.sleep(1)


t=threading.Thread(target=worker) # like p_thread t;
t.start() #like pthread_create
t.join() #like pthread_join

#def print_messg(messg):
 #   print(messg)
  #  time.sleep(1)

thread1=threading.Thread(target=print_messg, args=("Thread 1",))
thread2=threading.Thread(target=print_messg, args=("Thread 2",))

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print("both threads finished")


