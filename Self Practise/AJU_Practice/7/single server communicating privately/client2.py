import sysv_ipc

key = 1234
client_id = 2  # unique for each client

queue = sysv_ipc.MessageQueue(key)
print(f"Client {client_id} connected to message queue.")

msg = "Hello from Client 2!"
queue.send(msg.encode(), type=client_id)
print(f"Client {client_id} sent: {msg}")

reply, _ = queue.receive(type=client_id + 100)
print(f"Client {client_id} received reply: {reply.decode()}")
