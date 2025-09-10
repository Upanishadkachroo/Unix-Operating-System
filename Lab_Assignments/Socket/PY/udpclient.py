import socket

HOST = "127.0.0.1"  # Server IP
PORT = 8080         # Same port as server

# 1. Create socket (IPv4, UDP)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2. Send message (no connection required)
client_socket.sendto(b"Hello from UDP client!", (HOST, PORT))

# 3. Receive response
data, addr = client_socket.recvfrom(1024)
print("Server says: ", data.decode()) 

# 4. Close socket
client_socket.close()

