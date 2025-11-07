import sysv_ipc
import time

key_send = 1111   # Queue to send messages
key_recv = 2222   # Queue to receive messages

# Create both queues
mq_send = sysv_ipc.MessageQueue(key_send, sysv_ipc.IPC_CREAT)
mq_recv = sysv_ipc.MessageQueue(key_recv, sysv_ipc.IPC_CREAT)

print("User1 Chat started (type 'exit' to quit)")
while True:
    msg = input("You: ")
    mq_send.send(msg.encode())

    if msg.lower() == "exit":
        break

    print("Waiting for reply...")
    message, t = mq_recv.receive()
    print("User2:", message.decode())

# Clean up
mq_send.remove()
mq_recv.remove()
