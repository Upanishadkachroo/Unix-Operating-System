import os, sysv_ipc, time

key=1234

mq=sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)

print("enter number separated by space")
nums=input("Numbers: ").split()

for n in nums:
    mq.send(n.encode())
    print(f"Sent: {n}")
    time.sleep(0.5)

mq.send(b"exit")
print("all numbers sent, exiting")