import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 5050))
print("Connected to server.")

while True:
    msg = input("You: ")
    if msg == "exit":
        break
    s.sendall(msg.encode())
    data = s.recv(1024)
    print("Echo:", data.decode())

s.close()
