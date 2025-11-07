import sysv_ipc
import time

key = 1234
client_id = 1  # unique for each client

queue = sysv_ipc.MessageQueue(key)
print(f"Client {client_id} connected to message queue.")

# Send a message to the server
msg = "Hello from Client 1!"
queue.send(msg.encode(), type=client_id)
print(f"Client {client_id} sent: {msg}")

# Wait for reply (server replies with type = client_id + 100)
reply, _ = queue.receive(type=client_id + 100)
print(f"Client {client_id} received reply: {reply.decode()}")
