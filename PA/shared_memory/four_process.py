from multiprocessing import Process, Semaphore, shared_memory
import numpy as np
import time

# ------------------- Process 1: Writer -------------------
def writer(sem_write_done, arr_size=10):
    # Create shared memory for array and results
    shm = shared_memory.SharedMemory(create=True, size=1024, name="shared_mem")
    
    # Create random array
    data = np.random.randint(1, 100, arr_size, dtype=np.int32)
    print(f"[Writer] Generated array: {data.tolist()}")
    
    # Write array into shared memory
    shm_buf = np.ndarray((arr_size,), dtype=np.int32, buffer=shm.buf)
    shm_buf[:] = data[:]
    
    # Signal that writing is done
    sem_write_done.release()
    print("[Writer] Data written to shared memory.")
    
    shm.close()


# ------------------- Process 2: Sorter -------------------
def sorter(sem_write_done, sem_sort_done, arr_size=10):
    # Wait for writer to finish
    sem_write_done.acquire()
    
    shm = shared_memory.SharedMemory(name="shared_mem")
    shm_buf = np.ndarray((arr_size,), dtype=np.int32, buffer=shm.buf)
    
    print(f"[Sorter] Received array: {shm_buf.tolist()}")
    
    # Sort in-place
    sorted_arr = np.sort(shm_buf)
    shm_buf[:] = sorted_arr[:]
    
    print(f"[Sorter] Sorted array: {sorted_arr.tolist()}")
    
    # Signal sorting done
    sem_sort_done.release()
    
    shm.close()


# ------------------- Process 3: Statistics -------------------
def statistics(sem_sort_done, sem_stats_done, arr_size=10):
    # Wait for sorting to complete
    sem_sort_done.acquire()
    
    shm = shared_memory.SharedMemory(name="shared_mem")
    shm_buf = np.ndarray((arr_size,), dtype=np.int32, buffer=shm.buf)
    
    mean_val = np.mean(shm_buf)
    median_val = np.median(shm_buf)
    
    print(f"[Statistics] Mean = {mean_val:.2f}, Median = {median_val:.2f}")
    
    # Create shared memory for result storage
    res_shm = shared_memory.SharedMemory(create=True, size=64, name="result_mem")
    result_buf = np.ndarray((2,), dtype=np.float64, buffer=res_shm.buf)
    result_buf[0] = mean_val
    result_buf[1] = median_val
    
    # Signal that statistics are done
    sem_stats_done.release()
    
    shm.close()


# ------------------- Process 4: Display -------------------
def display(sem_stats_done):
    # Wait for stats to complete
    sem_stats_done.acquire()
    
    # Attach to both shared memories
    shm = shared_memory.SharedMemory(name="shared_mem")
    res_shm = shared_memory.SharedMemory(name="result_mem")
    
    arr_size = int(len(shm.buf) / 4)  # 4 bytes per int32
    shm_buf = np.ndarray((arr_size,), dtype=np.int32, buffer=shm.buf)
    result_buf = np.ndarray((2,), dtype=np.float64, buffer=res_shm.buf)
    
    print("\n========== FINAL OUTPUT ==========")
    print(f"Sorted Array : {shm_buf.tolist()}")
    print(f"Mean         : {result_buf[0]:.2f}")
    print(f"Median       : {result_buf[1]:.2f}")
    print("==================================\n")
    
    # Cleanup shared memory
    shm.close()
    shm.unlink()
    res_shm.close()
    res_shm.unlink()


# ------------------- Main Controller -------------------
if __name__ == "__main__":
    # Initialize semaphores (all locked initially)
    sem_write_done = Semaphore(0)
    sem_sort_done = Semaphore(0)
    sem_stats_done = Semaphore(0)
    
    arr_size = 10  # Size of array to process
    
    # Create processes
    p1 = Process(target=writer, args=(sem_write_done, arr_size))
    p2 = Process(target=sorter, args=(sem_write_done, sem_sort_done, arr_size))
    p3 = Process(target=statistics, args=(sem_sort_done, sem_stats_done, arr_size))
    p4 = Process(target=display, args=(sem_stats_done,))
    
    # Start all processes
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    
    # Wait for all to finish
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    
    print("[Main] All processes completed successfully.")
