from multiprocessing import shared_memory

def reader():
    try:
        # Connect to existing shared memory
        shm = shared_memory.SharedMemory(name="shm_example")
    except FileNotFoundError:
        print("Shared memory not found. Run writer first.")
        return

    # Read the string
    data = bytes(shm.buf[:]).split(b'\x00', 1)[0].decode()
    print("Data read from shared memory:", data)

    # Cleanup
    shm.close()

if __name__ == "__main__":
    reader()
