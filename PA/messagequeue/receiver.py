import sysv_ipc

# Connect to the existing message queue
key = 1234
mq = sysv_ipc.MessageQueue(key)

# Receive message
message, t = mq.receive()
print(f"[Receiver] Received message: {message.decode()}")

# Cleanup (optional)
mq.remove()
