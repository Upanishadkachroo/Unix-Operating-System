from multiprocessing import Process, Semaphore, shared_memory
import time
import random

BUFFER_SIZE = 5  # max items in shared memory buffer

def producer(empty, full, mutex, shm_name):
    shm = shared_memory.SharedMemory(name=shm_name)
    buffer = shm.buf

    in_index = 0
    for item in range(1, 11):  # produce 10 items
        empty.acquire()        # wait for empty slot
        mutex.acquire()        # enter critical section

        # Produce an item (store in buffer)
        buffer[in_index] = item
        print(f"[Producer] Produced item {item} at index {in_index}")
        in_index = (in_index + 1) % BUFFER_SIZE

        mutex.release()        # leave critical section
        full.release()         # signal one filled slot
        time.sleep(random.uniform(0.5, 1.5))

    shm.close()


def consumer(empty, full, mutex, shm_name):
    shm = shared_memory.SharedMemory(name=shm_name)
    buffer = shm.buf

    out_index = 0
    for _ in range(10):  # consume 10 items
        full.acquire()         # wait for item
        mutex.acquire()        # enter critical section

        item = buffer[out_index]
        print(f"[Consumer] Consumed item {item} from index {out_index}")
        buffer[out_index] = 0  # clear slot
        out_index = (out_index + 1) % BUFFER_SIZE

        mutex.release()        # leave critical section
        empty.release()        # signal one empty slot
        time.sleep(random.uniform(0.8, 1.5))

    shm.close()


if __name__ == "__main__":
    # Create shared memory buffer (each slot holds 1 byte)
    shm = shared_memory.SharedMemory(create=True, size=BUFFER_SIZE, name="prod_cons_shm")

    # Create semaphores
    empty = Semaphore(BUFFER_SIZE)
    full = Semaphore(0)
    mutex = Semaphore(1)

    # Create producer and consumer processes
    p = Process(target=producer, args=(empty, full, mutex, shm.name))
    c = Process(target=consumer, args=(empty, full, mutex, shm.name))

    p.start()
    c.start()

    p.join()
    c.join()

    # Cleanup
    shm.close()
    shm.unlink()
    print("\n[Main] Shared memory cleaned up. Exiting.")
