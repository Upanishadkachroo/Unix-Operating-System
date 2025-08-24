import sysv_ipc

key=5678

#get the same message
mq=sysv_ipc.MessageQueue(key)

#recieve message from process 1
msg, mtype=mq.receive(type=1)
print("process 2: recieved ->", msg.decode())

#reply to process 1
reply="loud and clear"
mq.send(reply.encode(), type=2)
print("process 2: sent ->",reply)
