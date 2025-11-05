from multiprocessing import shared_memory
import time

def server():
    SHM_SIZE = 30  # bytes
    # Create shared memory segment
    shm = shared_memory.SharedMemory(create=True, size=SHM_SIZE, name="demo_shm")
    print(f"[Server] Shared memory created with name: {shm.name}")

    # Fill memory with lowercase a-z
    data = ''.join(chr(c) for c in range(ord('a'), ord('z') + 1))
    bytes_data = data.encode('utf-8')
    shm.buf[:len(bytes_data)] = bytes_data
    shm.buf[len(bytes_data)] = 0  # Null terminator like in C

    print(f"[Server] Wrote: {data}")
    print("[Server] Waiting for client to signal completion (writing '#')...")

    # Wait until client writes '#'
    while True:
        if shm.buf[0] == ord('#'):
            print("[Server] Client has signaled completion. Exiting...")
            break
        time.sleep(1)

    shm.close()
    shm.unlink()  # remove shared memory from system

if __name__ == "__main__":
    server()
