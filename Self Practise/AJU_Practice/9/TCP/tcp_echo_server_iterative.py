import socket

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 5050))
    s.listen(1)
    print("[SERVER] TCP Iterative Echo Server started...")

    while True:
        conn, addr = s.accept()
        print(f"[SERVER] Connected with {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)  # echo back
        conn.close()
        print(f"[SERVER] Connection closed with {addr}")

if __name__ == "__main__":
    main()
