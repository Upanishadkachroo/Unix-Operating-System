from multiprocessing import shared_memory

def reader():
    try:
        # Connect to existing shared memory
        shm = shared_memory.SharedMemory(name="shm_alpha")
        print("[Reader] Connected to shared memory.")
    except FileNotFoundError:
        print("[Reader] Shared memory not found. Run writer first.")
        return

    # Read data until null byte (0)
    raw = bytes(shm.buf[:]).split(b'\x00', 1)[0]
    text = raw.decode('utf-8')

    print(f"[Reader] Read data: {text}")

    # Write data to file
    with open("output.txt", "w") as f:
        f.write(text)
    print("[Reader] Data written to 'output.txt'.")

    shm.close()

if __name__ == "__main__":
    reader()
