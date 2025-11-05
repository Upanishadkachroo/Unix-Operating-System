from multiprocessing import shared_memory, Semaphore
import time

def client():
    # Connect to existing shared memory and semaphores
    try:
        shm = shared_memory.SharedMemory(name="shm_demo")
    except FileNotFoundError:
        print("[Client] Shared memory not found. Start server first.")
        return

    sem_empty = Semaphore(0)
    sem_full = Semaphore(0)

    messages = ["Hello from Client", "Goodbye from Client"]

    for msg in messages:
        # Write message
        shm.buf[:len(msg)] = msg.encode()
        shm.buf[len(msg)] = 0
        print(f"[Client] Wrote: {msg}")

        # Signal server
        sem_empty.release()

        # Wait for server to read it
        sem_full.acquire()
        time.sleep(1)

    shm.close()
    print("[Client] Communication complete.")

if __name__ == "__main__":
    time.sleep(1)
    client()
