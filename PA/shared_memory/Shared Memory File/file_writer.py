from multiprocessing import shared_memory, Semaphore
import time
import os

def writer(input_file, chunk_size=512):
    sem_empty = Semaphore(1)  # Start with memory empty
    sem_full = Semaphore(0)

    shm = shared_memory.SharedMemory(create=True, size=chunk_size + 10, name="file_shm")
    shm.buf[0] = 0  # first byte indicates end-of-file flag (0 = more data, 1 = EOF)

    print(f"[Writer] Shared memory created with name '{shm.name}'")
    print(f"[Writer] Reading from file: {input_file}")

    with open(input_file, "rb") as f:
        while True:
            sem_empty.acquire()

            data = f.read(chunk_size)
            if not data:
                shm.buf[0] = 1  # EOF signal
                sem_full.release()
                break

            # Store data into shared memory (after first byte)
            shm.buf[0] = 0  # not EOF
            shm.buf[1:1 + len(data)] = data

            print(f"[Writer] Wrote {len(data)} bytes into shared memory.")
            sem_full.release()  # signal reader
            time.sleep(0.1)

    print("[Writer] File transfer complete. Cleaning up.")
    shm.close()
    shm.unlink()


if __name__ == "__main__":
    writer("input.txt")

