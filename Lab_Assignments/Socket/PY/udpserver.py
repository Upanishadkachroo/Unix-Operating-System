import socket

HOST = "127.0.0.1"  # Localhost
PORT = 8080         # Port to listen on

# 1. Create socket (IPv4, UDP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2. Bind to IP/Port
server_socket.bind((HOST, PORT))

print(f"UDP Server listening on {HOST}:{PORT}...")

# 3. Receive message (recvfrom returns data + client address)
data, addr = server_socket.recvfrom(1024)
print(f"Client {addr} says: {data.decode()}")

# 4. Send response back
server_socket.sendto(b"Hello from UDP server!\n", addr)

# 5. Close socket
server_socket.close()
 
