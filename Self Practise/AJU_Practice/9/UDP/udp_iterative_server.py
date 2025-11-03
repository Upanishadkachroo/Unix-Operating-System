import socket

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("127.0.0.1", 5001))
    print("[SERVER] UDP Iterative Server started...")

    while True:
        data, addr = server_socket.recvfrom(1024)
        print(f"[SERVER] Received from {addr}: {data.decode().strip()}")
        reply = f"Echo from server: {data.decode()}"
        server_socket.sendto(reply.encode(), addr)

if __name__ == "__main__":
    main()
