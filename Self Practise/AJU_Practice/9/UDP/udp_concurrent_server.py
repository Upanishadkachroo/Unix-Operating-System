import socket
import threading

def handle_client(data, addr, server_socket):
    print(f"[THREAD] Processing message from {addr}")
    reply = f"Echo from server: {data.decode()}"
    server_socket.sendto(reply.encode(), addr)

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("127.0.0.1", 5001))
    print("[SERVER] UDP Concurrent Server started...")

    while True:
        data, addr = server_socket.recvfrom(1024)
        print(f"[SERVER] Received from {addr}: {data.decode().strip()}")
        thread = threading.Thread(target=handle_client, args=(data, addr, server_socket))
        thread.start()

if __name__ == "__main__":
    main()
