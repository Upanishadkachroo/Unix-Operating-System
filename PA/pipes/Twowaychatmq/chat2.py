import sysv_ipc, threading

key1 = 1111
key2 = 2222
send_q = sysv_ipc.MessageQueue(key2, sysv_ipc.IPC_CREAT)
recv_q = sysv_ipc.MessageQueue(key1, sysv_ipc.IPC_CREAT)

def receiver():
    while True:
        msg, _ = recv_q.receive()
        print("\nFriend:", msg.decode())

threading.Thread(target=receiver, daemon=True).start()

while True:
    text = input("You: ")
    send_q.send(text.encode())
