import pickle
import time

with open("semaphore.pkl", "rb") as f:
    sem = pickle.load(f)

print("Performing P (wait) operation...")
sem.acquire()
print("Semaphore acquired! Critical section entered.")
time.sleep(3)
