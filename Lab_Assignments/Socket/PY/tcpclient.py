import socket

HOST = "127.0.0.1"  # Server IP
PORT = 8080         # Same port as server

# 1. Create socket (IPv4, TCP)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. Connect to server
client_socket.connect((HOST, PORT))

# 3. Send message
client_socket.sendall(b"Hello from TCP client!")

# 4. Receive response
data = client_socket.recv(1024).decode()
print("Server says:", data)

# 5. Close socket
client_socket.close()

