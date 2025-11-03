import socket
import threading

def handle_msg(data, addr, s):
    print(f"[THREAD] Handling message from {addr}")
    s.sendto(data, addr)  # Echo back

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1', 5051))
print("[SERVER] UDP Concurrent Echo Server started...")

while True:
    data, addr = s.recvfrom(1024)
    threading.Thread(target=handle_msg, args=(data, addr, s)).start()
