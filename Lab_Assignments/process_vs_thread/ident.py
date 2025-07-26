import threading
import os

def addition(a, b):
    print(f"[Thread ID: {threading.get_ident()} | PID: {os.getpid()}] Addition: {a} + {b} = {a + b}")

def subtraction(a, b):
    print(f"[Thread ID: {threading.get_ident()} | PID: {os.getpid()}] Subtraction: {a} - {b} = {a - b}")

def thread_arithmetic():
    print("\n--- Arithmetic using Threads ---")
    print(f"Main Thread PID: {os.getpid()} | Thread ID: {threading.get_ident()}")
    
    t1 = threading.Thread(target=addition, args=(10, 5))
    t2 = threading.Thread(target=subtraction, args=(10, 5))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

thread_arithmetic()

