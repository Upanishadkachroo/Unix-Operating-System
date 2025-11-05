# shm_write_file.py
import sys
from multiprocessing import shared_memory

def main():
    if len(sys.argv) != 2:
        print("Usage: python shm_write_file.py <filename>")
        sys.exit(1)

    infile = sys.argv[1]
    
    # Read the file content
    with open(infile, "r") as f:
        data = f.read()

    # Create shared memory segment
    shm = shared_memory.SharedMemory(create=True, size=len(data) + 1, name="file_shm")

    # Write data into shared memory buffer
    shm.buf[:len(data)] = data.encode()
    shm.buf[len(data)] = 0  # Null terminator
    print(f"[Server] Wrote file '{infile}' ({len(data)} bytes) to shared memory.")

    print("[Server] Waiting for client to finish reading...")
    input("Press ENTER after client has finished reading...")

    # Cleanup
    shm.close()
    shm.unlink()
    print("[Server] Shared memory released.")

if __name__ == "__main__":
    main()
