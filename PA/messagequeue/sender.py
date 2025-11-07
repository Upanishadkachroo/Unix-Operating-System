import sysv_ipc

# Create or get message queue with key 1234
key = 1234
mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)

# Message to send
message = "Hello from Process 1!"
mq.send(message.encode())

print(f"[Sender] Sent message: {message}")
