import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    msg = input("Enter message (or 'exit'): ")
    if msg == "exit":
        break
    client_socket.sendto(msg.encode(), ("127.0.0.1", 5001))
    data, _ = client_socket.recvfrom(1024)
    print("[CLIENT] From server:", data.decode())

client_socket.close()
