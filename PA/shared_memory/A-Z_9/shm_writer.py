from multiprocessing import shared_memory
import string
import time

def writer():
    # Create shared memory segment
    shm = shared_memory.SharedMemory(create=True, size=100, name="shm_alpha")
    print("[Writer] Shared memory created:", shm.name)

    # Write A–Z characters into shared memory
    data = string.ascii_uppercase  # 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    shm.buf[:len(data)] = data.encode('utf-8')
    shm.buf[len(data)] = 0  # Null terminator

    print(f"[Writer] Wrote data to shared memory: {data}")
    print("[Writer] Waiting for reader to read (press Ctrl+C to exit when done)...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[Writer] Cleaning up shared memory.")
        shm.close()
        shm.unlink()

if __name__ == "__main__":
    writer()
