import socket
import threading
import math
import numpy as np

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break

        parts = data.strip().split()
        command = parts[0].lower()

        if command == "factorial":
            n = int(parts[1])
            result = math.factorial(n)
        elif command == "reverse":
            result = " ".join(parts[1:])[::-1]
        elif command == "multiply":
            # Example: multiply 2x2 matrices as flattened lists
            nums = list(map(int, parts[1:]))
            A = np.array(nums[:4]).reshape(2,2)
            B = np.array(nums[4:]).reshape(2,2)
            result = str(A @ B)
        else:
            result = "Unknown command"

        conn.send(result.encode())

    conn.close()

def main():
    host = '127.0.0.1'
    port = 12348
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print("Distributed computation server running on port", port)

    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    main()
