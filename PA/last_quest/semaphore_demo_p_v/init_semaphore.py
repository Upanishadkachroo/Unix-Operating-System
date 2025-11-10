from multiprocessing import Semaphore
import pickle

sem = Semaphore(1)
# Save the semaphore state (for demo purpose)
with open("semaphore.pkl", "wb") as f:
    pickle.dump(sem, f)
print("Semaphore initialized and saved as semaphore.pkl")
