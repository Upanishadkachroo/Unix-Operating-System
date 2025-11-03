import socket
import math

def main():
    host = '127.0.0.1'
    port = 12346

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    print("UDP server ready on port", port)

    while True:
        data, addr = server_socket.recvfrom(1024)
        num = int(data.decode())
        print("Received number:", num, "from", addr)
        result = math.factorial(num)
        server_socket.sendto(str(result).encode(), addr)

if __name__ == "__main__":
    main()
