import sysv_ipc, threading

key1=1234
key2=4321

send_q=sysv_ipc.MessageQueue(key1, sysv_ipc.IPC_CREAT)
recv_q=sysv_ipc.MessageQueue(key2, sysv_ipc.IPC_CREAT)

def receiver():
    while True:
        message, t = recv_q.receive()
        print("\Freind:", message.decode())

threading.Thread(target=receiver, daemon=True).start()

while True:
    txt=input("You:")
    send_q.send(txt.encode())