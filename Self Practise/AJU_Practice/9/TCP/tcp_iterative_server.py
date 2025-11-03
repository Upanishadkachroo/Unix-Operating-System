import socket

def handle_client(conn, addr):
    print(f"[SERVER] Connected with {addr}")
    conn.sendall(b"Welcome to iterative TCP server!\n")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(f"[SERVER] Received from {addr}: {data.decode().strip()}")
        conn.sendall(b"Server Echo: " + data)
    conn.close()
    print(f"[SERVER] Connection closed with {addr}")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 5000))
    server_socket.listen(1)
    print("[SERVER] Iterative TCP Server started...")

    while True:
        conn, addr = server_socket.accept()
        handle_client(conn, addr)  # ⚠️ handled one-by-one (blocking)

if __name__ == "__main__":
    main()
