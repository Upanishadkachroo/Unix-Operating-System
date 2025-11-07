import sysv_ipc

key = 3000
mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)

print("[Server] Waiting for messages (Ctrl+C to stop)...")

try:
    while True:
        message, priority = mq.receive()
        print(f"[Server] Received (Priority={priority}): {message.decode()}")
except KeyboardInterrupt:
    print("\n[Server] Exiting and cleaning up...")
    mq.remove()
