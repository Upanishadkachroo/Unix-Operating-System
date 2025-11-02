import os

FIFO_PATH = "/tmp/myfifo"

with open(FIFO_PATH, "w") as fifo:
    fifo.write("Hello from client!\n")
    fifo.flush()

