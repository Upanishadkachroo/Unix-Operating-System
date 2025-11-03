import os, sys, time

fifo="/tmp/myfifo"
if not os.path.exits(fifo):
    os.mkfifo(fifo)

with open(fifo, "w") as f:
    while True:
        msg=input("ENter the message")
        if msg=="exit":
            break
        f.write(msg+"\n")
        f.flush()