import socket

def reverse_string(s):
    return s[::-1]

def main():
    host = '127.0.0.1'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print("Server is listening on port", port)

    conn, addr = server_socket.accept()
    print("Connected by", addr)

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print("Received:", data)
        reversed_data = reverse_string(data)
        conn.send(reversed_data.encode())

    conn.close()
    server_socket.close()

if __name__ == "__main__":
    main()
