import sysv_ipc
import math

# Create two message queues
# One for receiving jobs, one for sending results
job_key = 2001
result_key = 2002

job_queue = sysv_ipc.MessageQueue(job_key, sysv_ipc.IPC_CREAT)
result_queue = sysv_ipc.MessageQueue(result_key, sysv_ipc.IPC_CREAT)

print("[Server] Job Scheduler is running...")

def factorial(n):
    return math.factorial(n)

def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

while True:
    msg, _ = job_queue.receive()
    msg = msg.decode()

    if msg == "EXIT":
        print("[Server] Shutting down...")
        break

    # Expected format: "JOB_TYPE NUMBER CLIENT_ID"
    parts = msg.split()
    if len(parts) != 3:
        continue

    job_type, num_str, client_id = parts
    n = int(num_str)
    result = ""

    if job_type == "factorial":
        result = f"Factorial({n}) = {factorial(n)}"
    elif job_type == "fibonacci":
        result = f"Fibonacci({n}) = {fibonacci(n)}"
    elif job_type == "prime":
        result = f"{n} is {'prime' if is_prime(n) else 'not prime'}"
    else:
        result = "Unknown job type"

    print(f"[Server] Processed: {msg} → {result}")
    result_queue.send(f"{client_id}:{result}".encode())

# Cleanup
job_queue.remove()
result_queue.remove()
