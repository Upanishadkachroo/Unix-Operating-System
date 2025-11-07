from multiprocessing import shared_memory

def writer():
    # Create shared memory block of 1024 bytes
    shm = shared_memory.SharedMemory(create=True, size=1024, name="shm_example")

    # Get input from user
    data = input("Enter a string to write into shared memory: ")

    # Write data
    shm.buf[:len(data)] = data.encode()
    shm.buf[len(data)] = 0  # Null terminator

    print("Data written to shared memory.")
    input("Press Enter after running reader...")

    # Cleanup
    shm.close()
    shm.unlink()  # remove from system

if __name__ == "__main__":
    writer()
