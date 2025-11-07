import sysv_ipc

key = 5000
mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)

numbers = [10, 20, 30, 40, 50]
print(f"[Sender] Sending numbers: {numbers}")

for num in numbers:
    mq.send(str(num).encode())

# Send a termination message
mq.send(b"END")
