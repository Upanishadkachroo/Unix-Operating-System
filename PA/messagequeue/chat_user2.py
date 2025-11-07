import sysv_ipc

key_send = 2222  # This process sends on 2222
key_recv = 1111  # Receives from 1111

mq_send = sysv_ipc.MessageQueue(key_send, sysv_ipc.IPC_CREAT)
mq_recv = sysv_ipc.MessageQueue(key_recv, sysv_ipc.IPC_CREAT)

print("User2 Chat started (type 'exit' to quit)")
while True:
    print("Waiting for message...")
    message, t = mq_recv.receive()
    text = message.decode()
    print("User1:", text)

    if text.lower() == "exit":
        break

    msg = input("You: ")
    mq_send.send(msg.encode())

    if msg.lower() == "exit":
        break
