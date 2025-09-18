import socket
import threading
import time
import sys

# Client configuration
SERVER_HOST = '127.0.0.1'  # IP address of the server (localhost for testing)
SERVER_PORT = 12345        # Port of the server

# Function to receive messages from the server
def receive_messages(client_socket):
    while True:
        try:
            start_time = time.time()  # Start time for receiving the message
            message = client_socket.recv(1024).decode('utf-8')
            
            if message:
                message_size = len(message.encode('utf-8'))  # Size in bytes
                print(f"Received message: {message}")
                print(f"Size of received message: {message_size} bytes")
                end_time = time.time()  # End time for receiving the message
                print(f"Time to receive message: {end_time - start_time:.4f} seconds")
            else:
                break
        except:
            print("Error in receiving message.")
            break

# Function to send messages to the server
def send_messages(client_socket):
    while True:
        message = input("Enter message to send (or 'exit' to quit): ")
        
        if message.lower() == 'exit':
            client_socket.send('User has left the chat'.encode('utf-8'))
            client_socket.close()
            break
        else:
            start_time = time.time()  # Start time for sending the message
            message_size = len(message.encode('utf-8'))  # Size in bytes
            print(f"Sending message of size {message_size} bytes.")
            
            client_socket.send(message.encode('utf-8'))
            
            end_time = time.time()  # End time for sending the message
            print(f"Time to send message: {end_time - start_time:.4f} seconds.")

def start_client():
    # Create the client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
    except ConnectionRefusedError:
        print("Failed to connect to the server.")
        sys.exit(1)

    print("Connected to the server. Type your messages:")
    
    # Start threads for receiving and sending messages
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()
    send_messages(client_socket)

if __name__ == "__main__":
    start_client()
