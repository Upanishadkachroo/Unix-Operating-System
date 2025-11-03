import socket

def main():
    host = '127.0.0.1'
    port = 12346

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        num = input("Enter a number ('exit' to quit): ")
        if num.lower() == 'exit':
            break
        client_socket.sendto(num.encode(), (host, port))
        data, _ = client_socket.recvfrom(1024)
        print("Factorial from server:", data.decode())

    client_socket.close()

if __name__ == "__main__":
    main()
