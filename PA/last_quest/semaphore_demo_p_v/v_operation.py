import pickle

with open("semaphore.pkl", "rb") as f:
    sem = pickle.load(f)

sem.release()
print("Semaphore released! Other process can now enter.")


# mkdir semaphore_demo
# cd semaphore_demo
# python3 init_semaphore.py
# python3 p_operation.py &  # Simulate process waiting
# python3 v_operation.py    # Then release
