import socket
import threading

def handle_client(conn, addr):
    print(f"[THREAD] Client {addr} connected.")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        conn.sendall(data)
    print(f"[THREAD] Client {addr} disconnected.")
    conn.close()

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 5050))
    s.listen(5)
    print("[SERVER] TCP Concurrent Echo Server started...")

    while True:
        conn, addr = s.accept()
        t = threading.Thread(target=handle_client, args=(conn, addr))
        t.start()

if __name__ == "__main__":
    main()
