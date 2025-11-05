from multiprocessing import shared_memory
import time

def client():
    try:
        # Connect to existing shared memory
        shm = shared_memory.SharedMemory(name="demo_shm")
        print("[Client] Connected to shared memory")
    except FileNotFoundError:
        print("[Client] Shared memory not found. Start the server first.")
        return

    # Read characters until null byte (0)
    raw_bytes = bytes()
    for b in shm.buf:
        if b == 0:
            break
        raw_bytes += bytes([b])

    text = raw_bytes.decode('utf-8')
    print(f"[Client] Read from shared memory: {text}")

    # Write '#' to indicate done
    shm.buf[0] = ord('#')
    print("[Client] Signaled completion ('#')")

    shm.close()

if __name__ == "__main__":
    time.sleep(2)  # slight delay to ensure server is ready
    client()
