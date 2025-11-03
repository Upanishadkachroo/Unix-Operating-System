import os, sys

fifo="/tmp/fifo"
if not os.path.exists(fifo):
    os.mkfifo(fifo)

with open(fifo, "r") as f:
    print("Waiting for messages..")
    for line in f:
        print("Received:", line.strip())