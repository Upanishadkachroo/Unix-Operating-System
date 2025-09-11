import socket

host='127.0.0.1'
port=8000

obj=socket.socket()
obj.connect((host, port))
message=input("write message")
while message != 'q':
   obj.send(message.encode())
   data = obj.recv(1024).decode()
   print ('Received from server: ' + data)
   message = input("type message: ")
obj.close()
