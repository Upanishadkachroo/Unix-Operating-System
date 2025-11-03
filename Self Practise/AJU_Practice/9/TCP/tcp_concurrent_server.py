import socket
import threading

def handle_client(conn, addr):
    print(f"[THREAD] Connected with {addr}")
    conn.sendall(b"Welcome to concurrent TCP server!\n")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(f"[{addr}] {data.decode().strip()}")
        conn.sendall(b"Server Echo: " + data)
    conn.close()
    print(f"[THREAD] Connection closed with {addr}")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 5000))
    server_socket.listen(5)
    print("[SERVER] Concurrent TCP Server started...")

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[INFO] Active connections: {threading.active_count() - 1}")

if __name__ == "__main__":
    main()
