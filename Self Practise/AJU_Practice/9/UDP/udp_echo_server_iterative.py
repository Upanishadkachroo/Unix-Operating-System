import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1', 5051))
print("[SERVER] UDP Iterative Echo Server started...")

while True:
    data, addr = s.recvfrom(1024)
    print(f"[SERVER] From {addr}: {data.decode()}")
    s.sendto(data, addr)  # Echo back
