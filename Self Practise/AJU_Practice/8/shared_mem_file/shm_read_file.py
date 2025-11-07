# shm_read_file.py
from multiprocessing import shared_memory

def main():
    try:
        # Connect to existing shared memory
        shm = shared_memory.SharedMemory(name="file_shm")
    except FileNotFoundError:
        print("Shared memory segment not found! Start the writer first.")
        return

    # Read data until null byte (0)
    raw = bytes(shm.buf[:]).split(b'\x00', 1)[0]
    text = raw.decode()

    # Write the shared memory contents into a new file
    outfile = "output_from_shared.txt"
    with open(outfile, "w") as f:
        f.write(text)

    print(f"[Client] Read data from shared memory and saved to '{outfile}'.")

    # Cleanup
    shm.close()

if __name__ == "__main__":
    main()
