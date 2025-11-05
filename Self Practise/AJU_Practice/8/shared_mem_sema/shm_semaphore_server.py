from multiprocessing import shared_memory, Semaphore
import time, os, sys

def server():
    BUF_SIZE=100

    # Create shared memory and semaphores
    shm = shared_memory.SharedMemory(create=True, size=BUF_SIZE, name="shm_demo")
    sem_empty = Semaphore(0)  # Initially no message (client will release this)
    sem_full = Semaphore(0)   # Initially nothing to read

    print("[Server] Shared memory created:", shm.name)
    print("[Server] Waiting for client messages...")

    for _ in range(2):  # Expect two messages
        sem_empty.acquire()


        raw = bytes(shm.buf[:BUF_SIZE]).split(b'\x00', 1)[0]
        message = raw.decode()
        print("[Server] Received:", message)

        sem_full.release()
        time.sleep(1)

    # Cleanup
    shm.close()
    shm.unlink()
    print("[Server] Memory released and exiting.")


if __name__ == "__main__":
    server()