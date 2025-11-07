from multiprocessing import shared_memory, Semaphore
import time

def reader(output_file, chunk_size=512):
    sem_empty = Semaphore(1)
    sem_full = Semaphore(0)

    try:
        shm = shared_memory.SharedMemory(name="file_shm")
    except FileNotFoundError:
        print("[Reader] Shared memory not found. Run writer first.")
        return

    print(f"[Reader] Connected to shared memory '{shm.name}'")
    print(f"[Reader] Writing output to: {output_file}")

    with open(output_file, "wb") as f:
        while True:
            sem_full.acquire()

            eof_flag = shm.buf[0]
            if eof_flag == 1:
                sem_empty.release()
                print("[Reader] End of file reached.")
                break

            data = bytes(shm.buf[1:1 + chunk_size]).rstrip(b'\x00')
            f.write(data)
            print(f"[Reader] Read and wrote {len(data)} bytes to output file.")

            sem_empty.release()
            time.sleep(0.1)

    shm.close()
    print("[Reader] File reconstruction complete.")


if __name__ == "__main__":
    time.sleep(1)
    reader("output.txt")
