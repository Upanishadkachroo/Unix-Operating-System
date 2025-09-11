import socket
host='127.0.0.1'
port=8000

server=socket.socket()
server.bind((host, port))

server.listen()

conn, addr=server.accept()
print("connection from "+ str(addr))

while(True):
    data=conn.recv(1024).decode()
    if not data:
        break
    data=str(data).upper()
    print("from client "+ str(data))
    data=input("type message")
    conn.send(data.encode())
conn.close()

