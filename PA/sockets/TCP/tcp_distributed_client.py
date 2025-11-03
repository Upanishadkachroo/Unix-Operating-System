import socket

def main():
    host = '127.0.0.1'
    port = 12348

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    print("Available commands:")
    print("  factorial <n>")
    print("  reverse <string>")
    print("  multiply <8 numbers for 2 matrices>")

    while True:
        msg = input("Enter command ('exit' to quit): ")
        if msg.lower() == 'exit':
            break
        client_socket.send(msg.encode())
        data = client_socket.recv(4096).decode()
        print("Result:", data)

    client_socket.close()

if __name__ == "__main__":
    main()
