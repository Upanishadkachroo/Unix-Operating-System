import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 5000))
print(s.recv(1024).decode())
while True:
    msg = input("Enter message (or 'exit'): ")
    if msg == "exit":
        break
    s.sendall(msg.encode())
    print(s.recv(1024).decode())
s.close()
