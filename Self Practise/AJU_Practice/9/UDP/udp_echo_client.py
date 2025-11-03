import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    msg = input("You: ")
    if msg == "exit":
        break
    s.sendto(msg.encode(), ('127.0.0.1', 5051))
    data, _ = s.recvfrom(1024)
    print("Echo:", data.decode())

s.close()
