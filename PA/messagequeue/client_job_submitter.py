import sysv_ipc
import random

job_key = 2001
result_key = 2002

job_queue = sysv_ipc.MessageQueue(job_key)
result_queue = sysv_ipc.MessageQueue(result_key)

client_id = str(random.randint(1000, 9999))
print(f"[Client {client_id}] Connected to Job Server")

while True:
    job_type = input("Enter job (factorial/fibonacci/prime) or 'exit': ").strip().lower()
    if job_type == "exit":
        job_queue.send(b"EXIT")
        break

    n = input("Enter number: ").strip()
    msg = f"{job_type} {n} {client_id}"
    job_queue.send(msg.encode())
    print(f"[Client {client_id}] Job sent: {msg}")

    # Wait for server response
    while True:
        result_msg, _ = result_queue.receive()
        result_msg = result_msg.decode()
        if result_msg.startswith(client_id):
            print("[Client] Result:", result_msg.split(":", 1)[1])
            break
