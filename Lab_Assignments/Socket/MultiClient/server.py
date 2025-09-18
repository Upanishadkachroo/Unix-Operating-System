import socket
import threading
import time

# List of connected clients
clients = []

# Server configuration
HOST = '0.0.0.0'  # Accept connections from all available network interfaces
PORT = 5002       # Port to listen on

# Function to broadcast messages to all connected clients
def broadcast(message, client_socket):
    message_size = len(message)  # Get the size of the message in bytes
    print(f"Broadcasting message of size {message_size} bytes.")
    start_time = time.time()  # Start time for broadcasting
    
    for client in clients:
        if client != client_socket:
            try:
                client.send(message)
            except:
                # Remove client if the connection is lost
                clients.remove(client)
    
    end_time = time.time()  # End time for broadcasting
    print(f"Broadcast completed in {end_time - start_time:.4f} seconds.")
    print(f"Size of the broadcasted message: {message_size} bytes.")

# Function to handle communication with a single client
def handle_client(client_socket, client_address):
    print(f"New connection: {client_address}")
    
    while True:
        try:
            # Receive message from client
            start_time = time.time()  # Start time for receiving the message
            message = client_socket.recv(1024)
            
            if not message:
                break

            # Measure the size of the received message
            message_size = len(message)
            print(f"Received message of size {message_size} bytes.")
            print("Received message:",message.decode('utf-8'))
            end_time = time.time()  # End time for receiving the message
            print(f"Time to receive message: {end_time - start_time:.4f} seconds.")
            
            # Broadcast the received message to all other clients
            broadcast(message, client_socket)

        except Exception as e:
            # Handle client disconnection
            clients.remove(client_socket)
            break

    print(f"Connection closed: {client_address}")
    client_socket.close()

# Setting up the server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server started on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        
        # Start a new thread for each client
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    start_server()
