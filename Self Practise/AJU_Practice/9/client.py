import socket

def main():
    client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect(("127.0.0.1", 5050))
    print("[cleint] socket connected")

    data=client_socket.recv(1024).decode()
    print("[client] from server:", data)

    reply="thank you and love you"
    client_socket.sendall(reply.encode())

    client_socket.close()
    print("[client] connection closed")

if __name__=="__main__":
    main()