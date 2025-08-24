import sysv_ipc
import time

key=5678

#create a message queue
mq=sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)

#send message to process 2
mssg="are u hearing me?"
mq.send(mssg.encode(), type=1) #means message for process 2
print("process 1: send->", mssg)

#wait reply
reply, mtype=mq.receive(type=2) #means expecting reply
print("prcess 1: recieved -> ", reply.decode())

#confirmation
print("process 1, i can hear you")
