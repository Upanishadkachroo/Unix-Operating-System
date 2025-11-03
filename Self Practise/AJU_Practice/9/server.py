import socket

def main():
    server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind(("127.0.0.1", 5050))

    server_socket.listen(1)
    print("[server] waiting to conncet")

    conn, addr=server_socket.accept()
    print(f"[server] connceted to client")

    msg="welcome, u are connceted to server"
    conn.sendall(msg.encode())

    data=conn.recv(1024).decode()
    print("[server] recieved from client:", data)

    conn.close()
    server_socket.close()
    print("[server] closed")


if __name__=="__main__":
    main()