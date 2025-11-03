import sysv_ipc

key=1234
mq=sysv_ipc.MessageQueue(key)

total=0

print("receiver started")

while True:
    message, t = mq.receive()
    num_str=message.decode().strip()

    if num_str=="exit":
        break
    else:
        try:
            num=int(num_str)
            total+=num
            print(f"Received: {num}, Current Sum: {total}")
        except ValueError:
            print(f"Invalid number received: {num_str}")

print("Final Sum:", total)  
mq.remove()