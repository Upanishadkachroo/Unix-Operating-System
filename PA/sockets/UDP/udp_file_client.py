import socket

def main():
    host = '127.0.0.1'
    port = 12347

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    filename = input("Enter filename to download: ")
    client_socket.sendto(filename.encode(), (host, port))

    with open("received_" + filename, "wb") as f:
        while True:
            data, _ = client_socket.recvfrom(1024)
            if data == b"END" or b"ERROR" in data:
                print(data.decode())
                break
            f.write(data)
            client_socket.sendto(b"ACK", (host, port))

    print("File received successfully.")
    client_socket.close()

if __name__ == "__main__":
    main()
