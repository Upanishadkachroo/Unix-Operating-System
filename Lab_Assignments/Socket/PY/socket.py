import socket

host='127.0.0.1'
port=8080

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #by default af_inet, sock_stream(tcp), 0
server.bind((host, port))
server.listen()
client, addr=server.accept()
print("connection request from" + str(addr))
