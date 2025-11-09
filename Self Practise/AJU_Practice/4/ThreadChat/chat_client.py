import socket
import threading

HOST = '127.0.0.1'  # same as server
PORT = 5000

def receive_messages(client_socket):
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            if msg:
                print("\n" + msg)
        except:
            print("Disconnected from server.")
            client_socket.close()
            break

def client_program():
    name = input("Enter your name: ")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    
    thread = threading.Thread(target=receive_messages, args=(client_socket,))
    thread.start()
    
    while True:
        message = input()
        if message.lower() == 'exit':
            client_socket.close()
            break
        full_message = f"{name}: {message}"
        client_socket.send(full_message.encode())

if __name__ == "__main__":
    client_program()
