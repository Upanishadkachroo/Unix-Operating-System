import socket

def main():
    host = '127.0.0.1'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:
        msg = input("Enter a string ('exit' to quit): ")
        if msg.lower() == 'exit':
            break
        client_socket.send(msg.encode())
        data = client_socket.recv(1024).decode()
        print("Reversed from server:", data)

    client_socket.close()

if __name__ == "__main__":
    main()
