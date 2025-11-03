import socket
import os

def main():
    host = '127.0.0.1'
    port = 12347

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    print("UDP File Server running on port", port)

    filename, addr = server_socket.recvfrom(1024)
    filename = filename.decode()

    if not os.path.exists(filename):
        server_socket.sendto(b"ERROR: File not found", addr)
        return

    with open(filename, "rb") as f:
        while True:
            chunk = f.read(1024)
            if not chunk:
                break
            server_socket.sendto(chunk, addr)
            ack, _ = server_socket.recvfrom(1024)
            if ack.decode() != "ACK":
                break

    server_socket.sendto(b"END", addr)
    print("File transfer complete.")

if __name__ == "__main__":
    main()
