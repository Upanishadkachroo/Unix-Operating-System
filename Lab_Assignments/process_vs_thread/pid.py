import multiprocessing
import os

def multiplication(a, b):
    print(f"[Process PID: {os.getpid()}] Multiplication: {a} * {b} = {a * b}")

def division(a, b):
    print(f"[Process PID: {os.getpid()}] Division: {a} / {b} = {a / b}")

def process_arithmetic():
    print("\n--- Arithmetic using Processes ---")
    print(f"Main Process PID: {os.getpid()}")
    
    p1 = multiprocessing.Process(target=multiplication, args=(10, 5))
    p2 = multiprocessing.Process(target=division, args=(10, 5))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

if __name__ == "__main__":
    process_arithmetic()

