import sysv_ipc
import time

# Shared key (same for all processes)
key = 1234

# Create (or get existing) message queue
queue = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREX, mode=0o666)
print("Server: Message queue created with key", key)

try:
    while True:
        # Wait for message from any client
        msg, mtype = queue.receive(block=True)
        msg = msg.decode()

        print(f"Server received from Client {mtype}: {msg}")

        # Prepare reply — use unique reply type = mtype + 100
        reply = f"Hello Client {mtype}, I received your message!"
        queue.send(reply.encode(), type=mtype + 100)

except KeyboardInterrupt:
    print("\nServer shutting down. Removing message queue...")
    queue.remove()
    print("Queue removed successfully.")

