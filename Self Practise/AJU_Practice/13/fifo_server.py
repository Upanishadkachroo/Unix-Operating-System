import os

FIFO_PATH = "/tmp/myfifo"

# Create FIFO if it doesn't exist
if not os.path.exists(FIFO_PATH):
    os.mkfifo(FIFO_PATH)

print("Server waiting for data...")
with open(FIFO_PATH, "r") as fifo:
    while True:
        data = fifo.readline().strip()
        if not data:
            break
        print(f"Server received: {data}")

