import socket

HOST = "127.0.0.1"  # Localhost
PORT = 8080         # Port to listen on

# 1. Create socket (IPv4, TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. Bind to IP/Port
server_socket.bind((HOST, PORT))

# 3. Listen for connections
server_socket.listen()
print(f"TCP Server listening on {HOST}:{PORT}...")

# 4. Accept a connection
conn, addr = server_socket.accept()
print(f"Connected by {addr}")

# 5. Receive data
data = conn.recv(1024).decode()
print("Client says:", data)

# 6. Send response
conn.sendall(b"Hello from TCP server!\n")

# 7. Close sockets
conn.close()
server_socket.close()
