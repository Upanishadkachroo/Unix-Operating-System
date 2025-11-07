from multiprocessing import shared_memory
import time

def client():
    try:
        shm = shared_memory.SharedMemory(name="calc_shm")
    except FileNotFoundError:
        print("[Client] Shared memory not found. Start server first.")
        return

    buf = shm.buf

    while True:
        expr = input("Enter expression (e.g., 3 + 4) or 'exit' to quit: ")

        # Write expression to shared memory
        expr_bytes = expr.encode()
        buf[1:1+len(expr_bytes)] = expr_bytes
        buf[1+len(expr_bytes)] = 0

        # Set flag = 1 (request ready)
        buf[0] = 1

        if expr.strip().lower() == "exit":
            break

        # Wait for server to compute result
        while buf[0] != 2:
            time.sleep(0.2)

        # Read result from shared memory (starts at index 51)
        result_bytes = bytes(buf[51:100]).split(b'\x00', 1)[0]
        result = result_bytes.decode()
        print(f"[Client] Result: {result}")

        # Reset flag = 0 (ready for next input)
        buf[0] = 0

    shm.close()
    print("[Client] Exiting.")

if __name__ == "__main__":
    time.sleep(1)
    client()
