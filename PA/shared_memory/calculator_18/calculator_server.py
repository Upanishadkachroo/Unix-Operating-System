from multiprocessing import shared_memory
import time

def calculator():
    shm = shared_memory.SharedMemory(create=True, size=100, name="calc_shm")
    buf = shm.buf

    print("[Server] Shared memory created: calc_shm")
    print("[Server] Waiting for client requests...")

    while True:
        flag = buf[0]
        if flag == 1:  # request ready
            # Read the expression (bytes until null)
            expr_bytes = bytes(buf[1:50]).split(b'\x00', 1)[0]
            expr = expr_bytes.decode()

            if expr.strip().lower() == "exit":
                print("[Server] Exit signal received. Shutting down...")
                break

            print(f"[Server] Received expression: {expr}")

            try:
                result = str(eval(expr))  # perform calculation
            except Exception as e:
                result = f"Error: {e}"

            # Write result to shared memory (starting at index 51)
            result_bytes = result.encode()
            buf[51:51+len(result_bytes)] = result_bytes
            buf[51+len(result_bytes)] = 0

            # Set flag = 2 (result ready)
            buf[0] = 2
            print(f"[Server] Computed result: {result}")

        time.sleep(0.5)

    shm.close()
    shm.unlink()
    print("[Server] Shared memory removed. Exiting.")

if __name__ == "__main__":
    calculator()
